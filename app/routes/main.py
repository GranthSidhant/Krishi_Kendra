from flask import Blueprint, render_template, request, session, redirect, url_for, g, flash, jsonify
from app.models import Product, MandiRate, ColdStorage, GovernmentScheme, User, FarmerProfile, BuyerProfile, Notification
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch sample featured data for landing page
    featured_crops = Product.query.filter_by(is_active=True).limit(6).all()
    latest_mandi = MandiRate.query.order_by(MandiRate.updated_at.desc()).limit(8).all()
    schemes = GovernmentScheme.query.filter_by(is_featured=True, is_active=True).limit(3).all()
    total_farmers = User.query.filter_by(role='farmer', is_active=True).count()
    total_buyers = User.query.filter_by(role='buyer', is_active=True).count()
    total_cold_storages = ColdStorage.query.filter_by(is_active=True).count()

    return render_template(
        'index.html',
        featured_crops=featured_crops,
        latest_mandi=latest_mandi,
        schemes=schemes,
        stats={
            'farmers': max(total_farmers, 150),
            'buyers': max(total_buyers, 80),
            'cold_storages': max(total_cold_storages, 12),
            'mandis_covered': 45
        }
    )

@main_bp.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['en', 'hi', 'mr', 'ta', 'te']:
        session['language'] = lang
        if g.user:
            g.user.preferred_language = lang
            db.session.commit()
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/visiting-card/<custom_id>')
def public_visiting_card(custom_id):
    user = User.query.filter_by(custom_id=custom_id).first_or_404()
    profile = user.farmer_profile if user.role == 'farmer' else user.buyer_profile
    return render_template('shared/visiting_card_view.html', card_user=user, profile=profile)

@main_bp.route('/login')
def login_redirect():
    return redirect(url_for('auth.login'))

@main_bp.route('/admin/login')
def admin_login_redirect():
    return redirect(url_for('auth.admin_login'))

@main_bp.route('/register')
def register_redirect():
    return redirect(url_for('auth.register'))

