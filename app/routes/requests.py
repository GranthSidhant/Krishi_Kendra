import random
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.extensions import db
from app.models import User, ColdStorageBooking, TransportBooking, AdminTicket, Order, Notification
from app.routes.auth import login_required

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')


@requests_bp.route('/')
@login_required
def index():
    user = g.user
    active_tab = request.args.get('tab', 'cold_storage')

    # 1. Cold Storage Bookings
    cold_storage_bookings = ColdStorageBooking.query.filter_by(farmer_id=user.id).order_by(ColdStorageBooking.created_at.desc()).all()

    # 2. Transport Bookings
    transport_bookings = TransportBooking.query.filter_by(user_id=user.id).order_by(TransportBooking.created_at.desc()).all()

    # 3. Admin Support Tickets
    admin_tickets = AdminTicket.query.filter_by(user_id=user.id).order_by(AdminTicket.created_at.desc()).all()

    # User's confirmed orders (if they want to link a transport request to an order)
    user_orders = []
    if user.role == 'farmer':
        user_orders = Order.query.filter_by(farmer_id=user.id).all()
    elif user.role == 'buyer':
        user_orders = Order.query.filter_by(buyer_id=user.id).all()

    return render_template(
        'requests/index.html',
        user=user,
        active_tab=active_tab,
        cold_storage_bookings=cold_storage_bookings,
        transport_bookings=transport_bookings,
        admin_tickets=admin_tickets,
        user_orders=user_orders
    )


@requests_bp.route('/admin-ticket/create', methods=['POST'])
@login_required
def create_admin_ticket():
    user = g.user
    category = request.form.get('category', 'General Query').strip()
    subject = request.form.get('subject', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'medium').strip()

    if not subject or not description:
        flash('Please fill in both the subject and description for your admin request.', 'danger')
        return redirect(url_for('requests.index', tab='admin_requests'))

    code_num = random.randint(1000, 9999)
    ticket_code = f"TKT-2026-{code_num}"

    ticket = AdminTicket(
        ticket_code=ticket_code,
        user_id=user.id,
        category=category,
        subject=subject,
        description=description,
        priority=priority,
        status='open'
    )
    db.session.add(ticket)

    # Add confirmation notification
    notif = Notification(
        user_id=user.id,
        title="Admin Support Request Submitted",
        message=f"Your ticket #{ticket_code} ({subject}) has been logged. Krishi Kendra administration will review it shortly.",
        link_url=url_for('requests.index', tab='admin_requests')
    )
    db.session.add(notif)
    db.session.commit()

    flash(f'Support ticket #{ticket_code} submitted successfully. Our admin team will respond shortly.', 'success')
    return redirect(url_for('requests.index', tab='admin_requests'))


@requests_bp.route('/transport/create', methods=['POST'])
@login_required
def create_transport_booking():
    user = g.user
    pickup_address = request.form.get('pickup_address', '').strip()
    drop_address = request.form.get('drop_address', '').strip()
    produce_type = request.form.get('produce_type', 'Farm Harvest').strip()
    quantity_quintals = float(request.form.get('quantity_quintals', 10.0) or 10.0)
    vehicle_type = request.form.get('vehicle_type', 'Mini Truck (Tata Ace)').strip()
    scheduled_datetime = request.form.get('scheduled_datetime', '').strip()
    order_id = request.form.get('order_id')

    if not pickup_address or not drop_address:
        flash('Pickup and drop-off addresses are required for transport booking.', 'danger')
        return redirect(url_for('requests.index', tab='transport'))

    pickup_lat = request.form.get('pickup_latitude', type=float)
    pickup_lon = request.form.get('pickup_longitude', type=float)
    is_shared_pooling = 'is_shared_pooling' in request.form

    # Calculate estimated cost based on quantity and vehicle type
    base_rate = 800.0
    if '10-Ton' in vehicle_type or 'Medium' in vehicle_type:
        base_rate = 2800.0
    elif 'Refrigerated' in vehicle_type:
        base_rate = 3500.0
    elif 'Pickup' in vehicle_type:
        base_rate = 1400.0

    est_cost = base_rate + (quantity_quintals * 35.0)
    pool_code = None
    if is_shared_pooling:
        est_cost *= 0.65 # 35% savings from load consolidation
        pool_code = f"POOL-2026-{random.randint(100, 999)}"

    booking_code = f"TRP-2026-{random.randint(1000, 9999)}"

    booking = TransportBooking(
        booking_code=booking_code,
        user_id=user.id,
        order_id=int(order_id) if order_id and order_id.isdigit() else None,
        pickup_address=pickup_address,
        drop_address=drop_address,
        pickup_latitude=pickup_lat,
        pickup_longitude=pickup_lon,
        produce_type=produce_type,
        quantity_quintals=quantity_quintals,
        vehicle_type=vehicle_type,
        scheduled_datetime=scheduled_datetime or datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
        transport_partner='Gramin Express Logistics',
        driver_name='Ramesh Shinde (Assigned)',
        driver_phone='+91 98231 44556',
        vehicle_number='MH-15-EG-4402',
        estimated_cost=round(est_cost, 2),
        is_shared_pooling=is_shared_pooling,
        pool_code=pool_code,
        status='driver_assigned',
        tracking_notes='Shared pooling vehicle assigned. 35% freight cost saved.' if is_shared_pooling else 'Dedicated vehicle allocated and driver verified. Pre-pickup call scheduled.'
    )
    db.session.add(booking)

    notif = Notification(
        user_id=user.id,
        title="Transport Booking Confirmed",
        message=f"Transport booking #{booking_code} confirmed with driver Ramesh Shinde (+91 98231 44556).",
        link_url=url_for('requests.index', tab='transport')
    )
    db.session.add(notif)
    db.session.commit()

    flash(f'Transport request #{booking_code} registered! Driver assigned successfully.', 'success')
    return redirect(url_for('requests.index', tab='transport'))


@requests_bp.route('/cold-storage/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_cold_storage_booking(booking_id):
    user = g.user
    booking = ColdStorageBooking.query.filter_by(id=booking_id, farmer_id=user.id).first_or_404()
    if booking.status in ['requested', 'confirmed']:
        booking.status = 'cancelled'
        db.session.commit()
        flash('Cold storage booking request cancelled.', 'info')
    else:
        flash('Cannot cancel a booking that is currently in storage or already processed.', 'warning')
    return redirect(url_for('requests.index', tab='cold_storage'))


@requests_bp.route('/transport/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_transport_booking(booking_id):
    user = g.user
    booking = TransportBooking.query.filter_by(id=booking_id, user_id=user.id).first_or_404()
    if booking.status != 'completed':
        booking.status = 'cancelled'
        db.session.commit()
        flash(f'Transport booking #{booking.booking_code} has been cancelled.', 'info')
    else:
        flash('Cannot cancel an already completed transport order.', 'warning')
    return redirect(url_for('requests.index', tab='transport'))


@requests_bp.route('/admin-ticket/close/<int:ticket_id>', methods=['POST'])
@login_required
def close_admin_ticket(ticket_id):
    user = g.user
    ticket = AdminTicket.query.filter_by(id=ticket_id, user_id=user.id).first_or_404()
    ticket.status = 'closed'
    db.session.commit()
    flash(f'Support ticket #{ticket.ticket_code} marked as closed.', 'info')
    return redirect(url_for('requests.index', tab='admin_requests'))
