import pytest
from app import create_app
from app.extensions import db
from app.models import User, FarmerProfile, BuyerProfile, Offer, Order, Delivery
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def test_setup():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            farmer = User(custom_id='FK-301', phone='9300000001', name='Farmer Dave', role='farmer')
            farmer.set_password('pass')
            buyer = User(custom_id='BK-301', phone='9300000002', name='Buyer Alice', role='buyer')
            buyer.set_password('pass')
            db.session.add_all([farmer, buyer])
            db.session.flush()

            db.session.add(FarmerProfile(user_id=farmer.id, district='Nashik'))
            db.session.add(BuyerProfile(user_id=buyer.id, district='Mumbai'))
            db.session.commit()

            yield client, farmer, buyer
            db.session.remove()
            db.drop_all()

def test_offer_accept_and_order_flow(test_setup):
    client, farmer, buyer = test_setup

    # Create offer from buyer to farmer
    offer = Offer(
        buyer_id=buyer.id,
        farmer_id=farmer.id,
        product_name='Tomato',
        quantity=500.0,
        unit='kg',
        offered_price_per_unit=15.0,
        total_amount=7500.0,
        offered_by_role='buyer',
        status='pending'
    )
    db.session.add(offer)
    db.session.commit()

    # Log in as farmer and accept offer
    with client.session_transaction() as sess:
        sess['user_id'] = farmer.id
        sess['role'] = 'farmer'

    res = client.post(f'/farmer/offer/{offer.id}/respond', data={'action': 'accept'}, follow_redirects=True)
    assert res.status_code == 200

    # Verify Order created and Offer accepted
    updated_offer = Offer.query.get(offer.id)
    assert updated_offer.status == 'accepted'

    order = Order.query.filter_by(offer_id=offer.id).first()
    assert order is not None
    assert order.product_name == 'Tomato'
    assert order.total_amount == 7500.0
    assert order.status == 'confirmed'
    assert order.delivery is not None
