from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.routes.auth import admin_required
from app.models import User, Category, Product, ColdStorage, GovernmentScheme, Dispute, AuditLog, Order
from app.extensions import db
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    user = g.user
    total_farmers = User.query.filter_by(role='farmer').count()
    total_buyers = User.query.filter_by(role='buyer').count()
    pending_verifications = User.query.filter_by(verification_status='pending').count()
    open_disputes = Dispute.query.filter_by(status='open').count()
    active_orders = Order.query.filter(Order.status.in_(['confirmed', 'processing', 'transport_assigned', 'in_transit'])).count()
    total_cold_storages = ColdStorage.query.count()

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()
    pending_users = User.query.filter_by(verification_status='pending').limit(5).all()
    recent_disputes = Dispute.query.filter_by(status='open').limit(5).all()

    return render_template(
        'admin/dashboard.html',
        user=user,
        stats={
            'total_farmers': total_farmers,
            'total_buyers': total_buyers,
            'pending_verifications': pending_verifications,
            'open_disputes': open_disputes,
            'active_orders': active_orders,
            'total_cold_storages': total_cold_storages
        },
        recent_logs=recent_logs,
        pending_users=pending_users,
        recent_disputes=recent_disputes
    )


@admin_bp.route('/users')
@admin_required
def users():
    role_filter = request.args.get('role', '')
    query = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    all_users = query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users, role_filter=role_filter)


@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    target_user = User.query.get_or_404(user_id)
    target_user.is_active = not target_user.is_active
    db.session.commit()
    
    action_text = "RESTORED" if target_user.is_active else "SUSPENDED"
    AuditService.log(
        action=f"USER_{action_text}",
        admin_id=g.user.id,
        target_entity='User',
        target_id=target_user.id,
        details=f"Admin {g.user.name} {action_text.lower()} account for {target_user.name} ({target_user.custom_id})"
    )
    flash(f"Account for {target_user.name} has been {action_text.lower()}.", 'info')
    return redirect(url_for('admin.users'))


@admin_bp.route('/verifications')
@admin_required
def verifications():
    pending_list = User.query.filter_by(verification_status='pending').all()
    all_verified = User.query.filter_by(is_verified=True).all()
    return render_template('admin/verifications.html', pending_list=pending_list, all_verified=all_verified)


@admin_bp.route('/verifications/<int:user_id>/decide', methods=['POST'])
@admin_required
def decide_verification(user_id):
    target_user = User.query.get_or_404(user_id)
    decision = request.form.get('decision') # 'approve' or 'reject'
    reason = request.form.get('reason', '')

    if decision == 'approve':
        target_user.is_verified = True
        target_user.verification_status = 'approved'
        NotificationService.send(
            user_id=target_user.id,
            title='Account Verified! 🌟',
            message=f"Congratulations {target_user.name}! Your government ID verification was approved by the Agriculture Officer. You now have the Official Verified Badge.",
            link_url=url_for('auth.profile')
        )
        AuditService.log(
            action="VERIFICATION_APPROVED",
            admin_id=g.user.id,
            target_entity='User',
            target_id=target_user.id,
            details=f"Verification approved for {target_user.name} ({target_user.custom_id})"
        )
        flash(f"Verification approved for {target_user.name}. Verified badge awarded!", 'success')
    else:
        target_user.is_verified = False
        target_user.verification_status = 'rejected'
        target_user.verification_rejection_reason = reason
        NotificationService.send(
            user_id=target_user.id,
            title='Verification Update',
            message=f"Your verification request could not be approved. Reason: {reason or 'Document unclear'}. Please re-upload in Profile.",
            link_url=url_for('auth.profile')
        )
        AuditService.log(
            action="VERIFICATION_REJECTED",
            admin_id=g.user.id,
            target_entity='User',
            target_id=target_user.id,
            details=f"Verification rejected for {target_user.name}. Reason: {reason}"
        )
        flash(f"Verification rejected for {target_user.name}.", 'warning')

    db.session.commit()
    return redirect(url_for('admin.verifications'))


