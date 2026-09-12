import pytest
from app import create_app
from app.extensions import db
from app.models import User, FarmerProfile, BuyerProfile, Inventory, Offer, Order, Delivery
from app.services.escrow_service import EscrowService
from app.services.logistics_service import LogisticsService
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app_and_client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            farmer = User(
                custom_id="FK-2026-9001",
                phone="9800012345",
                name="Suresh Kisan",
                role="farmer",
                is_verified=True
            )
            farmer.set_password("pass123")
            db.session.add(farmer)
            db.session.flush()

            farmer_prof = FarmerProfile(
                user_id=farmer.id,
                state="Maharashtra",
                district="Nashik",
                farm_location_name="Kisan Agro Farms, Niphad",
                farm_size_acres=5.5
            )
            db.session.add(farmer_prof)

            buyer = User(
                custom_id="BK-2026-9002",
                phone="9800067890",
                name="Rajesh Agro Traders",
                role="buyer",
                is_verified=True
            )
            buyer.set_password("pass123")
            db.session.add(buyer)
            db.session.flush()

            buyer_prof = BuyerProfile(
                user_id=buyer.id,
                state="Maharashtra",
                district="Mumbai",
                business_name="Rajesh Agro Wholesalers",
                address="APMC Yard Vashi, Gate 4, Navi Mumbai"
            )
            db.session.add(buyer_prof)

            # Farmer lists 100 quintals of Onion
            inv = Inventory(
                farmer_id=farmer.id,
                product_name="Onion",
                available_quantity=100.0,
                unit="quintal",
                expected_price_per_unit=2400.0,
                quality_grade="Grade A",
                status="available"
            )
            db.session.add(inv)
            db.session.commit()

            farmer_id = farmer.id
            buyer_id = buyer.id
            inv_id = inv.id

        yield app, client, farmer_id, buyer_id, inv_id

        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_full_closed_loop_trade_chain(app_and_client):
    """
    Tests the complete end-to-end closed-loop trade lifecycle:
    Produce Listing -> Offer -> Acceptance -> Escrow Payment & Stock Auto-Deduct ->
    Logistics -> Pickup OTP Handover -> Delivery OTP Inspection -> Instant Farmer Payout -> Mutual Rating -> Invoice
    """
    app, client, farmer_id, buyer_id, inv_id = app_and_client

    # 1. Buyer logs in and sends an Offer for 40 quintals @ Rs. 2350
    with client.session_transaction() as sess:
        sess['user_id'] = buyer_id
        sess['role'] = 'buyer'

    offer_data = {
        'quantity': 40.0,
        'unit': 'quintal',
        'offered_price_per_unit': 2350.0,
        'notes': 'Need dispatch by tomorrow morning'
    }
    resp = client.post(f'/buyer/direct-request/{inv_id}', data=offer_data, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        offer = Offer.query.filter_by(buyer_id=buyer_id, farmer_id=farmer_id).first()
        assert offer is not None
        assert offer.status == 'pending'
        assert offer.total_amount == 40.0 * 2350.0
        offer_id = offer.id

    # 2. Farmer logs in and Accepts the Offer -> Creates Order & Delivery with OTPs
    with client.session_transaction() as sess:
        sess['user_id'] = farmer_id
        sess['role'] = 'farmer'

    resp = client.post(f'/farmer/offer/{offer_id}/respond', data={'action': 'accept'}, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        order = Order.query.filter_by(offer_id=offer_id).first()
        assert order is not None
        assert order.status == 'confirmed'
        assert order.total_amount == 94000.0
        assert order.delivery is not None
        assert len(order.delivery.pickup_otp) == 6
        assert len(order.delivery.delivery_otp) == 6
        pickup_otp = order.delivery.pickup_otp
        delivery_otp = order.delivery.delivery_otp
        order_id = order.id

    # 3. Buyer logs in and Funds Escrow -> Auto-deducts 40 quintals from Farmer Inventory
    with client.session_transaction() as sess:
        sess['user_id'] = buyer_id
        sess['role'] = 'buyer'

    resp = client.post(f'/orders/{order_id}/pay-escrow', data={'payment_method': 'UPI_ESCROW', 'upi_id': 'trader@okaxis'}, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        order = Order.query.get(order_id)
        assert order.escrow_txn_id is not None
        assert order.escrow_txn_id.startswith('ESC-TXN-')
        assert order.payment_status == 'in_escrow'
        
        # Verify Farmer stock deducted from 100 to 60 quintals
        inv_after = Inventory.query.get(inv_id)
        assert inv_after.available_quantity == 60.0
        assert inv_after.status == 'available'

    # 4. Assign Logistics Transport (Cold Reefer Truck)
    resp = client.post(f'/orders/{order_id}/assign-transport', data={
        'vehicle_category': 'cold_reefer',
        'driver_name': 'Kailash Patil',
        'driver_phone': '+91 98222 33445',
        'vehicle_number': 'MH-15-AB-9988',
        'distance_km': 60.0
    }, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        order = Order.query.get(order_id)
        assert order.delivery.driver_name == 'Kailash Patil'
        assert order.delivery.vehicle_category == 'cold_reefer'
        assert order.delivery.estimated_cost > 0

    # 5. Farm-gate Loading: Farmer / Driver enters Pickup OTP -> Order moves to 'in_transit'
    with client.session_transaction() as sess:
        sess['user_id'] = farmer_id
        sess['role'] = 'farmer'

    # Test wrong OTP rejected
    resp = client.post(f'/orders/{order_id}/verify-pickup-otp', data={'pickup_otp': '000000'}, follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        order = Order.query.get(order_id)
        assert order.delivery.pickup_verified_at is None

    # Correct Pickup OTP
    resp = client.post(f'/orders/{order_id}/verify-pickup-otp', data={'pickup_otp': pickup_otp}, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        order = Order.query.get(order_id)
        assert order.status == 'in_transit'
        assert order.delivery.pickup_verified_at is not None

    # 6. Destination Arrival: Buyer inspects produce & Enters Delivery OTP -> Releases Escrow Payout
    with client.session_transaction() as sess:
        sess['user_id'] = buyer_id
        sess['role'] = 'buyer'

    resp = client.post(f'/orders/{order_id}/verify-delivery-otp', data={'delivery_otp': delivery_otp}, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        order = Order.query.get(order_id)
        assert order.status == 'delivered'
        assert order.payment_status == 'released'
        assert order.payout_txn_id is not None
        assert order.payout_txn_id.startswith('PAYOUT-')
        assert order.payout_released_at is not None

    # 7. Post-Trade Mutual Rating: Buyer rates Farmer & Farmer rates Buyer
    resp_rate_buyer = client.post(f'/orders/{order_id}/rate', data={'rating': 5, 'review': 'Fresh Grade A onions, highly recommended!'}, follow_redirects=True)
    assert resp_rate_buyer.status_code == 200

    with client.session_transaction() as sess:
        sess['user_id'] = farmer_id
        sess['role'] = 'farmer'

    resp_rate_farmer = client.post(f'/orders/{order_id}/rate', data={'rating': 5, 'review': 'Prompt weighment and instantaneous escrow settlement.'}, follow_redirects=True)
    assert resp_rate_farmer.status_code == 200

    with app.app_context():
        order = Order.query.get(order_id)
        assert order.buyer_rating == 5
        assert order.farmer_rating == 5

    # 8. View Tax Invoice & Payout Certificate
    resp_inv = client.get(f'/orders/{order_id}/invoice')
    assert resp_inv.status_code == 200
    assert b'TAX INVOICE' in resp_inv.data
    assert b'Onion' in resp_inv.data

    resp_payout = client.get(f'/orders/{order_id}/payout-receipt')
    assert resp_payout.status_code == 200
    assert b'SETTLEMENT COMPLETED' in resp_payout.data
