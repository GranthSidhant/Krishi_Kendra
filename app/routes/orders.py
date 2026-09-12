from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.routes.auth import login_required
from app.models import Order, Delivery, Dispute, User, Inventory
from app.extensions import db
from app.services.notification_service import NotificationService
from app.services.escrow_service import EscrowService
from app.services.logistics_service import LogisticsService, VEHICLE_PROFILES
import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/<int:order_id>')
@login_required
def view_order(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)

    if user.id not in [order.farmer_id, order.buyer_id] and user.role != 'admin':
        flash('Unauthorized to view this order.', 'danger')
        return redirect(url_for('main.index'))

    delivery = order.delivery
    farmer_profile = order.farmer.farmer_profile
    buyer_profile = order.buyer.buyer_profile

    # Calculate freight options for UI preview
    vehicle_options = VEHICLE_PROFILES

    return render_template(
        'orders/detail.html',
        order=order,
        delivery=delivery,
        farmer_profile=farmer_profile,
        buyer_profile=buyer_profile,
        vehicle_options=vehicle_options,
        user=user
    )


@orders_bp.route('/<int:order_id>/pay-escrow', methods=['POST'])
@login_required
def pay_escrow(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)

    if user.id != order.buyer_id and user.role != 'admin':
        flash('Only the buyer can fund the escrow deposit.', 'danger')
        return redirect(url_for('orders.view_order', order_id=order.id))

    payment_method = request.form.get('payment_method', 'UPI_ESCROW')
    upi_id = request.form.get('upi_id', 'buyer@okaxis')

    result = EscrowService.process_escrow_payment(order.id, payment_method=payment_method, upi_id=upi_id)
    if result.get('success'):
        flash(f"Escrow payment of ₹{order.total_amount:,.2f} locked successfully! (Txn ID: {result.get('escrow_txn_id')})", 'success')
    else:
        flash(result.get('error', 'Failed to process escrow payment.'), 'danger')

    return redirect(url_for('orders.view_order', order_id=order.id))


@orders_bp.route('/<int:order_id>/assign-transport', methods=['POST'])
@login_required
def assign_transport(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)

    if user.id not in [order.farmer_id, order.buyer_id] and user.role != 'admin':
        flash('Unauthorized to assign transport.', 'danger')
        return redirect(url_for('orders.view_order', order_id=order.id))

    vehicle_category = request.form.get('vehicle_category', 'mini_truck')
    driver_name = request.form.get('driver_name', 'Ramesh Shinde').strip()
    driver_phone = request.form.get('driver_phone', '+91 98231 44556').strip()
    vehicle_number = request.form.get('vehicle_number', 'MH-15-EG-4402').strip().upper()
    distance_km = float(request.form.get('distance_km', 45.0))

    freight_info = LogisticsService.calculate_freight(vehicle_category, distance_km)

    if not order.delivery:
        pickup_otp, delivery_otp = LogisticsService.generate_handover_otps()
        delivery = Delivery(
            order_id=order.id,
            pickup_address=f"{order.farmer.farmer_profile.farm_location_name if order.farmer.farmer_profile else 'Farmer Farm'}, {order.farmer.farmer_profile.district if order.farmer.farmer_profile else ''}",
            drop_address=order.delivery_address,
            vehicle_type=freight_info['vehicle_name'],
            vehicle_category=vehicle_category,
            driver_name=driver_name,
            driver_phone=driver_phone,
            vehicle_number=vehicle_number,
            estimated_cost=freight_info['estimated_freight'],
            distance_km=distance_km,
            pickup_otp=pickup_otp,
            delivery_otp=delivery_otp,
            current_status='assigned'
        )
        db.session.add(delivery)
    else:
        delivery = order.delivery
        delivery.vehicle_type = freight_info['vehicle_name']
        delivery.vehicle_category = vehicle_category
        delivery.driver_name = driver_name
        delivery.driver_phone = driver_phone
        delivery.vehicle_number = vehicle_number
        delivery.estimated_cost = freight_info['estimated_freight']
        delivery.distance_km = distance_km
        if not delivery.pickup_otp:
            p_otp, d_otp = LogisticsService.generate_handover_otps()
            delivery.pickup_otp = p_otp
            delivery.delivery_otp = d_otp
        delivery.current_status = 'assigned'

    order.status = 'transport_assigned'
    db.session.commit()

    flash(f"Logistics assigned ({freight_info['vehicle_name']})! Pickup OTP sent to Farmer.", 'success')
    return redirect(url_for('orders.view_order', order_id=order.id))


