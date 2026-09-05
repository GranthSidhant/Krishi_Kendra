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
    assert "Wheat" in data['response_text']
    assert "/farmer/mandi-rates" in data['action_url']

    # Test Hindi crop query
    res_hi = client.post('/api/voice-query', json={'query': 'प्याज का भाव क्या है?'})
    assert res_hi.status_code == 200
    data_hi = res_hi.get_json()
    assert data_hi['success'] is True
    assert "Onion" in data_hi['response_text']

    # Test scheme query
    res_scheme = client.post('/api/voice-query', json={'query': 'PM KISAN samman nidhi'})
    assert res_scheme.status_code == 200
    data_scheme = res_scheme.get_json()
    assert "PM-KISAN" in data_scheme['response_text']


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


def test_home_page_rendering_for_all_roles(client):
    # 1. Guest
    res_guest = client.get('/')
    assert res_guest.status_code == 200
    assert b"I am a Farmer" in res_guest.data or b"btn_i_am_farmer" in res_guest.data

    # 2. Farmer
    client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)
    res_farmer = client.get('/')
    assert res_farmer.status_code == 200
    assert b"Farmer Dashboard" in res_farmer.data or b"btn_farmer_dash" in res_farmer.data
    client.get('/auth/logout')

    # 3. Buyer
    client.post('/auth/login', data={'login_id': '9222222222', 'password': 'buyerpass'}, follow_redirects=True)
    res_buyer = client.get('/')
    assert res_buyer.status_code == 200
    assert b"Buyer Dashboard" in res_buyer.data or b"btn_buyer_dash" in res_buyer.data
    client.get('/auth/logout')

    # 4. Admin
    client.post('/auth/admin/login', data={'login_id': '9999999999', 'password': 'adminpass'}, follow_redirects=True)
    res_admin = client.get('/')
    assert res_admin.status_code == 200
    assert b"Admin Portal" in res_admin.data or b"btn_admin_portal" in res_admin.data

