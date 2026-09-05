import pytest
from app import create_app
from app.extensions import db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register_and_otp(client):
    # Step 1: Register farmer
    res = client.post('/auth/register', data={
        'name': 'Test Farmer',
        'phone': '9811122233',
        'role': 'farmer',
        'password': 'password123',
        'state': 'Maharashtra',
        'district': 'Nashik',
        'preferred_language': 'en'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Verify Mobile Number' in res.data

    # Step 2: Verify OTP
    res_otp = client.post('/auth/verify-otp', data={'otp': '123456'}, follow_redirects=True)
    assert res_otp.status_code == 200
    assert b'Welcome to Krishi Kendra' in res_otp.data or b'Dashboard' in res_otp.data

    # Verify user exists in database
    user = User.query.filter_by(phone='9811122233').first()
    assert user is not None
    assert user.role == 'farmer'
    assert user.custom_id.startswith('FK-2026-')
    assert user.farmer_profile is not None

def test_login_and_logout(client):
    # Create user directly
    user = User(
        custom_id='FK-2026-9999',
        phone='9800011122',
        name='Login Tester',
        role='farmer'
    )
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()

    # Login
    res = client.post('/auth/login', data={
        'login_id': '9800011122',
        'password': 'testpass'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Logged in successfully' in res.data

    # Logout
    res_logout = client.get('/auth/logout', follow_redirects=True)
    assert res_logout.status_code == 200
    assert b'You have been logged out' in res_logout.data
