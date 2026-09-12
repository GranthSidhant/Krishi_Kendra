import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
from werkzeug.utils import secure_filename
from app.routes.auth import farmer_required
from app.models import Inventory, Requirement, Offer, Order, Delivery, MandiRate, Product, Category, Notification, ChatThread, Message
from app.extensions import db
from app.services.deal_analysis_service import DealAnalysisService
from app.services.mandi_service import MandiService
from app.services.notification_service import NotificationService

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route('/dashboard')
@farmer_required
def dashboard():
    user = g.user
    inventories = Inventory.query.filter_by(farmer_id=user.id).all()
    
    # Calculate summary metrics
    total_inventory_kg = 0.0
    for item in inventories:
        qty = item.available_quantity
        if item.unit.lower() == 'quintal':
            qty *= 100
        elif item.unit.lower() == 'ton':
            qty *= 1000
        total_inventory_kg += qty
        
    active_orders = Order.query.filter_by(farmer_id=user.id).filter(Order.status.in_(['confirmed', 'processing', 'transport_assigned', 'in_transit'])).all()
    completed_orders = Order.query.filter_by(farmer_id=user.id, status='completed').all()
    
    total_sales_amount = sum(o.total_amount for o in completed_orders)
    pending_payments_amount = sum(o.total_amount for o in active_orders if o.payment_status in ['pending', 'in_escrow'])
    
    # Recent incoming buyer offers / requests
    recent_offers = Offer.query.filter_by(farmer_id=user.id).order_by(Offer.created_at.desc()).limit(5).all()
    
    # Recent Mandi rates for farmer's crops
    mandi_rates = MandiRate.query.filter_by(district=user.farmer_profile.district if user.farmer_profile else 'Nashik').limit(6).all()
    if not mandi_rates:
        mandi_rates = MandiRate.query.limit(6).all()

    return render_template(
        'farmer/dashboard.html',
        user=user,
        inventories=inventories,
        total_inventory_kg=round(total_inventory_kg, 1),
        active_orders=active_orders,
        active_orders_count=len(active_orders),
        total_sales_amount=round(total_sales_amount, 2),
        pending_payments_amount=round(pending_payments_amount, 2),
        recent_offers=recent_offers,
        mandi_rates=mandi_rates
    )


@farmer_bp.route('/inventory')
@farmer_required
def inventory():
    user = g.user
    items = Inventory.query.filter_by(farmer_id=user.id).order_by(Inventory.created_at.desc()).all()
    return render_template('farmer/inventory.html', items=items, user=user)


@farmer_bp.route('/inventory/add', methods=['GET', 'POST'])
@farmer_required
def add_produce():
    user = g.user
    categories = Category.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True).all()

    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        category_name = request.form.get('category_name', 'Vegetables')
        available_quantity = float(request.form.get('available_quantity', 100))
        unit = request.form.get('unit', 'kg')
        expected_price = float(request.form.get('expected_price_per_unit', 20))
        quality_grade = request.form.get('quality_grade', 'Grade A')
        harvest_date = request.form.get('harvest_date', '')
        description = request.form.get('description', '')
        district = user.farmer_profile.district if user.farmer_profile else 'Nashik'
        state = user.farmer_profile.state if user.farmer_profile else 'Maharashtra'

        image_url = 'crop_default.jpg'
        if 'produce_image_file' in request.files:
            file = request.files['produce_image_file']
            if file and file.filename != '':
                filename = secure_filename(f"CROP_{user.custom_id}_{file.filename}")
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_url = filename

        item = Inventory(
            farmer_id=user.id,
            product_name=product_name,
            category_name=category_name,
            available_quantity=available_quantity,
            unit=unit,
            expected_price_per_unit=expected_price,
            quality_grade=quality_grade,
            harvest_date=harvest_date,
            location_district=district,
            location_state=state,
            description=description,
            image_url=image_url,
            status='available'
        )
        db.session.add(item)
        db.session.commit()
        flash(f'Added {available_quantity} {unit} of {product_name} to your inventory!', 'success')
        return redirect(url_for('farmer.inventory'))

    return render_template('farmer/add_produce.html', categories=categories, products=products)


