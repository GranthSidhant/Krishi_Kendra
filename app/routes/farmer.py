import os
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

    if action == 'accept':
        offer.status = 'accepted'
        offer.last_action_by = 'farmer'
        
        # Create confirmed Order
        order_code = f"ORD-2026-{offer.id + 8000}"
        buyer_profile = offer.buyer.buyer_profile
        delivery_addr = buyer_profile.address if (buyer_profile and buyer_profile.address) else "Buyer Warehouse, APMC Yard"
        
        order = Order(
            order_code=order_code,
            offer_id=offer.id,
            buyer_id=offer.buyer_id,
            farmer_id=user.id,
            product_name=offer.product_name,
            quantity=offer.quantity,
            unit=offer.unit,
            agreed_price_per_unit=offer.offered_price_per_unit,
            total_amount=offer.total_amount,
            delivery_address=delivery_addr,
            status='confirmed',
            payment_status='in_escrow'
        )
        db.session.add(order)
        db.session.flush()

        # Create Delivery record
        delivery = Delivery(
            order_id=order.id,
            pickup_address=f"{user.farmer_profile.farm_location_name}, {user.farmer_profile.district}",
            drop_address=delivery_addr,
            vehicle_type='Mini Truck (Tata Ace)',
            current_status='assigned'
        )
        db.session.add(delivery)
        
        # Notify buyer
        NotificationService.send(
            user_id=offer.buyer_id,
            title='Order Accepted by Farmer!',
            message=f"Farmer {user.name} accepted your offer for {offer.quantity} {offer.unit} of {offer.product_name}. Order #{order.order_code} is confirmed.",
            link_url=url_for('orders.view_order', order_id=order.id)
        )
        db.session.commit()
        flash(f'Offer accepted! Order #{order.order_code} is now confirmed.', 'success')

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
        counter_price = float(request.form.get('counter_price_per_unit', offer.offered_price_per_unit))
        counter_qty = float(request.form.get('counter_quantity', offer.quantity))
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

    return render_template(
        'farmer/browse_requirements.html',
        user=user,
        requirements=requirements,
        filter_type=filter_type,
        commodity=commodity,
        pre_order_count=pre_order_count
    )

