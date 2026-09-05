import pytest
from app import create_app
from app.extensions import db
from app.models import User, FarmerProfile, BuyerProfile, Inventory, Requirement
from app.services.matching_service import MatchingService
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

def test_matching_service():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

        # Farmer 1: Has 5000 kg Wheat in Nashik
        f1 = User(custom_id='FK-101', phone='9100000001', name='Farmer One', role='farmer', is_verified=True)
        f1.set_password('pass')
        db.session.add(f1)
        db.session.flush()
        db.session.add(FarmerProfile(user_id=f1.id, district='Nashik', open_to_all_quantities=True))
        db.session.add(Inventory(farmer_id=f1.id, product_name='Wheat', available_quantity=5000, unit='kg', expected_price_per_unit=24.0, status='available'))

        # Farmer 2: Has 500 kg Wheat in Pune but minimum order is 1000kg
        f2 = User(custom_id='FK-102', phone='9100000002', name='Farmer Two', role='farmer')
        f2.set_password('pass')
        db.session.add(f2)
        db.session.flush()
        db.session.add(FarmerProfile(user_id=f2.id, district='Pune', open_to_all_quantities=False, min_qty_kg=1000, max_qty_kg=5000))
        db.session.add(Inventory(farmer_id=f2.id, product_name='Wheat', available_quantity=500, unit='kg', expected_price_per_unit=23.0, status='available'))

        # Buyer requirement for 2000 kg Wheat
        b1 = User(custom_id='BK-201', phone='9200000001', name='Buyer One', role='buyer')
        b1.set_password('pass')
        db.session.add(b1)
        db.session.flush()
        req = Requirement(buyer_id=b1.id, product_name='Wheat', required_quantity=2000, unit='kg', delivery_district='Nashik')
        db.session.add(req)
        db.session.commit()

        # Run matching
        matches = MatchingService.find_matching_farmers_for_requirement(req)
        
        # Verify Farmer 1 is matched with high score (>80%)
        assert len(matches) >= 1
        top_match = matches[0]
        assert top_match['farmer'].id == f1.id
        assert top_match['match_score'] >= 85.0
        assert top_match['available_quantity'] == 5000.0

        db.session.remove()
        db.drop_all()
