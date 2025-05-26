import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Flask app."""
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Webhook URLs (for reference)
    SMS_WEBHOOK_URL = '/webhook/sms'
    VOICE_WEBHOOK_URL = '/webhook/voice'
    
    @classmethod
    def validate_twilio_config(cls):
        """Validate that required Twilio configuration is present."""
        missing = []
        if not cls.TWILIO_ACCOUNT_SID:
            missing.append('TWILIO_ACCOUNT_SID')
        if not cls.TWILIO_AUTH_TOKEN:
            missing.append('TWILIO_AUTH_TOKEN')
        if not cls.TWILIO_PHONE_NUMBER:
            missing.append('TWILIO_PHONE_NUMBER')
        
        return missing 