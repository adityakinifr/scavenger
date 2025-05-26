#!/usr/bin/env python3
"""
Test script for the Twilio Flask app.
Run this to verify your setup is working correctly.
"""

import requests
import json
import os
from config import Config

def test_app_running():
    """Test if the Flask app is running."""
    # Get port from environment
    port = int(os.environ.get('PORT', 5000))
    base_url = f'http://localhost:{port}'
    
    try:
        response = requests.get(f'{base_url}/')
        if response.status_code == 200:
            print("✅ Flask app is running successfully!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Flask app returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Flask app. Make sure it's running on localhost:{port}")
        return False

def test_config():
    """Test if Twilio configuration is set up."""
    missing = Config.validate_twilio_config()
    if not missing:
        print("✅ Twilio configuration is complete!")
        print(f"Account SID: {Config.TWILIO_ACCOUNT_SID[:8]}...")
        print(f"Phone Number: {Config.TWILIO_PHONE_NUMBER}")
        return True
    else:
        print("❌ Missing Twilio configuration:")
        for item in missing:
            print(f"  - {item}")
        print("\nPlease create a .env file with your Twilio credentials.")
        return False

def test_endpoints():
    """Test various app endpoints."""
    port = int(os.environ.get('PORT', 5000))
    base_url = f'http://localhost:{port}'
    endpoints = [
        ('GET', '/messages', 'Message history'),
        ('GET', '/calls', 'Call history'),
    ]
    
    print("\nTesting endpoints:")
    for method, endpoint, description in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {description} ({endpoint}): OK")
            else:
                print(f"❌ {description} ({endpoint}): Status {response.status_code}")
        except Exception as e:
            print(f"❌ {description} ({endpoint}): Error - {str(e)}")

def test_twilio_data():
    """Test fetching data from Twilio account."""
    port = int(os.environ.get('PORT', 5000))
    try:
        response = requests.get(f'http://localhost:{port}/twilio-data')
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully connected to Twilio account!")
            print(f"Recent messages: {len(data.get('messages', []))}")
            print(f"Recent calls: {len(data.get('calls', []))}")
            return True
        else:
            print(f"❌ Failed to fetch Twilio data: {response.status_code}")
            if response.status_code == 500:
                print("This might be due to missing Twilio credentials.")
            return False
    except Exception as e:
        print(f"❌ Error testing Twilio data: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Twilio Flask App Setup\n")
    
    # Test configuration
    config_ok = test_config()
    print()
    
    # Test if app is running
    app_running = test_app_running()
    print()
    
    if app_running:
        # Test endpoints
        test_endpoints()
        print()
        
        # Test Twilio connection (only if config is OK)
        if config_ok:
            test_twilio_data()
        else:
            print("⚠️  Skipping Twilio data test due to missing configuration.")
    
    print("\n" + "="*50)
    if app_running and config_ok:
        print("🎉 Setup looks good! Your Twilio Flask app is ready to use.")
        print("\nNext steps:")
        print("1. Use ngrok to expose your local server: ngrok http 5000")
        print("2. Configure webhooks in Twilio Console with your ngrok URL")
        print("3. Send an SMS to your Twilio number to test!")
    else:
        print("⚠️  Some issues found. Please check the errors above.")
        if not config_ok:
            print("\n📝 To fix configuration issues:")
            print("1. Create a .env file in the project root")
            print("2. Add your Twilio credentials (see README.md for details)")
        if not app_running:
            print("\n🚀 To start the Flask app:")
            print("python app.py")

if __name__ == '__main__':
    main() 