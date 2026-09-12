from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.routes.auth import buyer_required
from app.models import Inventory, Requirement, Offer, Order, Delivery, MandiRate, Product, User, Notification, ChatThread, Message
from app.extensions import db
from app.services.matching_service import MatchingService
from app.services.mandi_service import MandiService
from app.services.notification_service import NotificationService

buyer_bp = Blueprint('buyer', __name__)

@buyer_bp.route('/dashboard')
@buyer_required
def dashboard():
    user = g.user
    active_orders = Order.query.filter_by(buyer_id=user.id).filter(Order.status.in_(['confirmed', 'processing', 'transport_assigned', 'in_transit'])).all()
    in_delivery_orders = [o for o in active_orders if o.status in ['transport_assigned', 'in_transit']]
    
    my_requirements = Requirement.query.filter_by(buyer_id=user.id).order_by(Requirement.created_at.desc()).limit(5).all()
    pending_offers = Offer.query.filter_by(buyer_id=user.id, status='pending').all()
    counter_offers = Offer.query.filter_by(buyer_id=user.id, status='countered', last_action_by='farmer').all()
    
    # Recent available produce from verified farmers
    recent_produce = Inventory.query.filter_by(status='available').filter(Inventory.available_quantity > 0).order_by(Inventory.created_at.desc()).limit(6).all()

    return render_template(
        'buyer/dashboard.html',
        user=user,
        active_orders=active_orders,
        active_orders_count=len(active_orders),
        in_delivery_count=len(in_delivery_orders),
        pending_responses_count=len(pending_offers) + len(counter_offers),
        pending_counter_offers=counter_offers,
        my_requirements=my_requirements,
        recent_produce=recent_produce
    )


@buyer_bp.route('/browse')
@buyer_required
def browse():
    user = g.user
    query_crop = request.args.get('q', '').strip()
    category_filter = request.args.get('category', '')
    district_filter = request.args.get('district', '')
    min_qty = request.args.get('min_qty', type=float)

    query = Inventory.query.filter_by(status='available').filter(Inventory.available_quantity > 0)
    if query_crop:
        query = query.filter(Inventory.product_name.ilike(f"%{query_crop}%"))
    if category_filter and category_filter != 'All':
        query = query.filter(Inventory.category_name.ilike(f"%{category_filter}%"))
    if district_filter and district_filter != 'All':
        query = query.filter(Inventory.location_district.ilike(f"%{district_filter}%"))
    if min_qty:
        query = query.filter(Inventory.available_quantity >= min_qty)

    produce_items = query.order_by(Inventory.created_at.desc()).all()
    districts = db.session.query(Inventory.location_district).distinct().all()
    districts = [d[0] for d in districts if d[0]]

    return render_template(
        'buyer/browse.html',
        user=user,
        produce_items=produce_items,
        districts=districts,
        query_crop=query_crop,
        category_filter=category_filter,
        district_filter=district_filter
    )


@buyer_bp.route('/direct-request/<int:inventory_id>', methods=['POST'])
@buyer_required
def direct_request(inventory_id):
    user = g.user
    inventory = Inventory.query.get_or_404(inventory_id)
    
    qty = float(request.form.get('quantity', 100))
    offered_price = float(request.form.get('offered_price_per_unit', inventory.expected_price_per_unit))
    unit = request.form.get('unit', inventory.unit)
    notes = request.form.get('notes', '')

    if qty > inventory.available_quantity:
        flash(f'Requested quantity ({qty} {unit}) exceeds available stock ({inventory.available_quantity} {unit}). You may offer for up to {inventory.available_quantity} {unit}.', 'warning')
        return redirect(url_for('buyer.browse'))

    total = round(qty * offered_price, 2)
    offer = Offer(
        inventory_id=inventory.id,
        buyer_id=user.id,
        farmer_id=inventory.farmer_id,
        product_name=inventory.product_name,
        quantity=qty,
        unit=unit,
        offered_price_per_unit=offered_price,
        total_amount=total,
        offered_by_role='buyer',
        status='pending',
        last_action_by='buyer',
        notes=notes
    )
    db.session.add(offer)
    db.session.flush()

    # Notify farmer
    NotificationService.send(
        user_id=inventory.farmer_id,
        title='New Direct Buy Request!',
        message=f"Buyer {user.name} sent a direct purchase offer of ₹{offered_price}/{unit} for {qty} {unit} of {inventory.product_name}.",
        link_url=url_for('farmer.orders')
    )
    db.session.commit()
    flash(f'Direct purchase request sent to {inventory.farmer.name} for {qty} {unit} of {inventory.product_name}!', 'success')
    return redirect(url_for('buyer.orders'))


