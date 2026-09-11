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


