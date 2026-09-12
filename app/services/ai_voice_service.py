import os
import re
import json
import logging
import time
from flask import g
from app.models import MandiRate, ColdStorage, GovernmentScheme, Inventory, Offer, User
from app.services.mandi_service import MandiService

logger = logging.getLogger(__name__)

# In-memory grounding context cache to eliminate multi-query DB latency
_platform_grounding_cache = ""
_platform_grounding_cache_time = 0

def detect_query_language(query: str, preferred_lang: str = 'en') -> str:
    """
    Detects the language of the user query with script analysis and keyword heuristics.
    Returns ISO language code: 'en', 'hi', 'mr', 'ta', 'te', etc.
    """
    if not query:
        return preferred_lang or 'en'
        
    # Check for Devanagari script (Hindi / Marathi)
    if re.search(r'[\u0900-\u097F]', query):
        # Marathi specific marker words
        marathi_markers = ['आहे', 'बघा', 'सांगा', 'शेतकरी', 'बाजारभाव', 'कांदा', 'कसा', 'काय', 'कुठे', 'पाहिजे', 'शेती']
        if any(w in query for w in marathi_markers) or preferred_lang == 'mr':
            return 'mr'
        return 'hi'
        
    # Check for Tamil script
    if re.search(r'[\u0B80-\u0BFF]', query):
        return 'ta'
        
    # Check for Telugu script
    if re.search(r'[\u0C00-\u0C7F]', query):
        return 'te'
        
    # Check for Bengali script
    if re.search(r'[\u0980-\u09FF]', query):
        return 'bn'

    # Check for Gujarati script
    if re.search(r'[\u0A80-\u0AFF]', query):
        return 'gu'

    query_lower = query.lower()
    
    # Check for Hinglish / Romanized Hindi indicators
    hinglish_markers = [
        'kya', 'hai', 'kaise', 'bhav', 'bhaav', 'dam', 'daam', 'kitna', 'bataye', 'batao',
        'kisan', 'fasal', 'bechna', 'kharidna', 'mandi', 'yojana', 'paisa', 'mujhe', 'chahiye'
    ]
    if any(re.search(r'\b' + re.escape(w) + r'\b', query_lower) for w in hinglish_markers):
        return 'hi' if preferred_lang == 'hi' else 'en' # Respond in user preferred or clear English/Hinglish

    # If pure English or ASCII
    english_words = ['price', 'rate', 'cost', 'storage', 'crop', 'wheat', 'onion', 'tomato', 'potato', 'scheme', 'farmer', 'buy', 'sell', 'order', 'hello', 'what', 'how', 'where']
    if any(re.search(r'\b' + re.escape(w) + r'\b', query_lower) for w in english_words):
        return 'en'

    return preferred_lang or 'en'


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
        Supports multi-turn conversation history and exact user-language alignment.
        """
        user_role = user_context.get('role', 'farmer') if user_context else 'farmer'
        user_name = user_context.get('name', 'Kisan') if user_context else 'Kisan'
        preferred_lang = user_context.get('preferred_language', 'en') if user_context else 'en'
        
        detected_lang = detect_query_language(query, preferred_lang)
        
        lang_names = {
            'en': 'English',
            'hi': 'Hindi (Devanagari)',
            'mr': 'Marathi (Devanagari)',
            'ta': 'Tamil',
            'te': 'Telugu',
            'bn': 'Bengali',
            'gu': 'Gujarati'
        }
        target_lang_name = lang_names.get(detected_lang, 'English')

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return AIVoiceService._fallback_rule_based(query, detected_lang)

        db_context = AIVoiceService.get_database_grounding_context(user_context)

        system_instruction = f"""
You are 'Kisan Saarthi' (किसान सारथी), an intelligent, conversational agricultural AI advisor and voice navigator on the Krishi Kendra platform.

USER PROFILE:
- Name: {user_name}
- Role: {user_role}
- User's Query Language: {target_lang_name} (Code: {detected_lang})

REAL-TIME PLATFORM DATABASE RECORDS:
{db_context}

