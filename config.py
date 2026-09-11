import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'krishi-kendra-sih2026-super-secret-key-xyz987')
    
    # In Vercel serverless, the filesystem is read-only except /tmp
    if IS_VERCEL:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{Path('/tmp') / 'krishi_kendra.db'}")
        UPLOAD_FOLDER = Path('/tmp') / 'uploads'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'instance' / 'krishi_kendra.db'}")
        UPLOAD_FOLDER = BASE_DIR / 'app' / 'static' / 'uploads'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Dev OTP mode (set to True to enable on-screen demo OTP '123456')
    DEV_OTP_MODE = os.environ.get('DEV_OTP_MODE', 'True').lower() in ('true', '1', 't')
    DEFAULT_DEV_OTP = "123456"
    
    # JWT / Session
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'krishi-jwt-sih-secret-2026')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Multi-language configuration
    LANGUAGES = {
        'en': 'English',
        'hi': 'हिन्दी (Hindi)',
        'mr': 'मराठी (Marathi)',
        'ta': 'தமிழ் (Tamil)',
        'te': 'తెలుగు (Telugu)'
    }
    DEFAULT_LANGUAGE = 'en'