@farmer_bp.route('/inventory/edit/<int:item_id>', methods=['GET', 'POST'])
@farmer_required
def edit_inventory(item_id):
    user = g.user
    item = Inventory.query.filter_by(id=item_id, farmer_id=user.id).first_or_404()

    if request.method == 'POST':
        item.product_name = request.form.get('product_name', item.product_name).strip()
        item.available_quantity = float(request.form.get('available_quantity', item.available_quantity))
        item.unit = request.form.get('unit', item.unit)
        item.expected_price_per_unit = float(request.form.get('expected_price_per_unit', item.expected_price_per_unit))
        item.quality_grade = request.form.get('quality_grade', item.quality_grade)
        item.status = request.form.get('status', item.status)
        item.description = request.form.get('description', item.description)

        if 'produce_image_file' in request.files:
            file = request.files['produce_image_file']
            if file and file.filename != '':
                filename = secure_filename(f"CROP_{user.custom_id}_{file.filename}")
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                item.image_url = filename

        db.session.commit()
        flash('Inventory updated successfully!', 'success')
        return redirect(url_for('farmer.inventory'))

    return render_template('farmer/edit_inventory.html', item=item)


@farmer_bp.route('/inventory/delete/<int:item_id>', methods=['POST'])
@farmer_required
def delete_inventory(item_id):
    user = g.user
    item = Inventory.query.filter_by(id=item_id, farmer_id=user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Produce removed from inventory.', 'info')
    return redirect(url_for('farmer.inventory'))


@farmer_bp.route('/orders')
@farmer_required
def orders():
    user = g.user
    incoming_offers = Offer.query.filter_by(farmer_id=user.id).order_by(Offer.created_at.desc()).all()
    confirmed_orders = Order.query.filter_by(farmer_id=user.id).order_by(Order.created_at.desc()).all()

    # Pre-calculate deal analysis for each incoming offer
    offer_analyses = {}
    for offer in incoming_offers:
        district = user.farmer_profile.district if user.farmer_profile else 'Nashik'
        analysis = DealAnalysisService.analyze_offer(
            commodity_name=offer.product_name,
            offered_price_per_unit=offer.offered_price_per_unit if offer.status != 'countered' else (offer.counter_price_per_unit or offer.offered_price_per_unit),
            unit=offer.unit,
            district=district
        )
        offer_analyses[offer.id] = analysis

    return render_template(
        'farmer/orders.html',
        incoming_offers=incoming_offers,
        confirmed_orders=confirmed_orders,
        offer_analyses=offer_analyses
    )


@farmer_bp.route('/offer/<int:offer_id>/respond', methods=['POST'])
@farmer_required
def respond_offer(offer_id):
    user = g.user
    offer = Offer.query.filter_by(id=offer_id, farmer_id=user.id).first_or_404()
    action = request.form.get('action') # 'accept', 'reject', 'counter'

    effective_price = offer.counter_price_per_unit if (offer.status == 'countered' and offer.counter_price_per_unit) else offer.offered_price_per_unit
    effective_qty = offer.counter_quantity if (offer.status == 'countered' and offer.counter_quantity) else offer.quantity
    effective_total = round(effective_price * effective_qty, 2)

    if action == 'accept':
        offer.status = 'accepted'
        offer.last_action_by = 'farmer'
        
        # Check if confirmed Order already exists
        order = Order.query.filter_by(offer_id=offer.id).first()
        if not order:
            from app.services.escrow_service import EscrowService
            order_code = EscrowService.generate_unique_order_code()
            buyer_profile = offer.buyer.buyer_profile
            delivery_addr = buyer_profile.address if (buyer_profile and buyer_profile.address) else "Buyer Warehouse, APMC Yard"
            
            order = Order(
                order_code=order_code,
                offer_id=offer.id,
                inventory_id=offer.inventory_id,
                buyer_id=offer.buyer_id,
                farmer_id=user.id,
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
                pickup_address=f"{user.farmer_profile.farm_location_name if user.farmer_profile else 'Farmer Farm'}, {user.farmer_profile.district if user.farmer_profile else ''}",
                drop_address=delivery_addr,
                vehicle_type='Mini Truck (Tata Ace)',
                vehicle_category='mini_truck',
                pickup_otp=pickup_otp,
                delivery_otp=delivery_otp,
                current_status='assigned'
            )
            db.session.add(delivery)
            
            # Link order to chat thread if active
            chat_thread = ChatThread.query.filter_by(farmer_id=user.id, buyer_id=offer.buyer_id).first()
            if chat_thread:
                chat_thread.order_id = order.id
                status_msg = Message(
                    thread_id=chat_thread.id,
                    sender_id=user.id,
                    message_text=f"✅ Offer Accepted by Farmer! Confirmed Order #{order.order_code} generated for ₹{order.total_amount:,.2f}.",
                    message_type='text'
                )
                db.session.add(status_msg)

            # Notify buyer
            NotificationService.send(
                user_id=offer.buyer_id,
                title='Order Accepted by Farmer!',
                message=f"Farmer {user.name} accepted your offer for {effective_qty} {offer.unit} of {offer.product_name}. Order #{order.order_code} is confirmed.",
                link_url=url_for('orders.view_order', order_id=order.id)
            )
            db.session.commit()
            flash(f'Offer accepted! Order #{order.order_code} is now confirmed.', 'success')

        return redirect(url_for('orders.view_order', order_id=order.id))

    elif action == 'reject':
        offer.status = 'rejected'
        offer.last_action_by = 'farmer'
        NotificationService.send(
            user_id=offer.buyer_id,
            title='Offer Declined',
            message=f"Farmer {user.name} declined your offer for {offer.product_name}.",
            link_url=url_for('buyer.orders')
        )
        db.session.commit()
        flash('Offer rejected.', 'info')

    elif action == 'counter':
        counter_price = float(request.form.get('counter_price_per_unit', effective_price))
        counter_qty = float(request.form.get('counter_quantity', effective_qty))
        counter_notes = request.form.get('counter_notes', '')

        offer.status = 'countered'
        offer.counter_price_per_unit = counter_price
        offer.counter_quantity = counter_qty
        offer.counter_notes = counter_notes
        offer.last_action_by = 'farmer'
        offer.total_amount = round(counter_price * counter_qty, 2)

        # Notify buyer
        NotificationService.send(
            user_id=offer.buyer_id,
            title='Farmer Sent a Counter-Offer!',
            message=f"Farmer {user.name} sent a counter-offer for {offer.product_name}: ₹{counter_price}/{offer.unit} for {counter_qty} {offer.unit}.",
            link_url=url_for('buyer.orders')
        )
        db.session.commit()
        flash('Counter-offer sent to buyer successfully!', 'success')

    return redirect(url_for('farmer.orders'))


@farmer_bp.route('/requirements/<int:req_id>/quote', methods=['POST'])
@farmer_required
def submit_requirement_quote(req_id):
    import json
    user = g.user
    req = Requirement.query.get_or_404(req_id)

    price = float(request.form.get('offered_price', req.target_price_per_unit or 0))
    qty = float(request.form.get('quantity', req.required_quantity))
    unit = req.unit
    inventory_id = request.form.get('inventory_id', type=int)
    notes = request.form.get('notes', '').strip()

    if price <= 0 or qty <= 0:
        flash('Please enter a valid quotation price and quantity.', 'danger')
        return redirect(url_for('farmer.browse_requirements'))

    total_amount = round(price * qty, 2)

    # 1. Create Formal Offer
    offer = Offer(
        requirement_id=req.id,
        inventory_id=inventory_id if inventory_id else None,
        buyer_id=req.buyer_id,
        farmer_id=user.id,
        product_name=req.product_name,
        quantity=qty,
        unit=unit,
        offered_price_per_unit=price,
        total_amount=total_amount,
        offered_by_role='farmer',
        status='pending',
        last_action_by='farmer',
        notes=notes
    )
    db.session.add(offer)
    db.session.flush()

    # 2. Find or Create ChatThread
    thread = ChatThread.query.filter_by(farmer_id=user.id, buyer_id=req.buyer_id).first()
    if not thread:
        thread = ChatThread(
            farmer_id=user.id,
            buyer_id=req.buyer_id,
            offer_id=offer.id,
            requirement_id=req.id,
            subject_product=f"{req.product_name} Procurement"
        )
        db.session.add(thread)
        db.session.flush()
    else:
        thread.offer_id = offer.id
        thread.requirement_id = req.id

    # 3. Post structured offer card message in chat
    metadata = {
        'offer_id': offer.id,
        'requirement_id': req.id,
        'product_name': req.product_name,
        'price': price,
        'quantity': qty,
        'unit': unit,
        'total_amount': total_amount,
        'notes': notes,
        'offered_by': user.name,
        'role': 'farmer',
        'status': 'pending'
    }

    msg = Message(
        thread_id=thread.id,
        sender_id=user.id,
        message_text=f"Formal Quotation for Requirement: ₹{price}/{unit} for {qty} {unit} of {req.product_name} (Total ₹{total_amount:,.2f})",
        message_type='counter_card',
        metadata_json=json.dumps(metadata)
    )
    thread.last_message_at = datetime.utcnow()
    db.session.add(msg)

    # 4. Notify Buyer
    NotificationService.send(
        user_id=req.buyer_id,
        title=f"New Quotation from Farmer {user.name}!",
        message=f"Farmer {user.name} offered ₹{price}/{unit} for your {req.product_name} demand. View & accept deal in chat.",
        link_url=url_for('chat.view_thread', thread_id=thread.id)
    )
    db.session.commit()

    flash(f"Quotation of ₹{price}/{unit} submitted to {req.buyer.name}! You can now negotiate or finalize terms in chat.", "success")
    return redirect(url_for('chat.view_thread', thread_id=thread.id))


@farmer_bp.route('/mandi-rates')
@farmer_required
def mandi_rates():
    user = g.user
    district_filter = request.args.get('district', '')
    commodity_filter = request.args.get('commodity', '')

    rates = MandiService.get_latest_rates(district=district_filter, commodity=commodity_filter, limit=40)
    all_districts = db.session.query(MandiRate.district).distinct().all()
    all_districts = [d[0] for d in all_districts if d[0]]

    return render_template(
        'farmer/mandi_rates.html',
        rates=rates,
        districts=all_districts,
        selected_district=district_filter,
        selected_commodity=commodity_filter
    )


@farmer_bp.route('/visiting-card')
@farmer_required
def visiting_card():
    user = g.user
    profile = user.farmer_profile
    return render_template('farmer/visiting_card.html', user=user, profile=profile)


@farmer_bp.route('/logistics')
@farmer_required
def logistics():
    user = g.user
    active_orders = Order.query.filter_by(farmer_id=user.id).all()
    return render_template('farmer/logistics.html', user=user, orders=active_orders)


# ----------------------------------------------------
# Farmer Profit, Cost & ROI Calculator
# ----------------------------------------------------
@farmer_bp.route('/profit-calculator')
@farmer_required
def profit_calculator():
    user = g.user
    profile = user.farmer_profile
    return render_template('farmer/profit_calculator.html', user=user, profile=profile)


# ----------------------------------------------------
# Browse Buyer Requirements & Advance Pre-Orders
# ----------------------------------------------------
@farmer_bp.route('/requirements')
@farmer_required
def browse_requirements():
    user = g.user
    filter_type = request.args.get('filter', 'all') # 'all', 'pre_order', 'immediate'
    commodity = request.args.get('commodity', '').strip()
    
    query = Requirement.query.filter_by(status='open')
    if filter_type == 'pre_order':
        query = query.filter_by(is_pre_order=True)
    elif filter_type == 'immediate':
        query = query.filter_by(is_pre_order=False)
        
    if commodity:
        query = query.filter(Requirement.product_name.ilike(f"%{commodity}%"))
        
    requirements = query.order_by(Requirement.created_at.desc()).all()
    pre_order_count = Requirement.query.filter_by(status='open', is_pre_order=True).count()
    inventories = Inventory.query.filter_by(farmer_id=user.id, status='available').all()

    return render_template(
        'farmer/browse_requirements.html',
        user=user,
        requirements=requirements,
        filter_type=filter_type,
        commodity=commodity,
        pre_order_count=pre_order_count,
        inventories=inventories
    )


# ----------------------------------------------------
# AI Crop Health Doctor & Disease Diagnostic Scanner
# ----------------------------------------------------
@farmer_bp.route('/crop-doctor')
def crop_doctor():
    user = g.user
    return render_template('farmer/crop_doctor.html', user=user)


