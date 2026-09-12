import os
import io
import pytest
from app import create_app
from app.extensions import db
from app.models import User, ChatThread, Message, Offer, Order
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        
        # Seed test admin
        admin = User(
            custom_id="ADM-2026-9999",
            name="Super Admin",
            phone="9999999999",
            role="admin",
            is_active=True
        )
        admin.set_password("adminpass")
        db.session.add(admin)

        # Seed test farmer & buyer
        farmer = User(
            custom_id="FK-2026-1111",
            name="Ramesh Farmer",
            phone="9111111111",
            role="farmer",
            is_active=True
        )
        farmer.set_password("farmerpass")
        db.session.add(farmer)

        buyer = User(
            custom_id="BK-2026-2222",
            name="Suresh Buyer",
            phone="9222222222",
            role="buyer",
            is_active=True
        )
        buyer.set_password("buyerpass")
        db.session.add(buyer)

        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_admin_login_flow(client):
    # Admin login with correct password
    res = client.post('/auth/admin/login', data={
        'login_id': '9999999999',
        'password': 'adminpass'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Administrator Super Admin" in res.data or b"Admin" in res.data or b"Dashboard" in res.data


def test_ai_voice_query_api(client):
    # Test crop rate query
    res = client.post('/api/voice-query', json={'query': 'What is the price of Wheat today?'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert "wheat" in data['response_text'].lower()
    assert "/farmer/mandi-rates" in data['action_url']

    # Test Hindi crop query
    res_hi = client.post('/api/voice-query', json={'query': 'प्याज का भाव क्या है?'})
    assert res_hi.status_code == 200
    data_hi = res_hi.get_json()
    assert data_hi['success'] is True
    assert "onion" in data_hi['response_text'].lower() or "प्याज" in data_hi['response_text'] or "भाव" in data_hi['response_text']

    # Test scheme query
    res_scheme = client.post('/api/voice-query', json={'query': 'PM KISAN samman nidhi'})
    assert res_scheme.status_code == 200
    data_scheme = res_scheme.get_json()
    assert "PM-KISAN" in data_scheme['response_text'] or "kisan" in data_scheme['response_text'].lower()



def test_chat_offer_and_voice_features(app, client):
    with app.app_context():
        farmer = User.query.filter_by(role='farmer').first()
        buyer = User.query.filter_by(role='buyer').first()

        thread = ChatThread(
            farmer_id=farmer.id,
            buyer_id=buyer.id,
            subject_product="Tomato"
        )
        db.session.add(thread)
        db.session.commit()
        thread_id = thread.id

    # Login as farmer
    res_login = client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)
    assert res_login.status_code == 200

    # Send in-chat offer
    res_offer = client.post(f'/chat/thread/{thread_id}/send-offer', data={
        'product_name': 'Organic Tomato',
        'price': '35',
        'quantity': '200',
        'unit': 'kg',
        'notes': 'High quality farm fresh'
    })
    assert res_offer.status_code == 200
    offer_data = res_offer.get_json()
    assert offer_data['success'] is True
    assert offer_data['message']['type'] == 'counter_card'

    # Send voice note
    audio_bytes = io.BytesIO(b"FAKE_AUDIO_DATA_FOR_TESTING")
    res_voice = client.post(
        f'/chat/thread/{thread_id}/send-voice',
        data={'audio': (audio_bytes, 'recording.webm'), 'duration': '0:07'},
        content_type='multipart/form-data'
    )
    assert res_voice.status_code == 200
    voice_data = res_voice.get_json()
    assert voice_data['success'] is True
    assert voice_data['message']['type'] == 'voice_note'


def test_live_weather_api(client):
    # Test weather query for Nashik
    res = client.get('/api/weather?location=Nashik')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'temperature' in data
    assert 'weather_desc' in data
    assert 'forecast' in data
    assert len(data['forecast']) > 0

    # Test weather query with coordinates
    res_coord = client.get('/api/weather?lat=19.9975&lon=73.7898')
    assert res_coord.status_code == 200
    data_coord = res_coord.get_json()
    assert data_coord['success'] is True
    assert 'temperature' in data_coord


def test_report_submission_and_admin_moderation(app, client):
    with app.app_context():
        from app.models import Inventory
        farmer = User.query.filter_by(role='farmer').first()
        inv = Inventory(
            farmer_id=farmer.id,
            product_name="Alphonso Mango Export Grade",
            category_name="Fruits",
            available_quantity=500.0,
            unit="kg",
            expected_price_per_unit=120.0,
            status="available"
        )
        db.session.add(inv)
        db.session.commit()
        inv_id = inv.id

    # Login as buyer
    client.post('/auth/login', data={'login_id': '9222222222', 'password': 'buyerpass'}, follow_redirects=True)

    # 1. Submit a report on a listing via JSON
    res_rep = client.post('/api/report/submit', json={
        'target_type': 'inventory',
        'target_id': inv_id,
        'reason': 'misleading_price',
        'details': 'Price is quoted 10x below market standard, potential spam listing'
    })
    assert res_rep.status_code == 200
    rep_data = res_rep.get_json()
    assert rep_data['success'] is True
    assert 'report_code' in rep_data

    # 2. Admin logs in to view reports list
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/admin/login', data={'login_id': '9999999999', 'password': 'adminpass'}, follow_redirects=True)

    res_mod = client.get('/admin/moderation')
    assert res_mod.status_code == 200
    assert b'Alphonso Mango Export Grade' in res_mod.data

    # 3. Admin takes action (warn owner)
    with app.app_context():
        from app.models import Report
        rep = Report.query.first()
        rep_id = rep.id

    res_action = client.post(f'/admin/moderation/{rep_id}/action', data={
        'action': 'warn_owner',
        'admin_notes': 'Sent formal warning regarding pricing rules'
    }, follow_redirects=True)
    assert res_action.status_code == 200

    with app.app_context():
        from app.models import Report
        rep = Report.query.get(rep_id)
        assert rep.status == 'resolved'
        assert rep.action_taken == 'warning_sent'


def test_buyer_pre_order_and_farmer_browse(app, client):
    # Login as buyer
    client.post('/auth/login', data={'login_id': '9222222222', 'password': 'buyerpass'}, follow_redirects=True)

    # Post a pre-order contract sowing requirement
    res_req = client.post('/buyer/post-requirement', data={
        'product_name': 'Export Grade Turmeric',
        'required_quantity': '500',
        'unit': 'quintal',
        'target_price_per_unit': '8500',
        'delivery_location': 'Sangli APMC',
        'is_pre_order': 'on',
        'target_harvest_timeline': 'Nov 2026 Season',
        'advance_payment_terms': '25% advance token, 75% upon delivery QC approval'
    }, follow_redirects=True)
    assert res_req.status_code == 200

    with app.app_context():
        from app.models import Requirement
        req = Requirement.query.filter_by(product_name='Export Grade Turmeric').first()
        assert req is not None
        assert req.is_pre_order is True
        assert req.target_harvest_timeline == 'Nov 2026 Season'
        assert '25% advance token' in req.advance_payment_terms

    # Logout buyer & Login as farmer to browse requirements
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)

    res_browse = client.get('/farmer/requirements')
    assert res_browse.status_code == 200
    assert b'Export Grade Turmeric' in res_browse.data
    assert b'Advance Pre-Order' in res_browse.data


def test_farmer_profit_calculator_page(client):
    # Login as farmer
    client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)

    res = client.get('/farmer/profit-calculator')
    assert res.status_code == 200
    assert b'Farmer Profit, Cultivation Cost & ROI Calculator' in res.data
    assert b'Net Farmer Profit' in res.data



def test_transport_shared_pooling(app, client):
    # Login as farmer
    client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)

    # Book transport with shared pooling option
    res_book = client.post('/requests/transport/create', data={
        'vehicle_type': 'Mini Truck (Tata Ace)',
        'pickup_address': 'Farm Gate 2, Nashik Outskirts',
        'drop_address': 'Vashi APMC Market, Mumbai',
        'scheduled_datetime': '2026-10-15 08:00',
        'produce_type': 'Tomatoes',
        'quantity_quintals': '10',
        'pickup_latitude': '19.9975',
        'pickup_longitude': '73.7898',
        'is_shared_pooling': 'on'
    }, follow_redirects=True)
    assert res_book.status_code == 200

    with app.app_context():
        from app.models import TransportBooking
        tb = TransportBooking.query.filter_by(pickup_latitude=19.9975).first()
        assert tb is not None
        assert tb.is_shared_pooling is True
        assert tb.pool_code is not None
        assert tb.pool_code.startswith('POOL-')
        # Base: 800 + (10 * 35) = 1150; with 35% discount = 1150 * 0.65 = 747.5
        assert tb.estimated_cost == 747.5



def test_profile_picture_upload_and_avatar(app, client):
    # Login as farmer
    client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)
    
    # 1. Test Avatar Choice selection
    res_avatar = client.post('/auth/profile', data={
        'name': 'Ramesh Farmer',
        'avatar_choice': 'avatar_farmer_turban',
        'preferred_language': 'hi'
    }, follow_redirects=True)
    assert res_avatar.status_code == 200
    with app.app_context():
        u = User.query.filter_by(phone='9111111111').first()
        assert u.profile_image == 'avatar_farmer_turban'
        assert u.avatar_emoji == '👳‍♂️'

    # 2. Test Custom Photo File Upload
    img_bytes = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4")
    res_img = client.post('/auth/profile', data={
        'name': 'Ramesh Farmer Updated',
        'profile_image_file': (img_bytes, 'my_photo.png')
    }, content_type='multipart/form-data', follow_redirects=True)
    assert res_img.status_code == 200
    with app.app_context():
        u = User.query.filter_by(phone='9111111111').first()
        assert u.profile_image.startswith('data:image/png;base64,')
        assert u.avatar_src.startswith('data:image/png;base64,')




