import pytest
from app import create_app
from app.extensions import db
from app.models import User, FarmerProfile, Inventory
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client_with_farmer():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            farmer = User(
                custom_id='FK-2026-5555',
                phone='9900011122',
                name='Kisan Tester',
                role='farmer',
                is_verified=True
            )
            farmer.set_password('pass123')
            db.session.add(farmer)
            db.session.flush()

            prof = FarmerProfile(user_id=farmer.id, district='Nashik', state='Maharashtra')
            db.session.add(prof)
            db.session.commit()

            # Log in the farmer
            with client.session_transaction() as sess:
                sess['user_id'] = farmer.id
                sess['role'] = 'farmer'

            yield client, farmer
            db.session.remove()
            db.drop_all()

def test_farmer_inventory_crud(client_with_farmer):
    client, farmer = client_with_farmer

    # Add produce
    res = client.post('/farmer/inventory/add', data={
        'product_name': 'Organic Wheat',
        'category_name': 'Cereals & Grains',
        'available_quantity': '1500',
        'unit': 'kg',
        'expected_price_per_unit': '25.5',
        'quality_grade': 'Grade A (Premium)',
        'description': 'Direct farm harvested.'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Organic Wheat' in res.data

    # Verify in DB
    inv = Inventory.query.filter_by(farmer_id=farmer.id, product_name='Organic Wheat').first()
    assert inv is not None
    assert inv.available_quantity == 1500.0
    assert inv.expected_price_per_unit == 25.5

    # Edit inventory
    res_edit = client.post(f'/farmer/inventory/edit/{inv.id}', data={
        'product_name': 'Organic Wheat (Updated)',
        'available_quantity': '1200',
        'unit': 'kg',
        'expected_price_per_unit': '26.0',
        'quality_grade': 'Grade A (Premium)',
        'status': 'available',
        'description': 'Updated description'
    }, follow_redirects=True)
    assert res_edit.status_code == 200

    updated_inv = Inventory.query.get(inv.id)
    assert updated_inv.available_quantity == 1200.0
    assert updated_inv.expected_price_per_unit == 26.0

    # Delete inventory
    res_del = client.post(f'/farmer/inventory/delete/{inv.id}', follow_redirects=True)
    assert res_del.status_code == 200
    assert Inventory.query.get(inv.id) is None
