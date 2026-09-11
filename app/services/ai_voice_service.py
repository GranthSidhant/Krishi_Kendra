import os
import json
import logging
import urllib.request
import urllib.parse
from app.services.mandi_service import MandiService

logger = logging.getLogger(__name__)

class AIVoiceService:
    @staticmethod
    def process_query(query: str, user_context: dict = None) -> dict:
        """
        Processes voice/text query with Google Gemini AI.
        Falls back seamlessly to local agricultural intelligence if GEMINI_API_KEY is not configured or offline.
        """
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return AIVoiceService._fallback_rule_based(query)

        user_role = user_context.get('role', 'farmer') if user_context else 'farmer'
        user_name = user_context.get('name', 'Farmer') if user_context else 'Farmer'

        # Live Mandi benchmark sample for context grounding
        mandi_sample = "Wheat: ₹2,275/Q (Nashik), Onion: ₹2,450/Q (Lasalgaon), Tomato: ₹1,800/Q (Pune), Soybean: ₹4,600/Q (Indore)"

        system_instruction = f"""
You are 'Krishi Mitra' (कृषि मित्र), an expert agricultural AI copilot on the Krishi Kendra platform.
You assist Indian farmers, buyers, and traders.

User Info:
- Role: {user_role}
- Name: {user_name}
- Live platform Mandi rates sample: {mandi_sample}

Guidelines:
1. Understand queries in any Indian regional language (Hindi, Marathi, Tamil, Telugu, English, Hinglish).
2. Answer concisely (2-3 sentences max) in the EXACT same language and script the user spoke.
3. Provide practical, encouraging agricultural guidance (prices, post-harvest storage, schemes like PM-KISAN/PMFBY, selling produce).
4. Match to the most relevant deep-link URL:
   - '/farmer/inventory/add' (Sell produce / Add crop listing)
   - '/farmer/mandi-rates' (Live APMC mandi rates & price analytics)
   - '/cold-storage/' (Book accredited cold storage warehouse)
   - '/schemes/' (Govt agricultural subsidies, PM-KISAN, PMFBY, KCC)
   - '/marketplace/' (Browse marketplace / Buy produce)
   - '/farmer/orders' (Active deals, orders, negotiations)
   - '/farmer/visiting-card' (Digital Kisan Visiting Card with QR)
   - '/auth/profile' (Profile, avatar, verification settings)
   - '/farmer/dashboard' (Weather & general advisory)

Output STRICTLY a valid JSON object:
{{
  "response_text": "Spoken answer in user's language",
  "action_url": "/selected-path",
  "action_label": "Button text in user's language (e.g. 'मंडी भाव देखें' or 'View Schemes')"
}}
"""

        # Method 1: Try using google-genai SDK
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"User query: {query}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )
            data = json.loads(response.text)
            return {
                'success': True,
                'response_text': data.get('response_text', ''),
                'action_url': data.get('action_url'),
                'action_label': data.get('action_label', 'Open Page'),
                'is_ai': True
            }
        except Exception as sdk_err:
            logger.info(f"SDK attempt note: {sdk_err}. Trying REST API endpoint...")

        # Method 2: Fallback to direct Gemini REST API via standard library
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}\n\nUser query: {query}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0.3
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_body = json.loads(resp.read().decode('utf-8'))
                raw_text = res_body['candidates'][0]['content']['parts'][0]['text']
                data = json.loads(raw_text)
                return {
                    'success': True,
                    'response_text': data.get('response_text', ''),
                    'action_url': data.get('action_url'),
                    'action_label': data.get('action_label', 'Open Page'),
                    'is_ai': True
                }
        except Exception as rest_err:
            logger.warning(f"Gemini REST call failed: {rest_err}. Falling back to rule-based logic.")
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
