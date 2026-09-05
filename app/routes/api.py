from flask import Blueprint, request, jsonify, g
from app.models import MandiRate, Product, User
from app.services.mandi_service import MandiService
from app.services.deal_analysis_service import DealAnalysisService

api_bp = Blueprint('api', __name__)

@api_bp.route('/mandi-rate-lookup')
def mandi_rate_lookup():
    commodity = request.args.get('commodity', '').strip()
    district = request.args.get('district', '').strip()

    if not commodity:
        return jsonify({'found': False, 'error': 'Commodity required'}), 400

    info = MandiService.get_rate_for_commodity(commodity, district)
    return jsonify(info)


@api_bp.route('/analyze-deal', methods=['POST'])
def analyze_deal():
    data = request.get_json() or {}
    commodity = data.get('commodity', '')
    offered_price = float(data.get('offered_price', 0))
    unit = data.get('unit', 'kg')
    district = data.get('district', '')

    analysis = DealAnalysisService.analyze_offer(
        commodity_name=commodity,
        offered_price_per_unit=offered_price,
        unit=unit,
        district=district
    )
    return jsonify(analysis)


@api_bp.route('/voice-query', methods=['POST'])
def voice_query():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    query_lower = query.lower()

    response_text = "Namaste! I am Krishi Mitra, your agricultural AI copilot. You can ask me for live APMC Mandi rates, cold storage facilities, government schemes, or quick navigation."
    action_url = None
    action_label = None

    # Enhanced Multilingual Crop Dictionary
    crops_map = {
        'wheat': 'Wheat', 'गेहूं': 'Wheat', 'gehun': 'Wheat', 'gehu': 'Wheat', 'gahu': 'Wheat',
        'onion': 'Onion', 'प्याज': 'Onion', 'pyaz': 'Onion', 'kanda': 'Onion',
        'tomato': 'Tomato', 'टमाटर': 'Tomato', 'tamatar': 'Tomato',
        'potato': 'Potato', 'आलू': 'Potato', 'aaloo': 'Potato', 'alu': 'Potato', 'batata': 'Potato',
        'rice': 'Rice', 'चावल': 'Rice', 'dhan': 'Rice', 'धान': 'Rice', 'chawal': 'Rice', 'paddy': 'Rice',
        'soybean': 'Soybean', 'सोयाबीन': 'Soybean', 'soya': 'Soybean',
        'cotton': 'Cotton', 'कपास': 'Cotton', 'kapas': 'Cotton', 'rui': 'Cotton',
        'garlic': 'Garlic', 'लहसुन': 'Garlic', 'lahsun': 'Garlic',
        'mustard': 'Mustard', 'सरसों': 'Mustard', 'sarso': 'Mustard',
        'maize': 'Maize', 'मक्का': 'Maize', 'makka': 'Maize', 'bhutta': 'Maize',
        'gram': 'Gram', 'चना': 'Gram', 'chana': 'Gram',
        'banana': 'Banana', 'केला': 'Banana', 'kela': 'Banana',
        'apple': 'Apple', 'सेब': 'Apple', 'seb': 'Apple'
    }

    matched_crop = None
    for keyword, crop_name in crops_map.items():
        if keyword in query_lower:
            matched_crop = crop_name
            break

    if matched_crop:
        rate_info = MandiService.get_rate_for_commodity(matched_crop)
        rate_kg = rate_info.get('rate_per_kg', 25.0)
        modal_price = rate_info.get('raw_modal_price', rate_kg * 100)
        market = rate_info.get('market_name', 'APMC Mandi')
        trend = rate_info.get('trend', 'stable')
        trend_msg = "Rates are showing an upward trend." if trend == 'up' else ("Rates are slightly lower today." if trend == 'down' else "Rates remain stable today.")
        
        response_text = f"Today's Mandi rate for {matched_crop} is ₹{rate_kg}/kg (₹{modal_price:.0f}/Quintal) at {market}. {trend_msg}"
        action_url = f"/farmer/mandi-rates?commodity={matched_crop}"
        action_label = f"View Full {matched_crop} Mandi Analytics"

    elif any(k in query_lower for k in ['pm kisan', 'pm-kisan', 'kisan samman', 'सम्मान निधि', 'योजना', 'scheme', 'subsidy', 'pmfby', 'fasal bima', 'insurance', 'aif', 'kcc', 'credit card']):
        if 'pm kisan' in query_lower or 'सम्मान निधि' in query_lower:
            response_text = "PM-KISAN Samman Nidhi provides ₹6,000 per year directly into farmers' bank accounts in 3 equal installments of ₹2,000. You can view eligibility and application links on our Schemes portal."
        elif 'bima' in query_lower or 'insurance' in query_lower or 'pmfby' in query_lower:
            response_text = "Pradhan Mantri Fasal Bima Yojana (PMFBY) covers crop loss due to non-preventable natural risks with premium subsidies up to 90%."
        elif 'kcc' in query_lower or 'credit card' in query_lower:
            response_text = "Kisan Credit Card (KCC) provides short-term institutional credit at 4% effective interest rate for crop cultivation and post-harvest maintenance."
        else:
            response_text = "Krishi Kendra tracks all active central and state agricultural welfare schemes including PM-KISAN, PMFBY, and Agri Infrastructure Fund (AIF)."
        action_url = "/schemes/"
        action_label = "Open Government Schemes Board"

    elif any(k in query_lower for k in ['cold storage', 'storage', 'कोल्ड स्टोरेज', 'warehouse', 'गोदाम', 'store']):
        response_text = "Krishi Kendra has integrated accredited cold storage facilities across major agricultural districts with real-time temperature, capacity, and per-day rental rates."
        action_url = "/cold-storage/"
        action_label = "Explore Available Cold Storages"

    elif any(k in query_lower for k in ['add crop', 'add produce', 'list crop', 'inventory', 'फसल जोड़ें', 'बेचना', 'sell', 'new harvest', 'list produce']):
        response_text = "Taking you to the Add Produce wizard. You can list your crop details, upload photos, set expected pricing, and compare with live Mandi benchmarks."
        action_url = "/farmer/inventory/add"
        action_label = "Add Produce to Inventory"

    elif any(k in query_lower for k in ['order', 'ऑर्डर', 'requests', 'offers', 'negotiation', 'counter offer', 'सौदे']):
        response_text = "Opening your active orders and buyer counter-offer requests for direct review and confirmation."
        action_url = "/farmer/orders"
        action_label = "View Orders & Deals"

    elif any(k in query_lower for k in ['marketplace', 'buy crop', 'खरीदें', 'बाजार', 'browse', 'shop', 'produce list']):
        response_text = "Opening Krishi Kendra Marketplace with verified direct farm produce listings and quality certifications."
        action_url = "/marketplace/"
        action_label = "Browse Open Marketplace"

    elif any(k in query_lower for k in ['card', 'visiting card', 'विजिटिंग कार्ड', 'qr', 'contact card']):
        response_text = "Opening your digital Krishi Kendra Visiting Card with QR code verification."
        action_url = "/farmer/visiting-card"
        action_label = "Open My Visiting Card"

    elif any(k in query_lower for k in ['profile', 'setting', 'privacy', 'photo', 'avatar', 'खाता']):
        response_text = "Taking you to Profile Settings to update personal details, profile picture, and phone privacy preferences."
        action_url = "/auth/profile"
        action_label = "Edit Profile & Settings"

    elif any(k in query_lower for k in ['weather', 'मौसम', 'rain', 'barish', 'forecast']):
        response_text = "Agricultural Weather Advisory: Moderate temperatures expected across the region. Ensure adequate drainage for standing rabi/kharif crops and monitor pest alerts."
        action_url = "/farmer/dashboard"
        action_label = "Return to Dashboard"

    else:
        response_text = f"I understood: '{query}'. You can ask for crop rates like 'Onion price today', 'Cold storage near me', 'PM-KISAN scheme', or 'List new crop'."
        action_url = "/farmer/mandi-rates"
        action_label = "View Live Mandi Rates"

    return jsonify({
        'success': True,
        'response_text': response_text,
        'action_url': action_url,
        'action_label': action_label
    })


@api_bp.route('/user-popup/<int:user_id>')
def user_popup(user_id):
    user = User.query.get_or_404(user_id)
    profile = user.farmer_profile if user.role == 'farmer' else user.buyer_profile
    
    # Strict Privacy check: phone is only exposed if consent is enabled
    share_consent = profile.share_phone_consent if profile else False
    
    data = {
        'id': user.id,
        'custom_id': user.custom_id,
        'name': user.name,
        'role': user.role.capitalize(),
        'profile_image': user.profile_image,
        'is_verified': user.is_verified,
        'district': profile.district if profile else '',
        'state': profile.state if profile else '',
        'rating': getattr(profile, 'rating', 4.8),
        'phone_shared': share_consent,
        'phone': user.phone if share_consent else None,
        'bio': getattr(profile, 'bio', getattr(profile, 'description', ''))
    }
    return jsonify(data)
