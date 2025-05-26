"""
Webhook validation utilities for Twilio.
Use this in production to validate that webhooks are actually from Twilio.
"""

import hashlib
import hmac
import base64
from urllib.parse import urlencode
from flask import request
from config import Config

def validate_twilio_signature(url, post_vars, signature):
    """
    Validate that a webhook request is from Twilio.
    
    Args:
        url (str): The full URL of the webhook endpoint
        post_vars (dict): POST parameters from the request
        signature (str): X-Twilio-Signature header value
    
    Returns:
        bool: True if signature is valid, False otherwise
    """
    if not Config.TWILIO_AUTH_TOKEN:
        return False
    
    # Create the signature string
    signature_string = url
    if post_vars:
        # Sort parameters and append to URL
        sorted_params = sorted(post_vars.items())
        signature_string += urlencode(sorted_params)
    
    # Create HMAC-SHA1 signature
    mac = hmac.new(
        Config.TWILIO_AUTH_TOKEN.encode('utf-8'),
        signature_string.encode('utf-8'),
        hashlib.sha1
    )
    
    # Compare with provided signature
    expected_signature = base64.b64encode(mac.digest()).decode('utf-8')
    return hmac.compare_digest(expected_signature, signature)

def validate_request():
    """
    Validate the current Flask request is from Twilio.
    
    Returns:
        bool: True if request is valid, False otherwise
    """
    # Get the signature from headers
    signature = request.headers.get('X-Twilio-Signature', '')
    
    # Get the full URL
    url = request.url
    
    # Get POST parameters
    post_vars = request.form.to_dict()
    
    return validate_twilio_signature(url, post_vars, signature)

def require_twilio_signature(f):
    """
    Decorator to require valid Twilio signature on webhook endpoints.
    Use this in production to secure your webhooks.
    
    Usage:
        @app.route('/webhook/sms', methods=['POST'])
        @require_twilio_signature
        def sms_webhook():
            # Your webhook code here
    """
    def decorated_function(*args, **kwargs):
        if not validate_request():
            return 'Unauthorized', 403
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function 