@buyer_bp.route('/post-requirement', methods=['GET', 'POST'])
@buyer_required
def post_requirement():
    user = g.user
    products = Product.query.filter_by(is_active=True).all()

    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        required_quantity = float(request.form.get('required_quantity', 500))
        unit = request.form.get('unit', 'kg')
        required_quality = request.form.get('required_quality', 'Grade A')
        target_price = request.form.get('target_price_per_unit')
        target_price = float(target_price) if target_price else None
        
        delivery_location = request.form.get('delivery_location', user.buyer_profile.address if user.buyer_profile else '')
        delivery_district = request.form.get('delivery_district', user.buyer_profile.district if user.buyer_profile else 'Mumbai')
        delivery_state = request.form.get('delivery_state', 'Maharashtra')
        required_by_date = request.form.get('required_by_date', '')
        additional_notes = request.form.get('additional_notes', '')

        is_pre_order = 'is_pre_order' in request.form
        target_harvest_timeline = request.form.get('target_harvest_timeline', '').strip()
        advance_payment_terms = request.form.get('advance_payment_terms', '20% Advance on Sowing, 80% on Mandi Delivery').strip()

        req = Requirement(
            buyer_id=user.id,
            product_name=product_name,
            required_quantity=required_quantity,
            unit=unit,
            required_quality=required_quality,
            target_price_per_unit=target_price,
            delivery_location=delivery_location,
            delivery_district=delivery_district,
            delivery_state=delivery_state,
            required_by_date=required_by_date,
            additional_notes=additional_notes,
            is_pre_order=is_pre_order,
            target_harvest_timeline=target_harvest_timeline,
            advance_payment_terms=advance_payment_terms,
            status='open'
        )
        db.session.add(req)
        db.session.flush()

        # Run Matching Engine to find eligible farmers
        matches = MatchingService.find_matching_farmers_for_requirement(req)
        notified_count = 0
        for match in matches[:5]: # Notify top 5 matching farmers
            farmer = match['farmer']
            NotificationService.send(
                user_id=farmer.id,
                title='New Matching Buyer Requirement!',
                message=f"Buyer {user.name} requires {required_quantity} {unit} of {product_name} in {delivery_district}. Submit an offer now!",
                link_url=url_for('farmer.orders')
            )
            notified_count += 1

        db.session.commit()
        flash(f'Requirement posted successfully! {notified_count} matching farmers have been notified directly.', 'success')
        return redirect(url_for('buyer.responses', req_id=req.id))

    return render_template('buyer/post_requirement.html', user=user, products=products)


@buyer_bp.route('/responses/<int:req_id>')
@buyer_required
def responses(req_id):
    user = g.user
    req = Requirement.query.filter_by(id=req_id, buyer_id=user.id).first_or_404()
    
    # Potential matching farmers calculated dynamically
    matches = MatchingService.find_matching_farmers_for_requirement(req)
    
    # Direct offers submitted by farmers for this requirement
    received_offers = Offer.query.filter_by(requirement_id=req.id).all()

    # Get Mandi benchmark rate for comparison table
    mandi_info = MandiService.get_rate_for_commodity(req.product_name, req.delivery_district)

    return render_template(
        'buyer/responses.html',
        user=user,
        requirement=req,
        matches=matches,
        received_offers=received_offers,
        mandi_info=mandi_info
    )


@buyer_bp.route('/orders')
@buyer_required
def orders():
    user = g.user
    my_orders = Order.query.filter_by(buyer_id=user.id).order_by(Order.created_at.desc()).all()
    my_offers = Offer.query.filter_by(buyer_id=user.id).order_by(Offer.created_at.desc()).all()

    # Rule 16: Total historical spend is calculated and displayed here inside Order History
    completed_orders = [o for o in my_orders if o.status == 'completed']
    total_historical_spend = sum(o.total_amount for o in completed_orders)

    return render_template(
        'buyer/orders.html',
        user=user,
        orders=my_orders,
        offers=my_offers,
        total_historical_spend=round(total_historical_spend, 2)
    )


