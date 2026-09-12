import pytest
from app import create_app
from config import Config
from app.extensions import db
from app.models import User, Requirement, Offer, Order, ChatThread, Message, Delivery

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_requirement_quotation_and_chat_deal_acceptance(client, app):
    with app.app_context():
        # 1. Create Farmer and Buyer
        farmer = User(name='Ramesh Patil', phone='9812345670', role='farmer', custom_id='FK-2026-1011')
        farmer.set_password('Pass@123')
        buyer = User(name='Apex Agro Traders', phone='9812345671', role='buyer', custom_id='BK-2026-2022')
        buyer.set_password('Pass@123')
        db.session.add_all([farmer, buyer])
        db.session.commit()

        farmer_id = farmer.id
        buyer_id = buyer.id

        # 2. Buyer posts a Requirement for 200 Quintals of Wheat
        req = Requirement(
            buyer_id=buyer_id,
            product_name='Sharbati Wheat',
            required_quantity=200.0,
            unit='Quintal',
            target_price_per_unit=2450.0,
            delivery_state='Maharashtra',
            delivery_district='Nashik',
            required_quality='Grade A',
            is_pre_order=False,
            status='open'
        )
        db.session.add(req)
        db.session.commit()
        req_id = req.id

    # 3. Farmer browses requirements and submits formal quotation
    with client.session_transaction() as sess:
        sess['user_id'] = farmer_id
        sess['role'] = 'farmer'

    resp = client.post(f'/farmer/requirements/{req_id}/quote', data={
        'offered_price': 2400.0,
        'quantity': 200.0,
        'notes': 'Grade A certified wheat batch available for immediate loading.'
    }, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        # Verify Offer created
        offer = Offer.query.filter_by(requirement_id=req_id, farmer_id=farmer_id).first()
        assert offer is not None
        assert offer.offered_price_per_unit == 2400.0
        assert offer.quantity == 200.0
        assert offer.total_amount == 480000.0
        offer_id = offer.id

        # Verify ChatThread created and linked
        thread = ChatThread.query.filter_by(farmer_id=farmer_id, buyer_id=buyer_id).first()
        assert thread is not None
        assert thread.offer_id == offer_id
        assert thread.requirement_id == req_id

        # Verify Offer message card is posted in chat
        msg = Message.query.filter_by(thread_id=thread.id).order_by(Message.id.desc()).first()
        assert msg is not None
        meta = msg.get_metadata()
        assert meta.get('offer_id') == offer_id
        assert meta.get('price') == 2400.0

    # 4. Buyer logs in, opens chat, and accepts the deal & creates order
    with client.session_transaction() as sess:
        sess['user_id'] = buyer_id
        sess['role'] = 'buyer'

    resp_accept = client.post(f'/buyer/offer/{offer_id}/respond', data={'action': 'accept'}, follow_redirects=True)
    assert resp_accept.status_code == 200

    with app.app_context():
        order = Order.query.filter_by(offer_id=offer_id).first()
        assert order is not None
        assert order.status == 'confirmed'
        assert order.payment_status == 'in_escrow'
        assert order.total_amount == 480000.0
        assert order.delivery is not None
        assert order.delivery.pickup_otp is not None
        assert order.delivery.delivery_otp is not None
        assert order.order_code.startswith('ORD-2026-')

        # Verify idempotency: calling accept again returns the order safely without 500 error
        resp_reaccept = client.post(f'/buyer/offer/{offer_id}/respond', data={'action': 'accept'}, follow_redirects=True)
        assert resp_reaccept.status_code == 200
