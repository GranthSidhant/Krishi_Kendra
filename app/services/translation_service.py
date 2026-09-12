import os
import re
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# In-memory translation cache to guarantee sub-5ms response for repeated messages
_translation_cache = {}

LANGUAGE_NAMES = {
    'hi': 'Hindi (हिन्दी)',
    'mr': 'Marathi (मराठी)',
    'en': 'English',
    'ta': 'Tamil (தமிழ்)',
    'te': 'Telugu (తెలుగు)',
    'gu': 'Gujarati (ગુજરાતી)',
    'bn': 'Bengali (বাংলা)',
    'pa': 'Punjabi (ਪੰਜਾਬੀ)',
    'kn': 'Kannada (ಕನ್ನಡ)',
    'ml': 'Malayalam (മലയാളം)'
}

# Safety blacklist to reject unmoderated web spam or inappropriate terms
SPAM_BLOCKLIST = {
    'sexy', 'porn', 'xxx', 'video baf', 'nude', 'baf', 'adult', 'sex'
}

def contains_spam(text: str) -> bool:
    """Checks if translation output contains prohibited spam or inappropriate content."""
    if not text:
        return False
    lower = text.lower()
    for word in SPAM_BLOCKLIST:
        if word in lower:
            return True
    return False

# Curated High-Accuracy Multilingual Dictionaries for Agri-trade & Common Greetings
COMMON_PHRASES_HI = {
    "hi": "नमस्ते",
    "hii": "नमस्ते",
    "hello": "नमस्ते",
    "hey": "नमस्ते",
    "namaste": "नमस्ते",
    "namaskar": "नमस्कार",
    "pranam": "प्रणाम",
    "how are you": "आप कैसे हैं?",
    "how are you?": "आप कैसे हैं?",
    "kaise ho": "आप कैसे हैं?",
    "kaise ho?": "आप कैसे हैं?",
    "kese ho": "आप कैसे हैं?",
    "kasa ahes": "आप कैसे हैं?",
    "fine": "मैं ठीक हूँ",
    "i am fine": "मैं ठीक हूँ",
    "good": "अच्छा",
    "ok": "ठीक है",
    "okay": "ठीक है",
    "yes": "हाँ",
    "no": "नहीं",
    "ha": "हाँ",
    "nahi": "नहीं",
    "thanks": "धन्यवाद",
    "thank you": "धन्यवाद",
    "dhanyawad": "धन्यवाद",
    "shukriya": "शुक्रिया",
    "what is the price": "भाव क्या है?",
    "what is the rate": "दर क्या है?",
    "what is the price?": "भाव क्या है?",
    "what is the rate?": "दर क्या है?",
    "kya bhav hai": "भाव क्या है?",
    "kya rate hai": "दर क्या है?",
    "best price": "सर्वोत्तम भाव",
    "final price": "अंतिम भाव",
    "available": "उपलब्ध",
    "not available": "उपलब्ध नहीं है",
    "deal confirmed": "सौदा पक्का हुआ",
    "can you deliver": "क्या आप डिलीवरी कर सकते हैं?",
    "can you deliver?": "क्या आप डिलीवरी कर सकते हैं?",
    "ready for pickup": "उठाने के लिए तैयार है",
    "hello, what is the best price for your wheat?": "नमस्ते, आपके गेहूं का सबसे अच्छा भाव क्या है?",
    "fresh organic tomatoes ready for pickup": "ताजा जैविक टमाटर उठाने के लिए तैयार हैं",
    "50 quintals available": "50 क्विंटल उपलब्ध है",
    "payment via upi or cash": "यूपीआई या नकद द्वारा भुगतान",
    "mandi rate": "मंडी भाव"
}