@orders_bp.route('/<int:order_id>/verify-pickup-otp', methods=['POST'])
@login_required
def verify_pickup_otp(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)

    # Farmers hold the secret Pickup OTP; only the buyer, transporter, or admin verifies it
    if user.id == order.farmer_id and user.role != 'admin':
        flash('As the farmer/seller, please provide your Pickup OTP to the driver at loading rather than verifying it yourself.', 'warning')
        return redirect(url_for('orders.view_order', order_id=order.id))

    entered_otp = request.form.get('pickup_otp', '').strip()

    result = LogisticsService.verify_pickup_otp(order.id, entered_otp)
    if result.get('success'):
        flash(result['message'], 'success')
    else:
        flash(result.get('error', 'Invalid Pickup OTP.'), 'danger')

    return redirect(url_for('orders.view_order', order_id=order.id))


@orders_bp.route('/<int:order_id>/verify-delivery-otp', methods=['POST'])
@login_required
def verify_delivery_otp(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)

    # Buyers hold the secret Delivery OTP; only the farmer, transporter, or admin verifies it upon delivery handover
    if user.id == order.buyer_id and user.role != 'admin':
        flash('As the buyer, please share your Delivery OTP with the driver/farmer after inspection rather than verifying it yourself.', 'warning')
        return redirect(url_for('orders.view_order', order_id=order.id))

    entered_otp = request.form.get('delivery_otp', '').strip()

    result = LogisticsService.verify_delivery_otp(order.id, entered_otp)
    if result.get('success'):
        flash(result['message'], 'success')
    else:
        flash(result.get('error', 'Invalid Delivery OTP.'), 'danger')

    return redirect(url_for('orders.view_order', order_id=order.id))


@orders_bp.route('/<int:order_id>/rate', methods=['POST'])
@login_required
def rate_order(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)

    if user.id not in [order.farmer_id, order.buyer_id]:
        flash('Unauthorized to submit review.', 'danger')
        return redirect(url_for('orders.view_order', order_id=order.id))

    rating = int(request.form.get('rating', 5))
    review = request.form.get('review', '').strip()

    if user.id == order.buyer_id:
        order.buyer_rating = rating
        order.buyer_review = review
        flash('Thank you! Your rating for the farmer has been recorded.', 'success')
    else:
        order.farmer_rating = rating
        order.farmer_review = review
        flash('Thank you! Your rating for the buyer has been recorded.', 'success')

    db.session.commit()
    return redirect(url_for('orders.view_order', order_id=order.id))


@orders_bp.route('/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_status(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['confirmed', 'processing', 'transport_assigned', 'in_transit', 'delivered', 'completed']:
        order.status = new_status
        if new_status == 'delivered':
            EscrowService.release_escrow_payout(order.id)
        elif new_status == 'completed':
            order.payment_status = 'completed'

        if order.delivery:
            if new_status == 'transport_assigned':
                order.delivery.current_status = 'assigned'
            elif new_status == 'in_transit':
                order.delivery.current_status = 'in_transit'
            elif new_status in ['delivered', 'completed']:
                order.delivery.current_status = 'delivered'

        db.session.commit()
        flash(f'Order status updated to {new_status.replace("_", " ").title()}.', 'success')

    return redirect(url_for('orders.view_order', order_id=order.id))


@orders_bp.route('/<int:order_id>/invoice')
@login_required
def invoice(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('orders/invoice.html', order=order)


@orders_bp.route('/<int:order_id>/payout-receipt')
@login_required
def payout_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('orders/payout_receipt.html', order=order)


@orders_bp.route('/<int:order_id>/dispute', methods=['POST'])
@login_required
def file_dispute(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)
    against_id = order.buyer_id if user.id == order.farmer_id else order.farmer_id
    
    reason = request.form.get('reason', 'Quality / Delivery Mismatch')
    description = request.form.get('description', '')

    dispute = Dispute(
        order_id=order.id,
        raised_by_id=user.id,
        against_user_id=against_id,
        reason=reason,
        description=description,
        status='open'
    )
    db.session.add(dispute)
    db.session.commit()
    flash('Dispute registered. An Agriculture Officer / Admin will review the case.', 'info')
    return redirect(url_for('orders.view_order', order_id=order.id))
