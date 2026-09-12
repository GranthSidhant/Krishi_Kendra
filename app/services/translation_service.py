import os
import json
import logging
import time

logger = logging.getLogger(__name__)

# In-memory translation cache to guarantee sub-100ms response for repeated messages
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

class TranslationService:
    @staticmethod
    def translate_text(text: str, target_lang: str = 'en') -> dict:
        """
        Translates chat text into the specified Indian regional or global language using Gemini Flash.
        Includes fast in-memory caching and resilient fallback.
        """
        if not text or not text.strip():
            return {'success': True, 'translated_text': '', 'target_lang': target_lang}

        target_lang = (target_lang or 'en').lower()
        cache_key = f"{target_lang}:{text.strip()}"
        if cache_key in _translation_cache:
            return _translation_cache[cache_key]

        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            res = {
                'success': True,
                'translated_text': text,
                'target_lang': target_lang,
                'target_lang_name': target_lang_name,
                'is_fallback': True
            }
            return res

        prompt = f"""You are a professional agricultural trade translator on Krishi Kendra.
Translate the following chat message accurately into {target_lang_name} while preserving agricultural commodity terminology, prices, quantities, and respectful tone.

MESSAGE:
"{text}"

Return STRICTLY a JSON object with this format:
{{
  "translated_text": "<accurate translation in {target_lang_name} script>",
  "detected_source_lang": "<source language e.g. English, Hindi, Marathi>"
}}
"""

        for model_candidate in ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-flash-latest']:
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
                        max_output_tokens=250
                    )
                )

                text_out = response.text.strip()
                if text_out.startswith("```"):
                    text_out = text_out.strip("`").replace("json\n", "", 1).strip()

                data = json.loads(text_out)
                translated = data.get('translated_text', text)
                source_lang = data.get('detected_source_lang', 'Auto-detected')

                result = {
                    'success': True,
                    'translated_text': translated,
                    'detected_source_lang': source_lang,
                    'target_lang': target_lang,
                    'target_lang_name': target_lang_name,
                    'is_ai': True
                }

                _translation_cache[cache_key] = result
                return result

            except Exception as e:
                logger.warning(f"Translation model {model_candidate} attempt note: {e}")
                continue

        # Fallback if API unavailable
        fallback_res = {
            'success': True,
            'translated_text': text,
            'target_lang': target_lang,
            'target_lang_name': target_lang_name,
            'is_fallback': True
        }
        return fallback_res
