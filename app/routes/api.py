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


from app.services.ai_voice_service import AIVoiceService


@api_bp.route('/voice-query', methods=['POST'])
def voice_query():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify({
            'success': True,
            'response_text': 'Namaste! I am Krishi Mitra, your agricultural AI copilot. Ask me anything about mandi rates, cold storages, government schemes, or buying/selling crops.',
            'action_url': '/farmer/mandi-rates',
            'action_label': 'View Live Mandi Rates'
        })

    user_context = None
    if g.user:
        user_context = {
            'id': g.user.id,
            'name': g.user.name,
            'role': g.user.role,
            'preferred_language': g.user.preferred_language
        }

    result = AIVoiceService.process_query(query, user_context)
    return jsonify(result)


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