@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_category':
            name = request.form.get('name', '').strip()
            hindi_name = request.form.get('hindi_name', '').strip()
            icon = request.form.get('icon', 'fa-seedling')
            description = request.form.get('description', '')
            if name:
                cat = Category(name=name, hindi_name=hindi_name, icon=icon, description=description)
                db.session.add(cat)
                db.session.commit()
                AuditService.log("CATEGORY_ADDED", g.user.id, 'Category', cat.id, f"Added category {name}")
                flash(f"Category '{name}' added successfully!", 'success')
        elif action == 'add_product':
            category_id = int(request.form.get('category_id'))
            name = request.form.get('name', '').strip()
            hindi_name = request.form.get('hindi_name', '').strip()
            default_unit = request.form.get('default_unit', 'kg')
            est_rate = float(request.form.get('estimated_mandi_rate', 25.0))
            if name:
                prod = Product(category_id=category_id, name=name, hindi_name=hindi_name, default_unit=default_unit, estimated_mandi_rate=est_rate)
                db.session.add(prod)
                db.session.commit()
                AuditService.log("PRODUCT_ADDED", g.user.id, 'Product', prod.id, f"Added crop/product {name}")
                flash(f"Product '{name}' added successfully!", 'success')
        return redirect(url_for('admin.categories'))

    all_categories = Category.query.all()
    all_products = Product.query.all()
    return render_template('admin/categories.html', categories=all_categories, products=all_products)


@admin_bp.route('/cold-storage', methods=['GET', 'POST'])
@admin_required
def cold_storage():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        operator_name = request.form.get('operator_name', '')
        contact_phone = request.form.get('contact_phone', '')
        address = request.form.get('address', '')
        district = request.form.get('district', 'Nashik')
        state = request.form.get('state', 'Maharashtra')
        capacity = float(request.form.get('total_capacity_mt', 5000))
        avail = float(request.form.get('available_capacity_mt', 2000))
        charge = float(request.form.get('approx_charge_per_month_per_quintal', 60))
        temp = request.form.get('temp_range_celsius', '0°C to 4°C')
        produce = request.form.get('supported_produce', 'Potato, Onion, Apple')
        facilities = request.form.get('facilities', 'Solar Cold Backup, CCTV')

        cs = ColdStorage(
            name=name,
            operator_name=operator_name,
            contact_phone=contact_phone,
            address=address,
            district=district,
            state=state,
            total_capacity_mt=capacity,
            available_capacity_mt=avail,
            approx_charge_per_month_per_quintal=charge,
            temp_range_celsius=temp,
            supported_produce=produce,
            facilities=facilities,
            is_verified=True,
            is_active=True
        )
        db.session.add(cs)
        db.session.commit()
        AuditService.log("COLD_STORAGE_REGISTERED", g.user.id, 'ColdStorage', cs.id, f"Registered facility {name} in {district}")
        flash(f"Cold Storage facility '{name}' registered successfully!", 'success')
        return redirect(url_for('admin.cold_storage'))

    storages = ColdStorage.query.order_by(ColdStorage.created_at.desc()).all()
    return render_template('admin/cold_storage.html', storages=storages)


@admin_bp.route('/schemes', methods=['GET', 'POST'])
@admin_required
def schemes():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        hindi_title = request.form.get('hindi_title', '').strip()
        category = request.form.get('category', 'Subsidy')
        description = request.form.get('description', '')
        eligibility = request.form.get('eligibility_summary', '')
        benefits = request.form.get('benefits_summary', '')
        link = request.form.get('application_link', '')

        scheme = GovernmentScheme(
            title=title,
            hindi_title=hindi_title,
            category=category,
            description=description,
            eligibility_summary=eligibility,
            benefits_summary=benefits,
            application_link=link,
            is_featured=True,
            is_active=True
        )
        db.session.add(scheme)
        db.session.commit()
        AuditService.log("SCHEME_PUBLISHED", g.user.id, 'GovernmentScheme', scheme.id, f"Published scheme {title}")
        flash(f"Government Scheme '{title}' published on the farmer board!", 'success')
        return redirect(url_for('admin.schemes'))

    all_schemes = GovernmentScheme.query.order_by(GovernmentScheme.created_at.desc()).all()
    return render_template('admin/schemes.html', schemes=all_schemes)


