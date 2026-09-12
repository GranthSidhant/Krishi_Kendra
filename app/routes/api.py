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
    history = data.get('history', [])
    if not query:
        return jsonify({
            'success': True,
            'response_text': 'Namaste! I am Kisan Saarthi, your AI agricultural voice copilot. Ask me anything about live mandi rates, cold storages, government schemes, or your active farm inventory and deals.',
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

    result = AIVoiceService.process_query(query, user_context, history)
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
        'profile_image': user.avatar_src,
        'avatar_emoji': user.avatar_emoji,
        'is_verified': user.is_verified,
        'district': profile.district if profile else '',
        'state': profile.state if profile else '',
        'rating': getattr(profile, 'rating', 4.8),
        'phone_shared': share_consent,
        'phone': user.phone if share_consent else None,
        'bio': getattr(profile, 'bio', getattr(profile, 'description', ''))
    }
    return jsonify(data)


# ----------------------------------------------------
# Real-Time Live Weather API
# ----------------------------------------------------
from app.services.weather_service import WeatherService

@api_bp.route('/weather')
def get_weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    district = request.args.get('district', '').strip()
    
    if not district and g.user:
        profile = g.user.farmer_profile if g.user.role == 'farmer' else g.user.buyer_profile
        if profile and profile.district:
            district = profile.district

    weather_data = WeatherService.fetch_live_weather(lat=lat, lon=lon, district=district)
    return jsonify(weather_data)


# ----------------------------------------------------
# Report & Flagging Submission API
# ----------------------------------------------------
import random
from app.models import Report, Inventory, Requirement
from app.extensions import db

@api_bp.route('/report/submit', methods=['POST'])
def submit_report():
    if not g.user:
        return jsonify({'success': False, 'error': 'Please log in to submit a report.'}), 401
    
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    target_type = data.get('target_type', 'inventory') # 'inventory', 'requirement', 'user'
    target_id = int(data.get('target_id', 0))
    reason = data.get('reason', '').strip()
    details = data.get('details', '').strip()

    if not target_id or not reason:
        return jsonify({'success': False, 'error': 'Target item and reason are required.'}), 400

    target_title = ''
    target_owner_id = None

    if target_type == 'inventory':
        inv = Inventory.query.get(target_id)
        if inv:
            target_title = f"{inv.product_name} ({inv.available_quantity} {inv.unit} @ ₹{inv.expected_price_per_unit})"
            target_owner_id = inv.farmer_id
    elif target_type == 'requirement':
        req = Requirement.query.get(target_id)
        if req:
            target_title = f"Requirement: {req.product_name} ({req.required_quantity} {req.unit})"
            target_owner_id = req.buyer_id
    elif target_type == 'user':
        u = User.query.get(target_id)
        if u:
            target_title = f"User: {u.name} ({u.custom_id})"
            target_owner_id = u.id

    report_code = f"RPT-2026-{random.randint(1000, 9999)}"
    report = Report(
        report_code=report_code,
        reporter_id=g.user.id,
        target_type=target_type,
        target_id=target_id,
        target_title=target_title,
        target_owner_id=target_owner_id,
        reason=reason,
        details=details,
        status='pending'
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        'success': True,
        'report_code': report.report_code,
        'message': 'Report received and submitted to Krishi Kendra Admin Moderation.'
    })


# ----------------------------------------------------
# AI Crop Health Doctor & Disease Diagnostic Scanner
# ----------------------------------------------------
import base64
from app.services.crop_doctor_service import CropDoctorService

@api_bp.route('/crop-doctor/scan', methods=['POST'])
def crop_doctor_scan():
    crop_hint = request.form.get('crop_hint') or ''
    user_lang = request.form.get('lang') or (g.user.preferred_language if g.user else 'en')

    image_bytes = None
    mime_type = "image/jpeg"

    # Check multipart file upload
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            image_bytes = file.read()
            mime_type = file.content_type or "image/jpeg"
    
    # Or check base64 JSON payload
    if not image_bytes:
        data = request.get_json(silent=True) or {}
        image_data = data.get('image_base64', '')
        crop_hint = data.get('crop_hint') or crop_hint
        user_lang = data.get('lang') or user_lang
        if image_data:
            if ',' in image_data:
                header, encoded = image_data.split(',', 1)
                if 'png' in header:
                    mime_type = 'image/png'
                elif 'webp' in header:
                    mime_type = 'image/webp'
                image_bytes = base64.b64decode(encoded)
            else:
                image_bytes = base64.b64decode(image_data)

    if not image_bytes:
        return jsonify({'success': False, 'error': 'No image provided for crop scan.'}), 400

    report = CropDoctorService.analyze_crop_image(
        image_bytes=image_bytes,
        mime_type=mime_type,
        user_lang=user_lang,
        crop_hint=crop_hint
    )
    return jsonify(report)


@api_bp.route('/crop-doctor/sample/<sample_key>')
def crop_doctor_sample(sample_key):
    report = CropDoctorService.get_sample_diagnosis(sample_key)
    return jsonify(report)