CRITICAL LANGUAGE & CONVERSATIONAL DIRECTIVES:
1. MANDATORY LANGUAGE MATCHING:
   - The user asked this question in {target_lang_name}.
   - You MUST formulate your 'response_text' and 'action_label' in {target_lang_name}.
   - If the user asks in English -> Reply STRICTLY in natural, professional English. Do NOT use Hindi!
   - If the user asks in Hindi -> Reply in Hindi (Devanagari script).
   - If the user asks in Marathi -> Reply in Marathi (Devanagari script).
   - If the user asks in Tamil / Telugu / Bengali -> Reply in that respective language.
2. Ground your answers directly on the platform database records provided above when asked about mandi rates, cold storages, government schemes, or inventory.
3. Keep response concise (2 to 3 sentences max) so it sounds great during text-to-speech audio readout.
4. Suggest the single most appropriate deep-link action URL:
   - '/farmer/crop-doctor' -> Crop disease diagnosis, pest attack, leaf spots, spray recommendations
   - '/farmer/inventory/add' -> Add crop listing, sell harvest produce
   - '/farmer/mandi-rates' -> Live mandi rates, price trend charts
   - '/cold-storage/' -> Cold storage booking, storage capacity, rental rates
   - '/schemes/' -> PM-KISAN, PMFBY insurance, KCC loans, government subsidies
   - '/marketplace/' -> Buy produce, browse open marketplace
   - '/farmer/orders' -> Active orders, incoming buyer counter-offers
   - '/impact' -> Market comparison, profit calculator, economic benefits
   - '/farmer/visiting-card' -> Digital visiting card, QR profile
   - '/auth/profile' -> Profile & account settings
   - '/farmer/dashboard' -> General navigation

