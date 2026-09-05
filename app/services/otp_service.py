import random
from flask import current_app, session

# In-memory store for active OTPs during demo/runtime
_OTP_STORE = {}

class OTPService:
    @staticmethod
    def generate_otp(phone: str) -> str:
        """
        Generates a 6-digit OTP. In DEV mode, uses DEFAULT_DEV_OTP or returns a fixed 6-digit code.
        """
        dev_mode = current_app.config.get('DEV_OTP_MODE', True)
        if dev_mode:
            otp = current_app.config.get('DEFAULT_DEV_OTP', '123456')
        else:
            otp = str(random.randint(100000, 999999))
            
        _OTP_STORE[phone] = {
            'otp': otp,
            'verified': False
        }
        return otp

    @staticmethod
    def verify_otp(phone: str, entered_otp: str) -> bool:
        """
        Verifies the OTP for the given phone number.
        """
        dev_mode = current_app.config.get('DEV_OTP_MODE', True)
        # In dev mode, always accept default demo OTP '123456'
        if dev_mode and entered_otp == current_app.config.get('DEFAULT_DEV_OTP', '123456'):
            if phone in _OTP_STORE:
                _OTP_STORE[phone]['verified'] = True
            return True
            
        record = _OTP_STORE.get(phone)
        if record and record['otp'] == entered_otp.strip():
            record['verified'] = True
            return True
        return False

    @staticmethod
    def is_verified(phone: str) -> bool:
        return _OTP_STORE.get(phone, {}).get('verified', False)

    @staticmethod
    def clear_otp(phone: str):
        if phone in _OTP_STORE:
            del _OTP_STORE[phone]
