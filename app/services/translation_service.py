import os
import json
import logging
import time

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

# Common agricultural phrases offline fallback map (Hindi / Marathi)
COMMON_PHRASES_HI = {
    "hello": "नमस्ते",
    "hi": "नमस्ते",
    "what is the price": "भाव क्या है?",
    "what is the rate": "दर क्या है?",
    "best price": "सर्वोत्तम भाव",
    "available": "उपलब्ध",
    "deal confirmed": "सौदा पक्का हुआ",
    "can you deliver": "क्या आप डिलीवरी कर सकते हैं?",
    "ready for pickup": "उठाने के लिए तैयार है"
}

class TranslationService:
    @staticmethod
    def translate_text(text: str, target_lang: str = 'en') -> dict:
        """
        Translates chat text into the specified Indian regional or global language using Gemini Flash.
        Includes fast in-memory caching, modern model fallbacks, and agricultural domain context.
        """
        if not text or not text.strip():
            return {'success': True, 'translated_text': '', 'target_lang': target_lang}

        target_lang = (target_lang or 'en').lower().strip()
        cache_key = f"{target_lang}:{text.strip()}"
        if cache_key in _translation_cache:
            return _translation_cache[cache_key]

        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

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

        # Fallback if API unavailable
        fallback_translated = text
        text_lower = text.lower().strip()
        if target_lang == 'hi' and text_lower in COMMON_PHRASES_HI:
            fallback_translated = COMMON_PHRASES_HI[text_lower]

        fallback_res = {
            'success': True,
            'translated_text': fallback_translated,
            'target_lang': target_lang,
            'target_lang_name': target_lang_name,
            'is_fallback': True
        }
        return fallback_res
