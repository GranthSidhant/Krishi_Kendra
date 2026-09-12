import os
import json
import logging
from flask import g
from app.models import MandiRate, ColdStorage, GovernmentScheme, Inventory, Offer, User
from app.services.mandi_service import MandiService

import time

logger = logging.getLogger(__name__)

# In-memory grounding context cache to eliminate multi-query DB latency
_platform_grounding_cache = ""
_platform_grounding_cache_time = 0

class AIVoiceService:
    @staticmethod
    def get_database_grounding_context(user_context: dict = None) -> str:
        """
        Dynamically extracts current database records with in-memory caching to eliminate DB latency.
        """
        global _platform_grounding_cache, _platform_grounding_cache_time
        now = time.time()
        
        # Reuse cached platform records if younger than 180 seconds
        if not _platform_grounding_cache or (now - _platform_grounding_cache_time > 180):
            context_parts = []
            
            # 1. Mandi Rates summary from Database
            try:
                rates = MandiRate.query.order_by(MandiRate.last_updated.desc()).limit(12).all()
                if rates:
                    rate_strs = [f"{r.commodity} in {r.market_name} ({r.district}): ₹{r.modal_price_per_kg}/kg (₹{r.modal_price_per_kg*100:.0f}/Q)" for r in rates]
                    context_parts.append("LIVE MANDI RATES IN DATABASE:\n" + "\n".join(rate_strs[:8]))
            except Exception as e:
                logger.debug(f"DB Mandi context note: {e}")

            # 2. Cold Storages from Database
            try:
                storages = ColdStorage.query.filter_by(is_active=True).limit(6).all()
                if storages:
                    storage_strs = [
                        f"{cs.name} ({cs.district}, {cs.state}): {cs.available_capacity_mt} MT available out of {cs.total_capacity_mt} MT, Temp: {cs.temperature_celsius}°C, Rate: ₹{cs.price_per_day_quintal}/day/Q"
                        for cs in storages
                    ]
                    context_parts.append("ACTIVE COLD STORAGES IN DATABASE:\n" + "\n".join(storage_strs))
            except Exception as e:
                logger.debug(f"DB Cold storage context note: {e}")

            # 3. Government Schemes from Database
            try:
                schemes = GovernmentScheme.query.filter_by(is_active=True).limit(6).all()
                if schemes:
                    scheme_strs = [f"{s.title} ({s.code}): {s.benefit_summary}" for s in schemes]
                    context_parts.append("GOVERNMENT SCHEMES IN DATABASE:\n" + "\n".join(scheme_strs))
            except Exception as e:
                logger.debug(f"DB Schemes context note: {e}")

            _platform_grounding_cache = "\n\n".join(context_parts)
            _platform_grounding_cache_time = now

        context_parts = [_platform_grounding_cache] if _platform_grounding_cache else []

        # 4. User-Specific Live Data (if logged in)
        if user_context and user_context.get('id'):
            user_id = user_context.get('id')
            role = user_context.get('role', 'farmer')
            try:
                if role == 'farmer':
                    my_inv = Inventory.query.filter_by(farmer_id=user_id, status='available').all()
                    if my_inv:
                        inv_strs = [f"{i.product_name} ({i.available_quantity} {i.unit} @ ₹{i.expected_price_per_unit}/{i.unit}, {i.quality_grade})" for i in my_inv]
                        context_parts.append(f"USER'S ACTIVE INVENTORY:\n" + ", ".join(inv_strs))
                    
                    my_offers = Offer.query.filter_by(farmer_id=user_id, status='pending').all()
                    if my_offers:
                        context_parts.append(f"USER'S PENDING BUYER OFFERS: {len(my_offers)} buyer offers awaiting confirmation in /farmer/orders")
                elif role == 'buyer':
                    buyer_offers = Offer.query.filter_by(buyer_id=user_id).limit(5).all()
                    if buyer_offers:
                        context_parts.append(f"USER'S BUYER OFFERS: {len(buyer_offers)} active trade requests placed.")
            except Exception as e:
                logger.debug(f"User context DB note: {e}")

        return "\n\n".join(context_parts)

    @staticmethod
    def process_query(query: str, user_context: dict = None, conversation_history: list = None) -> dict:
        """
        Processes voice/text queries using Google Gemini AI grounded on live database records.
        Supports multi-turn conversation history.
        """
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return AIVoiceService._fallback_rule_based(query)

        user_role = user_context.get('role', 'farmer') if user_context else 'farmer'
        user_name = user_context.get('name', 'Kisan') if user_context else 'Kisan'
        db_context = AIVoiceService.get_database_grounding_context(user_context)

        system_instruction = f"""
You are 'Kisan Saarthi' (किसान सारथी), an intelligent, conversational agricultural AI advisor and voice navigator on the Krishi Kendra platform.
You assist Indian farmers, buyers, and agricultural traders in their native regional languages (Hindi, Marathi, Tamil, Telugu, English, Hinglish).

CURRENT USER:
- Name: {user_name}
- Role: {user_role}

REAL-TIME PLATFORM DATABASE RECORDS:
{db_context}

INSTRUCTIONS:
1. Ground your answers directly on the platform database records provided above whenever answering about prices, cold storages, government schemes, or user inventory.
2. Reply concisely (2 to 3 sentences max) in the EXACT same language and script that the user asked in (e.g. reply in Devanagari Hindi if user asks in Hindi).
3. Be respectful, encouraging, and clear for voice readout.
4. Maintain context across conversation turns if the user asks follow-up questions.
5. Suggest the single most appropriate deep-link action URL:
   - '/farmer/inventory/add' -> If user wants to sell produce or add crop listing
   - '/farmer/mandi-rates' -> If user wants to check mandi rates or price charts
   - '/cold-storage/' -> If user asks about cold storage facilities or booking
   - '/schemes/' -> If user asks about government schemes (PM-KISAN, PMFBY, KCC, AIF)
   - '/marketplace/' -> If user wants to buy crops or browse listings
   - '/farmer/orders' -> If user asks about their active orders or deals
   - '/farmer/visiting-card' -> If user asks about digital visiting card or QR profile
   - '/auth/profile' -> If user asks about account settings or verification
   - '/farmer/dashboard' -> For general navigation or dashboard

Return STRICTLY a JSON object with this structure:
{{
  "response_text": "<concise spoken reply in user's language>",
  "action_url": "<relevant url or null>",
  "action_label": "<short button label in user's language, e.g. 'मंडी भाव देखें' or 'View Schemes'>"
}}
"""

        # Build prompt with history
        history_text = ""
        if conversation_history and isinstance(conversation_history, list):
            for turn in conversation_history[-4:]: # Keep last 4 turns for context
                role_label = "User" if turn.get('role') == 'user' else "Kisan Saarthi"
                history_text += f"{role_label}: {turn.get('content', '')}\n"

        full_prompt = f"{system_instruction}\n\nCONVERSATION HISTORY:\n{history_text}\nUser Voice Query: {query}"

        # Call Gemini using google-genai SDK (optimized for fast voice responses)
        for model_candidate in ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-flash-latest']:
            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=model_candidate,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                        max_output_tokens=350
                    )
                )
                
                text_out = response.text.strip()
                # Clean any markdown block formatting if present
                if text_out.startswith("```"):
                    text_out = text_out.strip("`").replace("json\n", "", 1).strip()
                data = json.loads(text_out)
                
                return {
                    'success': True,
                    'response_text': data.get('response_text', ''),
                    'action_url': data.get('action_url'),
                    'action_label': data.get('action_label', 'Open Page'),
                    'is_ai': True,
                    'model': model_candidate
                }
            except Exception as e:
                logger.warning(f"Model {model_candidate} attempt note: {e}")
                continue

        # Fallback to local rule-based if all API calls failed
        return AIVoiceService._fallback_rule_based(query)

    @staticmethod
    def _fallback_rule_based(query: str) -> dict:
        """Local smart agricultural knowledge fallback when offline or no API key."""
        query_lower = query.lower()

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
            action_label = f"View {matched_crop} Mandi Analytics"

        elif any(k in query_lower for k in ['pm kisan', 'pm-kisan', 'kisan samman', 'सम्मान निधि', 'योजना', 'scheme', 'subsidy', 'pmfby', 'fasal bima', 'insurance', 'aif', 'kcc', 'credit card']):
            if 'pm kisan' in query_lower or 'सम्मान निधि' in query_lower:
                response_text = "PM-KISAN Samman Nidhi provides ₹6,000/year in 3 installments of ₹2,000 directly to farmers' bank accounts. View details on our Schemes page."
            elif 'bima' in query_lower or 'insurance' in query_lower or 'pmfby' in query_lower:
                response_text = "PM Fasal Bima Yojana (PMFBY) covers crop loss from natural risks with up to 90% premium subsidies."
            elif 'kcc' in query_lower or 'credit card' in query_lower:
                response_text = "Kisan Credit Card (KCC) provides short-term crop loans at 4% effective interest rate."
            else:
                response_text = "Krishi Kendra tracks active agricultural schemes including PM-KISAN, PMFBY, and Agri Infrastructure Fund (AIF)."
            action_url = "/schemes/"
            action_label = "Open Schemes Board"

        elif any(k in query_lower for k in ['cold storage', 'storage', 'कोल्ड स्टोरेज', 'warehouse', 'गोदाम', 'store']):
            response_text = "Krishi Kendra provides accredited cold storage facilities with real-time temperature, capacity tracking, and per-day rental rates."
            action_url = "/cold-storage/"
            action_label = "Explore Cold Storages"

        elif any(k in query_lower for k in ['add crop', 'add produce', 'list crop', 'inventory', 'फसल जोड़ें', 'बेचना', 'sell', 'new harvest', 'list produce']):
            response_text = "Opening the Add Produce wizard where you can list crops, set prices, and compare with live Mandi rates."
            action_url = "/farmer/inventory/add"
            action_label = "Add Produce to Inventory"

        elif any(k in query_lower for k in ['order', 'ऑर्डर', 'requests', 'offers', 'negotiation', 'counter offer', 'सौदे']):
            response_text = "Opening your active orders and buyer counter-offer requests for direct review and confirmation."
            action_url = "/farmer/orders"
            action_label = "View Orders & Deals"

        elif any(k in query_lower for k in ['marketplace', 'buy crop', 'खरीदें', 'बाजार', 'browse', 'shop', 'produce list']):
            response_text = "Opening Krishi Kendra Marketplace with verified direct farm produce listings."
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
            response_text = "Agricultural Weather Advisory: Moderate temperatures expected. Ensure adequate field drainage and monitor pest alerts."
            action_url = "/farmer/dashboard"
            action_label = "Return to Dashboard"

        else:
            response_text = f"I understood: '{query}'. You can ask for crop rates like 'Onion price today', 'Cold storage near me', 'PM-KISAN scheme', or 'List new crop'."
            action_url = "/farmer/mandi-rates"
            action_label = "View Live Mandi Rates"

        return {
            'success': True,
            'response_text': response_text,
            'action_url': action_url,
            'action_label': action_label,
            'is_ai': False
        }
