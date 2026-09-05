from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required
from app.models import Order, Delivery, Dispute, User
from app.extensions import db
from app.services.notification_service import NotificationService

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

    return render_template(
        'orders/detail.html',
        order=order,
        delivery=delivery,
        farmer_profile=farmer_profile,
        buyer_profile=buyer_profile,
        user=user
    )


@orders_bp.route('/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_status(order_id):
    user = g.user
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['processing', 'transport_assigned', 'in_transit', 'delivered', 'completed']:
        order.status = new_status
        if new_status == 'delivered':
            order.payment_status = 'released'
            NotificationService.send(
                user_id=order.farmer_id,
                title='Order Delivered & Payment Released!',
                message=f"Order #{order.order_code} was marked as delivered. ₹{order.total_amount} released to your account.",
                link_url=url_for('orders.view_order', order_id=order.id)
            )
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
