import pytest
from app import create_app
from app.extensions import db
from app.models import User, BuyerProfile, Requirement
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client_with_buyer():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            buyer = User(
                custom_id='BK-2026-7777',
                phone='9988001122',
                name='Buyer Tester',
                role='buyer',
                is_verified=True
            )
            buyer.set_password('pass123')
            db.session.add(buyer)
            db.session.flush()

            prof = BuyerProfile(user_id=buyer.id, business_name='Testing Wholesale', district='Mumbai')
            db.session.add(prof)
            db.session.commit()

            with client.session_transaction() as sess:
                sess['user_id'] = buyer.id
                sess['role'] = 'buyer'

            yield client, buyer
            db.session.remove()
            db.drop_all()

def test_buyer_post_requirement(client_with_buyer):
    client, buyer = client_with_buyer

    res = client.post('/buyer/post-requirement', data={
        'product_name': 'Red Onion',
        'required_quantity': '3000',
        'unit': 'kg',
        'required_quality': 'Grade A (Premium)',
        'target_price_per_unit': '18.5',
        'delivery_district': 'Mumbai',
        'delivery_location': 'Vashi APMC Hub'
    }, follow_redirects=True)
    assert res.status_code == 200

    # Verify requirement in database
    req = Requirement.query.filter_by(buyer_id=buyer.id, product_name='Red Onion').first()
    assert req is not None
    assert req.required_quantity == 3000.0
    assert req.delivery_district == 'Mumbai'
