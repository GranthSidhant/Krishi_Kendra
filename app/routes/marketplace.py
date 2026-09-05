from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required
from app.models import MarketplaceProduct, MarketplaceOrder
from app.extensions import db

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/')
def index():
    category_filter = request.args.get('category', '')
    query_text = request.args.get('q', '').strip()

    query = MarketplaceProduct.query.filter_by(is_available=True)
    if category_filter and category_filter != 'All':
        query = query.filter_by(category=category_filter)
    if query_text:
        query = query.filter(MarketplaceProduct.title.ilike(f"%{query_text}%"))

    products = query.all()
    categories = ['Seeds', 'Fertilizers', 'Equipment', 'Irrigation', 'Crop Protection']

    my_orders = []
    if g.user:
        my_orders = MarketplaceOrder.query.filter_by(farmer_id=g.user.id).order_by(MarketplaceOrder.created_at.desc()).all()

    return render_template(
        'marketplace/index.html',
        products=products,
        categories=categories,
        selected_category=category_filter,
        query_text=query_text,
        my_orders=my_orders
    )


@marketplace_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = MarketplaceProduct.query.get_or_404(product_id)
    return render_template('marketplace/product_detail.html', product=product)


@marketplace_bp.route('/buy/<int:product_id>', methods=['POST'])
@login_required
def buy_product(product_id):
    product = MarketplaceProduct.query.get_or_404(product_id)
    qty = int(request.form.get('quantity', 1))
    address = request.form.get('delivery_address', g.user.farmer_profile.address if g.user.farmer_profile else 'Farmer Farm Address')

    total = round(product.price * qty, 2)
    order = MarketplaceOrder(
        farmer_id=g.user.id,
        product_id=product.id,
        product_title=product.title,
        quantity=qty,
        unit_price=product.price,
        total_amount=total,
        delivery_address=address,
        status='confirmed'
    )
    db.session.add(order)
    db.session.commit()
    flash(f'Order placed successfully for {qty} x {product.title} (₹{total}). Dispatched soon!', 'success')
    return redirect(url_for('marketplace.index'))