@admin_bp.route('/disputes')
@admin_required
def disputes():
    all_disputes = Dispute.query.order_by(Dispute.created_at.desc()).all()
    return render_template('admin/disputes.html', disputes=all_disputes)


@admin_bp.route('/disputes/<int:dispute_id>/resolve', methods=['POST'])
@admin_required
def resolve_dispute(dispute_id):
    disp = Dispute.query.get_or_404(dispute_id)
    resolution = request.form.get('resolution_notes', '')
    status = request.form.get('status', 'resolved')

    disp.status = status
    disp.resolution_notes = resolution
    disp.resolved_by_admin_id = g.user.id
    disp.resolved_at = datetime.utcnow()

    NotificationService.send(
        user_id=disp.raised_by_id,
        title='Dispute Resolved by Officer',
        message=f"Your dispute regarding Order #{disp.order.order_code if disp.order else ''} was reviewed. Decision: {resolution}",
        link_url=url_for('orders.view_order', order_id=disp.order_id) if disp.order_id else '#'
    )
    AuditService.log("DISPUTE_RESOLVED", g.user.id, 'Dispute', disp.id, f"Resolved dispute #{disp.id} - Status: {status}")
    db.session.commit()
    flash('Dispute resolution recorded and notified to users.', 'success')
    return redirect(url_for('admin.disputes'))


from app.models import User, Category, Product, ColdStorage, GovernmentScheme, Dispute, AuditLog, Order, AdminTicket, ColdStorageBooking, TransportBooking

@admin_bp.route('/audit-logs')
@admin_required
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template('admin/audit_logs.html', logs=logs)


@admin_bp.route('/requests')
@admin_required
def requests_list():
    tickets = AdminTicket.query.order_by(AdminTicket.created_at.desc()).all()
    cold_bookings = ColdStorageBooking.query.order_by(ColdStorageBooking.created_at.desc()).all()
    transport_bookings = TransportBooking.query.order_by(TransportBooking.created_at.desc()).all()
    return render_template('admin/requests.html', tickets=tickets, cold_bookings=cold_bookings, transport_bookings=transport_bookings)


@admin_bp.route('/requests/tickets/<int:ticket_id>/respond', methods=['POST'])
@admin_required
def respond_ticket(ticket_id):
    ticket = AdminTicket.query.get_or_404(ticket_id)
    response_text = request.form.get('admin_response', '').strip()
    status = request.form.get('status', 'resolved')

    ticket.admin_response = response_text
    ticket.status = status
    ticket.resolved_by_admin_id = g.user.id
    ticket.resolved_at = datetime.utcnow()

    NotificationService.send(
        user_id=ticket.user_id,
        title=f"Admin Support Update: #{ticket.ticket_code}",
        message=f"Your ticket '{ticket.subject}' was updated by the Agriculture Officer: {response_text[:120]}...",
        link_url=url_for('requests.index', tab='admin_requests')
    )
    AuditService.log("ADMIN_TICKET_RESPONDED", g.user.id, 'AdminTicket', ticket.id, f"Responded to ticket #{ticket.ticket_code} - Status: {status}")
    db.session.commit()
    flash(f"Response logged for ticket #{ticket.ticket_code}.", 'success')
    return redirect(url_for('admin.requests_list'))


@admin_bp.route('/requests/cold-storage/<int:booking_id>/update-status', methods=['POST'])
@admin_required
def update_cold_storage_status(booking_id):
    booking = ColdStorageBooking.query.get_or_404(booking_id)
    new_status = request.form.get('status', 'confirmed')
    booking.status = new_status
    db.session.commit()
    flash(f"Cold Storage request #{booking.id} updated to {new_status}.", 'success')
    return redirect(url_for('admin.requests_list'))


@admin_bp.route('/requests/transport/<int:booking_id>/update-status', methods=['POST'])
@admin_required
def update_transport_status(booking_id):
    booking = TransportBooking.query.get_or_404(booking_id)
    new_status = request.form.get('status', 'driver_assigned')
    booking.status = new_status
    db.session.commit()
    flash(f"Transport booking #{booking.booking_code} updated to {new_status}.", 'success')
    return redirect(url_for('admin.requests_list'))

