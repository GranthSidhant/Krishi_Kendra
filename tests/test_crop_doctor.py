import io
import base64
import pytest
from app import create_app
from app.extensions import db
from app.models import User
from app.services.crop_doctor_service import CropDoctorService
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

        farmer = User(
            custom_id="FK-2026-1111",
            name="Ramesh Farmer",
            phone="9111111111",
            role="farmer",
            is_active=True
        )
        farmer.set_password("farmerpass")
        db.session.add(farmer)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_crop_doctor_page_render(client):
    # Login as farmer
    client.post('/auth/login', data={'login_id': '9111111111', 'password': 'farmerpass'}, follow_redirects=True)
    res = client.get('/farmer/crop-doctor')
    assert res.status_code == 200
    assert b"AI Crop Doctor" in res.data
    assert b"Scan Crop Foliage" in res.data
    assert b"Run AI Disease Diagnosis" in res.data


def test_crop_doctor_sample_endpoint(client):
    res = client.get('/api/crop-doctor/sample/tomato_early_blight')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert "Early Blight" in data['disease_name']
    assert data['confidence_pct'] >= 90
    assert "Mancozeb" in data['chemical_treatment']
    assert "Neem" in data['organic_remedy']


def test_crop_doctor_scan_multipart_upload(client):
    # Mock image bytes
    fake_img = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4")
    res = client.post(
        '/api/crop-doctor/scan',
        data={
            'image': (fake_img, 'leaf_spot.png'),
            'crop_hint': 'Potato',
            'lang': 'hi'
        },
        content_type='multipart/form-data'
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'disease_name' in data
    assert 'organic_remedy' in data
    assert 'chemical_treatment' in data


def test_crop_doctor_scan_base64_payload(client):
    sample_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    res = client.post(
        '/api/crop-doctor/scan',
        json={
            'image_base64': sample_b64,
            'crop_hint': 'Wheat',
            'lang': 'en'
        }
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'disease_name' in data
    assert 'severity' in data
