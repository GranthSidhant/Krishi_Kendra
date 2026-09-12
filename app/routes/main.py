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

@main_bp.route('/impact')
def market_impact():
    # Preset commodities with real-world economic benchmarks
    preset_commodities = [
        {
            'id': 'wheat',
            'name': 'Wheat (गेहूं)',
            'icon': '🌾',
            'base_rate': 2650,
            'msp': 2275,
            'unit': 'Quintal',
            'traditional_cut_pct': 11.5,
            'traditional_handling': 65,
            'traditional_spoilage_pct': 3.0,
            'aggregator_cut_pct': 10.0,
            'aggregator_handling': 45,
            'aggregator_spoilage_pct': 2.0,
            'krishi_handling': 20,
            'krishi_spoilage_pct': 0.8
        },
        {
            'id': 'onion',
            'name': 'Red Onion (लाल प्याज)',
            'icon': '🧅',
            'base_rate': 2100,
            'msp': None,
            'unit': 'Quintal',
            'traditional_cut_pct': 14.0,
            'traditional_handling': 85,
            'traditional_spoilage_pct': 9.0,
            'aggregator_cut_pct': 12.5,
            'aggregator_handling': 60,
            'aggregator_spoilage_pct': 5.0,
            'krishi_handling': 30,
            'krishi_spoilage_pct': 1.5
        },
        {
            'id': 'tomato',
            'name': 'Tomato (टमाटर)',
            'icon': '🍅',
            'base_rate': 2400,
            'msp': None,
            'unit': 'Quintal',
            'traditional_cut_pct': 15.5,
            'traditional_handling': 90,
            'traditional_spoilage_pct': 12.0,
            'aggregator_cut_pct': 13.0,
            'aggregator_handling': 65,
            'aggregator_spoilage_pct': 6.0,
            'krishi_handling': 35,
            'krishi_spoilage_pct': 2.0
        },
        {
            'id': 'rice',
            'name': 'Basmati Rice (बासमती चावल)',
            'icon': '🍚',
            'base_rate': 4800,
            'msp': 2300,
            'unit': 'Quintal',
            'traditional_cut_pct': 10.0,
            'traditional_handling': 70,
            'traditional_spoilage_pct': 2.5,
            'aggregator_cut_pct': 9.0,
            'aggregator_handling': 50,
            'aggregator_spoilage_pct': 1.5,
            'krishi_handling': 25,
            'krishi_spoilage_pct': 0.5
        },
        {
            'id': 'potato',
            'name': 'Potato (आलू)',
            'icon': '🥔',
            'base_rate': 1650,
            'msp': None,
            'unit': 'Quintal',
            'traditional_cut_pct': 13.0,
            'traditional_handling': 75,
            'traditional_spoilage_pct': 7.0,
            'aggregator_cut_pct': 11.0,
            'aggregator_handling': 55,
            'aggregator_spoilage_pct': 4.0,
            'krishi_handling': 25,
            'krishi_spoilage_pct': 1.2
        },
        {
            'id': 'soybean',
            'name': 'Soybean (सोयाबीन)',
            'icon': '🌱',
            'base_rate': 4600,
            'msp': 4892,
            'unit': 'Quintal',
            'traditional_cut_pct': 10.5,
            'traditional_handling': 60,
            'traditional_spoilage_pct': 2.5,
            'aggregator_cut_pct': 8.5,
            'aggregator_handling': 40,
            'aggregator_spoilage_pct': 1.5,
            'krishi_handling': 20,
            'krishi_spoilage_pct': 0.6
        },
        {
            'id': 'cotton',
            'name': 'Cotton (कपास)',
            'icon': '☁️',
            'base_rate': 7100,
            'msp': 7121,
            'unit': 'Quintal',
            'traditional_cut_pct': 9.5,
            'traditional_handling': 80,
            'traditional_spoilage_pct': 2.0,
            'aggregator_cut_pct': 8.0,
            'aggregator_handling': 55,
            'aggregator_spoilage_pct': 1.0,
            'krishi_handling': 25,
            'krishi_spoilage_pct': 0.5
        },
        {
            'id': 'mustard',
            'name': 'Mustard Seed (सरसों)',
            'icon': '🌼',
            'base_rate': 5450,
            'msp': 5650,
            'unit': 'Quintal',
            'traditional_cut_pct': 10.0,
            'traditional_handling': 65,
            'traditional_spoilage_pct': 2.0,
            'aggregator_cut_pct': 8.5,
            'aggregator_handling': 45,
            'aggregator_spoilage_pct': 1.2,
            'krishi_handling': 20,
            'krishi_spoilage_pct': 0.5
        }
    ]
    
    # Try fetching live mandi updates to enhance presets
    for item in preset_commodities:
        mandi_match = MandiRate.query.filter(MandiRate.commodity.ilike(f"%{item['id']}%")).first()
        if mandi_match and mandi_match.modal_price:
            item['base_rate'] = round(mandi_match.modal_price, 2)
            item['market_name'] = mandi_match.market_name
            item['district'] = mandi_match.district

    return render_template('market_impact.html', preset_commodities=preset_commodities)

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