COMMON_PHRASES_MR = {
    "hi": "नमस्कार",
    "hii": "नमस्कार",
    "hello": "नमस्कार",
    "hey": "नमस्कार",
    "namaste": "नमस्कार",
    "namaskar": "नमस्कार",
    "pranam": "प्रणाम",
    "how are you": "तुम्ही कसे आहात?",
    "how are you?": "तुम्ही कसे आहात?",
    "kaise ho": "तुम्ही कसे आहात?",
    "kaise ho?": "तुम्ही कसे आहात?",
    "kasa ahes": "तुम्ही कसे आहात?",
    "kasa ahes?": "तुम्ही कसे आहात?",
    "fine": "मी ठीक आहे",
    "i am fine": "मी ठीक आहे",
    "good": "छान",
    "ok": "ठीक आहे",
    "okay": "ठीक आहे",
    "yes": "होय",
    "no": "नाही",
    "ho": "होय",
    "nahi": "नाही",
    "nako": "नको",
    "thanks": "धन्यवाद",
    "thank you": "धन्यवाद",
    "dhanyawad": "धन्यवाद",
    "aabhar": "आभार",
    "what is the price": "दर काय आहे?",
    "what is the rate": "भाव काय आहे?",
    "what is the price?": "दर काय आहे?",
    "what is the rate?": "भाव काय आहे?",
    "bhav kay ahe": "भाव काय आहे?",
    "rate kay ahe": "दर काय आहे?",
    "best price": "सर्वोत्तम दर",
    "final price": "अंतिम दर",
    "available": "उपलब्ध",
    "not available": "उपलब्ध नाही",
    "deal confirmed": "सौदा पक्का झाला",
    "can you deliver": "तुम्ही डिलिव्हरी करू शकता का?",
    "can you deliver?": "तुम्ही डिलिव्हरी करू शकता का?",
    "ready for pickup": "घेऊन जाण्यासाठी तयार आहे",
    "hello, what is the best price for your wheat?": "नमस्कार, तुमच्या गव्हाचा सर्वोत्तम दर काय आहे?",
    "fresh organic tomatoes ready for pickup": "ताजे सेंद्रिय टोमॅटो घेऊन जाण्यासाठी तयार आहेत",
    "50 quintals available": "50 क्विंटल उपलब्ध आहे",
    "payment via upi or cash": "यूपीआय किंवा रोखीने पेमेंट",
    "mandi rate": "मार्केट दर"
}

COMMON_PHRASES_EN = {
    "hi": "Hello",
    "hii": "Hello",
    "hello": "Hello",
    "hey": "Hello",
    "namaste": "Hello / Greetings",
    "namaskar": "Hello / Greetings",
    "नमस्ते": "Hello",
    "नमस्कार": "Hello",
    "kaise ho": "How are you?",
    "kaise ho?": "How are you?",
    "kasa ahes": "How are you?",
    "आप कैसे हैं?": "How are you?",
    "तुम्ही कसे आहात?": "How are you?",
    "kya bhav hai": "What is the price?",
    "kya bhav hai?": "What is the price?",
    "kya rate hai": "What is the rate?",
    "भाव क्या है?": "What is the price?",
    "दर काय आहे?": "What is the rate?",
    "सौदा पक्का हुआ": "Deal confirmed",
    "सौदा पक्का झाला": "Deal confirmed",
    "उपलब्ध": "Available",
    "उपलब्ध नहीं है": "Not available",
    "धन्यवाद": "Thank you",
    "शुक्रिया": "Thank you",
    "आभार": "Thank you"
}

COMMON_PHRASES_TE = {
    "hi": "నమస్కారం",
    "hii": "నమస్కారం",
    "hello": "నమస్కారం",
    "what is the price": "ధర ఎంత?",
    "best price": "ఉత్తమ ధర",
    "available": "అందుబాటులో ఉంది",
    "deal confirmed": "డీల్ ఖరారైంది",
    "thank you": "ధన్యవాదాలు"
}

COMMON_PHRASES_TA = {
    "hi": "வணக்கம்",
    "hii": "வணக்கம்",
    "hello": "வணக்கம்",
    "what is the price": "விலை என்ன?",
    "best price": "சிறந்த விலை",
    "available": "கிடைக்கிறது",
    "deal confirmed": "ஒப்பந்தம் உறுதியானது",
    "thank you": "நன்றி"
}

COMMON_PHRASES_GU = {
    "hi": "નમસ્તે",
    "hii": "નમસ્તે",
    "hello": "નમસ્તે",
    "what is the price": "ભાવ શું છે?",
    "best price": "શ્રેષ્ઠ ભાવ",
    "available": "ઉપલબ્ધ",
    "deal confirmed": "સોદો પાકો થયો",
    "thank you": "આભાર"
}

COMMON_PHRASES_PA = {
    "hi": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ",
    "hii": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ",
    "hello": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ",
    "what is the price": "ਰੇਟ ਕੀ ਹੈ?",
    "best price": "ਵਧੀਆ ਰੇਟ",
    "available": "ਉਪਲਬਧ",
    "deal confirmed": "ਸੌਦਾ ਪੱਕਾ ਹੋ ਗਿਆ",
    "thank you": "ਧੰਨਵਾਦ"
}

COMMON_PHRASES_BN = {
    "hi": "নমস্কার",
    "hii": "নমস্কার",
    "hello": "নমস্কার",
    "what is the price": "দাম কত?",
    "best price": "সেরা দাম",
    "available": "উপলব্ধ",
    "deal confirmed": "চুক্তি চূড়ান্ত",
    "thank you": "ধন্যবাদ"
}