Return STRICTLY a JSON object with this structure:
{{
  "response_text": "<concise spoken reply strictly in {target_lang_name}>",
  "action_url": "<relevant url or null>",
  "action_label": "<short button label strictly in {target_lang_name}>"
}}
"""

        # Build prompt with history
        history_text = ""
        if conversation_history and isinstance(conversation_history, list):
            for turn in conversation_history[-4:]:
                role_label = "User" if turn.get('role') == 'user' else "Kisan Saarthi"
                history_text += f"{role_label}: {turn.get('content', '')}\n"

        full_prompt = f"{system_instruction}\n\nCONVERSATION HISTORY:\n{history_text}\nUser Voice Query: {query}"

        model_candidates = [
            'gemini-3.1-flash-lite',
            'gemini-3.5-flash-lite',
            'gemini-flash-lite-latest',
            'gemini-3.1-flash-lite-preview',
            'gemini-flash-latest',
            'gemini-3.5-flash',
            'gemini-3.6-flash',
            'gemini-2.5-flash-lite'
        ]
        for model_candidate in model_candidates:
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
                if text_out.startswith("```"):
                    text_out = text_out.strip("`").replace("json\n", "", 1).strip()
                data = json.loads(text_out)
                
                return {
                    'success': True,
                    'response_text': data.get('response_text', ''),
                    'action_url': data.get('action_url'),
                    'action_label': data.get('action_label', 'Open Page'),
                    'is_ai': True,
                    'language': detected_lang,
                    'model': model_candidate
                }
            except Exception as e:
                logger.warning(f"Model {model_candidate} attempt note: {e}")
                continue

        # Fallback to local multilingual rule-based if all API calls failed
        return AIVoiceService._fallback_rule_based(query, detected_lang)

    @staticmethod
    def _fallback_rule_based(query: str, lang: str = 'en') -> dict:
        """Local smart multilingual agricultural knowledge fallback when offline or no API key."""
        query_lower = query.lower()

        crops_map = {
            'wheat': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},
            'gehun': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},
            'gehu': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},
            'gahu': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},
            'गेहूं': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},
            'गहू': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},

            'onion': {'en': 'Onion', 'hi': 'प्याज', 'mr': 'कांदा'},
            'pyaz': {'en': 'Onion', 'hi': 'प्याज', 'mr': 'कांदा'},
            'kanda': {'en': 'Onion', 'hi': 'प्याज', 'mr': 'कांदा'},
            'प्याज': {'en': 'Onion', 'hi': 'प्याज', 'mr': 'कांदा'},
            'कांदा': {'en': 'Onion', 'hi': 'प्याज', 'mr': 'कांदा'},

            'tomato': {'en': 'Tomato', 'hi': 'टमाटर', 'mr': 'टोमॅटो'},
            'tamatar': {'en': 'Tomato', 'hi': 'टमाटर', 'mr': 'टोमॅटो'},
            'टमाटर': {'en': 'Tomato', 'hi': 'टमाटर', 'mr': 'टोमॅटो'},
            'टोमॅटो': {'en': 'Tomato', 'hi': 'टमाटर', 'mr': 'टोमॅटो'},

            'potato': {'en': 'Potato', 'hi': 'आलू', 'mr': 'बटाटा'},
            'aaloo': {'en': 'Potato', 'hi': 'आलू', 'mr': 'बटाटा'},
            'alu': {'en': 'Potato', 'hi': 'आलू', 'mr': 'बटाटा'},
            'batata': {'en': 'Potato', 'hi': 'आलू', 'mr': 'बटाटा'},
            'आलू': {'en': 'Potato', 'hi': 'आलू', 'mr': 'बटाटा'},
            'बटाटा': {'en': 'Potato', 'hi': 'आलू', 'mr': 'बटाटा'},

            'rice': {'en': 'Rice', 'hi': 'चावल', 'mr': 'तांदूळ'},
            'paddy': {'en': 'Rice', 'hi': 'धान', 'mr': 'भात'},
            'chawal': {'en': 'Rice', 'hi': 'चावल', 'mr': 'तांदूळ'},
            'dhan': {'en': 'Rice', 'hi': 'धान', 'mr': 'भात'},
            'चावल': {'en': 'Rice', 'hi': 'चावल', 'mr': 'तांदूळ'},
            'धान': {'en': 'Rice', 'hi': 'धान', 'mr': 'भात'},

            'soybean': {'en': 'Soybean', 'hi': 'सोयाबीन', 'mr': 'सोयाबीन'},
            'soya': {'en': 'Soybean', 'hi': 'सोयाबीन', 'mr': 'सोयाबीन'},
            'सोयाबीन': {'en': 'Soybean', 'hi': 'सोयाबीन', 'mr': 'सोयाबीन'},

            'cotton': {'en': 'Cotton', 'hi': 'कपास', 'mr': 'कापूस'},
            'kapas': {'en': 'Cotton', 'hi': 'कपास', 'mr': 'कापूस'},
            'कपास': {'en': 'Cotton', 'hi': 'कपास', 'mr': 'कापूस'},
            'कापूस': {'en': 'Cotton', 'hi': 'कपास', 'mr': 'कापूस'},

            'mustard': {'en': 'Mustard', 'hi': 'सरसों', 'mr': 'मोहरी'},
            'sarso': {'en': 'Mustard', 'hi': 'सरसों', 'mr': 'मोहरी'},
            'सरसों': {'en': 'Mustard', 'hi': 'सरसों', 'mr': 'मोहरी'}
        }

        matched_crop_dict = None
        for keyword, names in crops_map.items():
            if keyword in query_lower:
                matched_crop_dict = names
                break

        if matched_crop_dict:
            crop_en = matched_crop_dict['en']
            crop_local = matched_crop_dict.get(lang, crop_en)
            rate_info = MandiService.get_rate_for_commodity(crop_en)
            rate_kg = rate_info.get('rate_per_kg', 25.0)
            modal_price = rate_info.get('raw_modal_price', rate_kg * 100)
            market = rate_info.get('market_name', 'District APMC Mandi')
            trend = rate_info.get('trend', 'stable')

            if lang == 'hi':
                trend_msg = "भाव में आज तेजी देखी जा रही है।" if trend == 'up' else ("भाव में आज हल्की नरमी है।" if trend == 'down' else "भाव आज स्थिर हैं।")
                response_text = f"आज {market} में {crop_local} का मंडी भाव ₹{rate_kg}/किलो (₹{modal_price:.0f}/क्विंटल) है। {trend_msg}"
                action_label = f"{crop_local} मंडी भाव देखें"
            elif lang == 'mr':
                trend_msg = "बाजारात आज तेजी दिसत आहे." if trend == 'up' else ("बाजारात आज थोडी मंदी आहे." if trend == 'down' else "बाजारभाव आज स्थिर आहेत.")
                response_text = f"आज {market} मध्ये {crop_local} चा बाजारभाव ₹{rate_kg}/किलो (₹{modal_price:.0f}/क्विंटल) आहे. {trend_msg}"
                action_label = f"{crop_local} बाजारभाव पहा"
            else:
                trend_msg = "Rates are showing an upward trend." if trend == 'up' else ("Rates are slightly lower today." if trend == 'down' else "Rates remain stable today.")
                response_text = f"Today's Mandi rate for {crop_en} is ₹{rate_kg}/kg (₹{modal_price:.0f}/Quintal) at {market}. {trend_msg}"
                action_label = f"View {crop_en} Mandi Rates"

            action_url = f"/farmer/mandi-rates?commodity={crop_en}"

        elif any(k in query_lower for k in ['pm kisan', 'pm-kisan', 'kisan samman', 'सम्मान निधि', 'योजना', 'scheme', 'subsidy', 'pmfby', 'fasal bima', 'insurance', 'aif', 'kcc', 'credit card']):
            if lang == 'hi':
                response_text = "पीएम-किसान योजना के तहत किसानों को हर साल ₹6,000 की वित्तीय सहायता 3 किस्तों में दी जाती है। आप हमारी योजना बोर्ड पर सभी विवरण देख सकते हैं।"
                action_label = "सरकारी योजनाएं देखें"
            elif lang == 'mr':
                response_text = "पीएम-किसान योजनेअंतर्गत शेतकऱ्यांना दरवर्षी ₹6,000 ची मदत 3 हप्त्यांमध्ये दिली जाते. सविस्तर माहिती योजना पृष्ठावर उपलब्ध आहे."
                action_label = "शासकीय योजना पहा"
            else:
                response_text = "PM-KISAN Samman Nidhi provides ₹6,000/year in 3 installments directly to farmers' bank accounts. Explore active schemes on our dashboard."
                action_label = "Open Schemes Board"
            action_url = "/schemes/"

        elif any(k in query_lower for k in ['cold storage', 'storage', 'कोल्ड स्टोरेज', 'warehouse', 'गोदाम', 'store']):
            if lang == 'hi':
                response_text = "कृषि केंद्र पर तापमान, लाइव खाली क्षमता और दैनिक किराए के साथ सत्यापित कोल्ड स्टोरेज उपलब्ध हैं।"
                action_label = "कोल्ड स्टोरेज खोजें"
            elif lang == 'mr':
                response_text = "कृषी केंद्रावर तापमान, उपलब्ध क्षमता आणि दैनिक दरांसह प्रमाणित कोल्ड स्टोरेज उपलब्ध आहेत."
                action_label = "कोल्ड स्टोरेज शोधा"
            else:
                response_text = "Krishi Kendra provides accredited cold storage facilities with real-time temperature, capacity tracking, and daily rental rates."
                action_label = "Explore Cold Storages"
            action_url = "/cold-storage/"

        elif any(k in query_lower for k in ['add crop', 'add produce', 'list crop', 'inventory', 'फसल जोड़ें', 'बेचना', 'sell', 'new harvest', 'list produce']):
            if lang == 'hi':
                response_text = "फसल बिक्री विजार्ड खुल रहा है जहाँ आप मात्रा, भाव और फोटो जोड़कर सीधे खरीदारों से जुड़ सकते हैं।"
                action_label = "फसल बिक्री के लिए जोड़ें"
            elif lang == 'mr':
                response_text = "नवीन शेतमाल विक्री पेज उघडत आहे जेथे आपण पिकाची माहिती आणि अपेक्षित दर नोंदवू शकता."
                action_label = "शेतमाल विक्री नोंदणी"
            else:
                response_text = "Opening the Add Produce wizard where you can list crops, set your price, and compare with live Mandi rates."
                action_label = "Add Produce to Inventory"
            action_url = "/farmer/inventory/add"

        elif any(k in query_lower for k in ['order', 'ऑर्डर', 'requests', 'offers', 'negotiation', 'counter offer', 'सौदे']):
            if lang == 'hi':
                response_text = "आपके सक्रिय ऑर्डर्स और खरीदारों के सौदों की सूची खोली जा रही है।"
                action_label = "ऑर्डर्स और सौदे देखें"
            elif lang == 'mr':
                response_text = "आपल्या सक्रिय ऑर्डर्स आणि खरेदीदारांच्या मागण्यांची यादी उघडत आहे."
                action_label = "ऑर्डर्स पहा"
            else:
                response_text = "Opening your active orders and buyer counter-offer requests for direct review and confirmation."
                action_label = "View Orders & Deals"
            action_url = "/farmer/orders"

        elif any(k in query_lower for k in ['card', 'visiting card', 'विजिटिंग कार्ड', 'qr', 'contact card']):
            if lang == 'hi':
                response_text = "आपका डिजिटल विजिटिंग कार्ड और क्यूआर कोड खोला जा रहा है।"
                action_label = "विजिटिंग कार्ड देखें"
            elif lang == 'mr':
                response_text = "आपले डिजिटल व्हिजिटिंग कार्ड आणि क्यूआर प्रोफाइल उघडत आहे."
                action_label = "व्हिजिटिंग कार्ड पहा"
            else:
                response_text = "Opening your digital Krishi Kendra Visiting Card with QR code verification."
                action_label = "Open My Visiting Card"
            action_url = "/farmer/visiting-card"

        elif any(k in query_lower for k in ['doctor', 'disease', 'pest', 'leaf', 'spray', 'कीट', 'रोग', 'दवा', 'डॉक्टर', 'पाने']):
            if lang == 'hi':
                response_text = "एआई क्रॉप डॉक्टर खुल रहा है। पौधे या पत्ती की फोटो अपलोड करके तुरंत रोग पहचान और जैविक उपचार प्राप्त करें।"
                action_label = "एआई क्रॉप डॉक्टर खोलें"
            elif lang == 'mr':
                response_text = "एआय पीक डॉक्टर उघडत आहे. पिकाचा किंवा पानाचा फोटो अपलोड करून रोगाचे त्वरित निदान मिळवा."
                action_label = "एआय पीक डॉक्टर उघडा"
            else:
                response_text = "Opening AI Crop Doctor. Upload a photo of damaged leaves or crops for instant disease diagnosis and treatment steps."
                action_label = "Open AI Crop Doctor"
            action_url = "/farmer/crop-doctor"

        elif any(k in query_lower for k in ['impact', 'profit', 'calculator', 'comparison', 'फायदा', 'कैलकुलेटर', 'मुनाफा']):
            if lang == 'hi':
                response_text = "मार्केट तुलना और मुनाफा कैलकुलेटर खोला जा रहा है जहाँ आप बिचौलियों के बिना अपनी अतिरिक्त कमाई देख सकते हैं।"
                action_label = "मार्केट तुलना और मुनाफा देखें"
            elif lang == 'mr':
                response_text = "बाजार तुलना आणि नफा कॅल्क्युलेटर उघडत आहे जेथे आपण थेट विक्रीचा फायदा तपासू शकता."
                action_label = "नफा कॅल्क्युलेटर पहा"
            else:
                response_text = "Opening Market Comparison & Profit Simulator to view net extra earnings compared to traditional mandis."
                action_label = "View Profit Comparison"
            action_url = "/impact"

        else:
            if lang == 'hi':
                response_text = f"मैंने समझा: '{query}'। आप मुझसे 'आज प्याज का भाव', 'कोल्ड स्टोरेज', 'फसल रोग जांच' या 'फसल जोड़ें' के बारे में पूछ सकते हैं।"
                action_label = "मंडी भाव देखें"
            elif lang == 'mr':
                response_text = f"मी समजलो: '{query}'। आपण मला 'कांद्याचा भाव', 'कोल्ड स्टोरेज', 'पीक रोग तपासणी' किंवा 'शेतमाल विक्री' विचारू शकता."
                action_label = "बाजारभाव पहा"
            else:
                response_text = f"I understood: '{query}'. You can ask for crop rates like 'Wheat price today', 'Cold storage near me', 'PM-KISAN scheme', or 'Check crop disease'."
                action_label = "View Live Mandi Rates"
            action_url = "/farmer/mandi-rates"

        return {
            'success': True,
            'response_text': response_text,
            'action_url': action_url,
            'action_label': action_label,
            'is_ai': False,
            'language': lang
        }
