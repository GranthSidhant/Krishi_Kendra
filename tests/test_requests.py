import pytest
from app import create_app
from app.extensions import db
from app.models import User, FarmerProfile, ColdStorage, ColdStorageBooking, TransportBooking, AdminTicket
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client_and_users():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            farmer = User(
                custom_id='FK-2026-7777',
                phone='9811122233',
                name='Ramesh Kisan',
                role='farmer',
                is_verified=True
            )
            farmer.set_password('pass123')
            db.session.add(farmer)
            db.session.flush()

            prof = FarmerProfile(user_id=farmer.id, district='Nashik', state='Maharashtra')
            db.session.add(prof)

            admin = User(
                custom_id='ADM-001',
                phone='9000000001',
                name='Admin Officer',
                role='admin',
                is_verified=True
            )
            admin.set_password('adminpass')
            db.session.add(admin)

            facility = ColdStorage(
                name='Nashik Kisan Sahakari Cold Storage',
                address='Panchavati MIDC',
                district='Nashik',
                state='Maharashtra',
                total_capacity_mt=5000,
                available_capacity_mt=2500,
                approx_charge_per_month_per_quintal=65.0
            )
            db.session.add(facility)
            db.session.commit()

            # Session for farmer
            with client.session_transaction() as sess:
                sess['user_id'] = farmer.id
                sess['role'] = 'farmer'

            yield client, farmer, admin, facility
            db.session.remove()
            db.drop_all()


def test_requests_hub_rendering(client_and_users):
    client, farmer, admin, facility = client_and_users

    res = client.get('/requests/')
    assert res.status_code == 200
    assert b'My Service Requests Hub' in res.data
    assert b'Cold Storage Space Requests' in res.data
    assert b'Vehicle Transport Bookings' in res.data
    assert b'Platform Admin Requests' in res.data


def test_admin_ticket_flow(client_and_users):
    client, farmer, admin, facility = client_and_users

    # Submit an admin ticket
    res = client.post('/requests/admin-ticket/create', data={
        'category': 'Payment & Escrow Release Dispute',
        'priority': 'high',
        'subject': 'Escrow payout pending for Order #ORD-9901',
        'description': 'Buyer received 20 quintals of wheat, but bank payout has not arrived.'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Escrow payout pending' in res.data

    ticket = AdminTicket.query.filter_by(user_id=farmer.id).first()
    assert ticket is not None
    assert ticket.priority == 'high'
    assert ticket.status == 'open'


def test_transport_booking_flow(client_and_users):
    client, farmer, admin, facility = client_and_users

    res = client.post('/requests/transport/create', data={
        'pickup_address': 'Family Farm Gate, Dindori, Nashik',
        'drop_address': 'Vashi APMC Mandi, Navi Mumbai',
        'produce_type': 'Red Onions',
        'quantity_quintals': '25',
        'vehicle_type': 'Medium 6-Wheeler Truck (up to 7 MT)',
        'scheduled_datetime': '2026-09-15 08:00'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'TRP-2026-' in res.data

    booking = TransportBooking.query.filter_by(user_id=farmer.id).first()
    assert booking is not None
    assert booking.quantity_quintals == 25.0
    assert booking.status == 'driver_assigned'
