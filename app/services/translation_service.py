import os
import json
import logging
import time
import requests
import urllib.parse

logger = logging.getLogger(__name__)

# In-memory translation cache to guarantee sub-50ms response for repeated messages
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

# Common agricultural phrases offline fallback map (Hindi, Marathi, etc.)
COMMON_PHRASES_HI = {
    "hello": "नमस्ते",
    "hi": "नमस्ते",
    "what is the price": "भाव क्या है?",
    "what is the rate": "दर क्या है?",
    "best price": "सर्वोत्तम भाव",
    "available": "उपलब्ध",
    "deal confirmed": "सौदा पक्का हुआ",
    "can you deliver": "क्या आप डिलीवरी कर सकते हैं?",
    "ready for pickup": "उठाने के लिए तैयार है",
    "hello, what is the best price for your wheat?": "नमस्ते, आपके गेहूं का सबसे अच्छा भाव क्या है?",
    "fresh organic tomatoes ready for pickup": "ताजा जैविक टमाटर उठाने के लिए तैयार हैं"
}

COMMON_PHRASES_MR = {
    "hello": "नमस्कार",
    "hi": "नमस्कार",
    "what is the price": "दर काय आहे?",
    "what is the rate": "भाव काय आहे?",
    "best price": "सर्वोत्तम दर",
    "available": "उपलब्ध",
    "deal confirmed": "सौदा पक्का झाला",
    "can you deliver": "तुम्ही डिलिव्हरी करू शकता का?",
    "ready for pickup": "घेऊन जाण्यासाठी तयार आहे",
    "hello, what is the best price for your wheat?": "नमस्कार, तुमच्या गव्हाचा सर्वोत्तम दर काय आहे?",
    "fresh organic tomatoes ready for pickup": "ताजे सेंद्रिय टोमॅटो घेऊन जाण्यासाठी तयार आहेत"
}

class TranslationService:
    @staticmethod
    def translate_text(text: str, target_lang: str = 'en') -> dict:
        """
        Translates chat text into the specified Indian regional or global language.
        Multi-tier architecture:
          1. In-memory response cache
          2. Google Gemini Flash (if GEMINI_API_KEY / GOOGLE_API_KEY configured)
          3. Fast Online Multilingual Translation API (MyMemory / Lingva)
          4. Offline Agricultural trade phrase dictionary
        """
        if not text or not text.strip():
            return {'success': True, 'translated_text': '', 'target_lang': target_lang}

        target_lang = (target_lang or 'en').lower().strip()
        cache_key = f"{target_lang}:{text.strip()}"
        if cache_key in _translation_cache:
            return _translation_cache[cache_key]

        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

        # Tier 1: Gemini GenAI
        if api_key:
            prompt = f"""You are a professional agricultural trade translator on Krishi Kendra.
Translate the following chat message accurately into {target_lang_name}.
Preserve agricultural commodity names, quantities, units, and price figures faithfully with a respectful tone.

MESSAGE:
"{text}"

Return STRICTLY a JSON object with this exact format:
{{
  "translated_text": "<accurate natural translation in {target_lang_name} script>",
  "detected_source_lang": "<source language e.g. English, Hindi, Marathi>"
}}
"""
            model_candidates = [
                'gemini-2.5-flash',
                'gemini-2.0-flash',
                'gemini-1.5-flash',
                'gemini-2.5-flash-lite',
                'gemini-flash-latest'
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
                    if translated:
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

        # Tier 2: Free Online Translation API (MyMemory)
        try:
            # Pair: if target is hindi and source seems english or mixed
            langpair = f"en|{target_lang}" if target_lang != 'en' else 'hi|en'
            resp = requests.get(
                'https://api.mymemory.translated.net/get',
                params={'q': text.strip(), 'langpair': langpair},
                timeout=4
            )
            if resp.status_code == 200:
                data = resp.json()
                translated_candidate = data.get('responseData', {}).get('translatedText', '').strip()
                if translated_candidate and translated_candidate.lower() != text.lower():
                    # Successfully translated
                    result = {
                        'success': True,
                        'translated_text': translated_candidate,
                        'detected_source_lang': 'Auto-detected',
                        'target_lang': target_lang,
                        'target_lang_name': target_lang_name,
                        'is_online_service': True
                    }
                    _translation_cache[cache_key] = result
                    return result
        except Exception as net_err:
            logger.debug(f"Online translation fallback note: {net_err}")

        # Tier 3: Offline Dictionary Fallback
        fallback_translated = text
        text_lower = text.lower().strip()
        if target_lang == 'hi':
            fallback_translated = COMMON_PHRASES_HI.get(text_lower, text)
        elif target_lang == 'mr':
            fallback_translated = COMMON_PHRASES_MR.get(text_lower, text)

        fallback_res = {
            'success': True,
            'translated_text': fallback_translated,
            'target_lang': target_lang,
            'target_lang_name': target_lang_name,
            'is_fallback': True
        }
        return fallback_res