DICTIONARIES = {
    'hi': COMMON_PHRASES_HI,
    'mr': COMMON_PHRASES_MR,
    'en': COMMON_PHRASES_EN,
    'te': COMMON_PHRASES_TE,
    'ta': COMMON_PHRASES_TA,
    'gu': COMMON_PHRASES_GU,
    'pa': COMMON_PHRASES_PA,
    'bn': COMMON_PHRASES_BN
}

class TranslationService:
    @staticmethod
    def translate_text(text: str, target_lang: str = 'en') -> dict:
        """
        Translates chat text into the specified Indian regional or global language.
        Multi-tier architecture:
          1. In-memory response cache
          2. Curated Offline Agricultural & Greeting Dictionary (instant exact match)
          3. Google Gemini Flash (gemini-3.6-flash / gemini-3.5-flash / gemini-3.1-flash-lite)
          4. Robust Regional Fallback Dictionary
        """
        if not text or not text.strip():
            return {'success': True, 'translated_text': '', 'target_lang': target_lang}

        target_lang = (target_lang or 'en').lower().strip()
        cleaned_text = text.strip()
        cache_key = f"{target_lang}:{cleaned_text}"

        if cache_key in _translation_cache:
            return _translation_cache[cache_key]

        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang.title())
        normalized_lower = cleaned_text.lower().strip()

        # Tier 1: Check curated dictionary for instant exact greeting / trading phrase
        target_dict = DICTIONARIES.get(target_lang, {})
        if normalized_lower in target_dict:
            res = {
                'success': True,
                'translated_text': target_dict[normalized_lower],
                'detected_source_lang': 'Auto-detected',
                'target_lang': target_lang,
                'target_lang_name': target_lang_name,
                'is_dictionary': True
            }
            _translation_cache[cache_key] = res
            return res

        # If source is already in English and target is English
        if target_lang == 'en' and re.match(r'^[a-zA-Z0-9\s.,!?:;\-\'\"%₹]+$', cleaned_text):
            # Check if it was an Indian greeting transcribed in English (e.g. "namaste", "kasa ahes")
            if normalized_lower in COMMON_PHRASES_EN:
                trans = COMMON_PHRASES_EN[normalized_lower]
            else:
                trans = cleaned_text
            res = {
                'success': True,
                'translated_text': trans,
                'detected_source_lang': 'English',
                'target_lang': target_lang,
                'target_lang_name': target_lang_name,
                'is_passthrough': True
            }
            _translation_cache[cache_key] = res
            return res

        api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

        # Tier 2: Gemini Flash GenAI
        if api_key:
            prompt = f"""You are a professional agricultural trade translator for Krishi Kendra (India).
Translate the following farmer/buyer chat message accurately into {target_lang_name}.
Preserve commodity names, quantities, units (e.g. quintal, kg, acre), and prices accurately with a polite and professional tone.
Never include adult, spam, or inappropriate text.

MESSAGE:
"{cleaned_text}"

Return STRICTLY a JSON object with this exact format:
{{
  "translated_text": "<accurate natural translation in {target_lang_name} script>",
  "detected_source_lang": "<source language e.g. English, Hindi, Marathi, Hinglish>"
}}
"""
            model_candidates = [
                'gemini-3.6-flash',
                'gemini-3.5-flash',
                'gemini-3.1-flash-lite',
                'gemini-flash-latest',
                'gemini-3.7-flash'
            ]

            for model_candidate in model_candidates:
                try:
                    from google import genai
                    from google.genai import types

                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model=model_candidate,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.1,
                            max_output_tokens=300
                        )
                    )

                    text_out = response.text.strip()
                    if text_out.startswith("```"):
                        text_out = text_out.strip("`").replace("json\n", "", 1).strip()

                    data = json.loads(text_out)
                    translated = data.get('translated_text', '').strip()

                    # Safety check: ensure no spam/inappropriate content
                    if translated and not contains_spam(translated):
                        source_lang = data.get('detected_source_lang', 'Auto-detected')
                        result = {
                            'success': True,
                            'translated_text': translated,
                            'detected_source_lang': source_lang,
                            'target_lang': target_lang,
                            'target_lang_name': target_lang_name,
                            'is_ai': True,
                            'model': model_candidate
                        }
                        _translation_cache[cache_key] = result
                        return result

                except Exception as e:
                    logger.debug(f"Translation model {model_candidate} attempt note: {e}")
                    continue

        # Tier 3: Safe Fallback Dictionary Lookup
        fallback_translated = cleaned_text
        if target_lang in DICTIONARIES:
            fallback_translated = DICTIONARIES[target_lang].get(normalized_lower, cleaned_text)

        fallback_res = {
            'success': True,
            'translated_text': fallback_translated,
            'target_lang': target_lang,
            'target_lang_name': target_lang_name,
            'is_fallback': True
        }
        return fallback_res