@buyer_bp.route('/offer/<int:offer_id>/respond', methods=['POST'])
@buyer_required
def respond_offer(offer_id):
    user = g.user
    offer = Offer.query.filter_by(id=offer_id, buyer_id=user.id).first_or_404()
    action = request.form.get('action')  # 'accept', 'reject', 'counter'

    effective_price = offer.counter_price_per_unit if (offer.status == 'countered' and offer.counter_price_per_unit) else offer.offered_price_per_unit
    effective_qty = offer.counter_quantity if (offer.status == 'countered' and offer.counter_quantity) else offer.quantity
    effective_total = round(effective_price * effective_qty, 2)

    if action == 'accept':
        offer.status = 'accepted'
        offer.last_action_by = 'buyer'

        # Check if an Order already exists for this offer
        order = Order.query.filter_by(offer_id=offer.id).first()
        if not order:
            from app.services.escrow_service import EscrowService
            order_code = EscrowService.generate_unique_order_code()
            buyer_profile = user.buyer_profile
            delivery_addr = buyer_profile.address if (buyer_profile and buyer_profile.address) else "Buyer Warehouse, APMC Yard"

            order = Order(
                order_code=order_code,
                offer_id=offer.id,
                inventory_id=offer.inventory_id,
                buyer_id=user.id,
                farmer_id=offer.farmer_id,
                product_name=offer.product_name,
                quantity=effective_qty,
                unit=offer.unit,
                agreed_price_per_unit=effective_price,
                total_amount=effective_total,
                delivery_address=delivery_addr,
                status='confirmed',
                payment_status='in_escrow'
            )
            db.session.add(order)
            db.session.flush()

            from app.services.logistics_service import LogisticsService
            pickup_otp, delivery_otp = LogisticsService.generate_handover_otps()

            # Create Delivery record with Two-Step OTP
            delivery = Delivery(
                order_id=order.id,
                pickup_address=f"{offer.farmer.farmer_profile.farm_location_name if offer.farmer.farmer_profile else 'Farmer Farm'}, {offer.farmer.farmer_profile.district if offer.farmer.farmer_profile else ''}",
                drop_address=delivery_addr,
                vehicle_type='Mini Truck (Tata Ace)',
                vehicle_category='mini_truck',
                pickup_otp=pickup_otp,
                delivery_otp=delivery_otp,
                current_status='assigned'
            )
            db.session.add(delivery)

            # Link order to chat thread if active
            chat_thread = ChatThread.query.filter_by(farmer_id=offer.farmer_id, buyer_id=user.id).first()
            if chat_thread:
                chat_thread.order_id = order.id
                status_msg = Message(
                    thread_id=chat_thread.id,
                    sender_id=user.id,
                    message_text=f"✅ Deal Accepted by Buyer! Confirmed Order #{order.order_code} generated for ₹{order.total_amount:,.2f}.",
                    message_type='text'
                )
                db.session.add(status_msg)

            # Notify farmer
            NotificationService.send(
                user_id=offer.farmer_id,
                title='Counter-Offer Accepted by Buyer!',
                message=f"Buyer {user.name} accepted your price for {effective_qty} {offer.unit} of {offer.product_name}. Order #{order.order_code} is confirmed.",
                link_url=url_for('orders.view_order', order_id=order.id)
            )
            db.session.commit()
            flash(f'Offer accepted! Order #{order.order_code} has been created with guaranteed escrow.', 'success')

        return redirect(url_for('orders.view_order', order_id=order.id))

    elif action == 'reject':
        offer.status = 'rejected'
        offer.last_action_by = 'buyer'
        NotificationService.send(
            user_id=offer.farmer_id,
            title='Offer Declined',
            message=f"Buyer {user.name} declined the counter-offer for {offer.product_name}.",
            link_url=url_for('farmer.orders')
        )
        db.session.commit()
        flash('Offer declined.', 'info')

    elif action == 'counter':
        counter_price = float(request.form.get('counter_price_per_unit', effective_price))
        counter_qty = float(request.form.get('counter_quantity', effective_qty))
        counter_notes = request.form.get('counter_notes', '')

        offer.status = 'countered'
        offer.counter_price_per_unit = counter_price
        offer.counter_quantity = counter_qty
        offer.counter_notes = counter_notes
        offer.last_action_by = 'buyer'
        offer.total_amount = round(counter_price * counter_qty, 2)

        # Notify farmer
        NotificationService.send(
            user_id=offer.farmer_id,
            title='Buyer Sent a New Counter-Offer!',
            message=f"Buyer {user.name} counter-proposed ₹{counter_price}/{offer.unit} for {counter_qty} {offer.unit} of {offer.product_name}.",
            link_url=url_for('farmer.orders')
        )
        db.session.commit()
        flash('New counter-offer sent to farmer successfully!', 'success')

    return redirect(url_for('buyer.orders'))


@buyer_bp.route('/visiting-card')
@buyer_required
def visiting_card():
    user = g.user
    profile = user.buyer_profile
    return render_template('buyer/visiting_card.html', user=user, profile=profile)

