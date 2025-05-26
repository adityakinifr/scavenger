#!/usr/bin/env python3
"""
Startup script for the Twilio Flask app.
This script checks configuration and starts the app.
"""

import os
import sys
from config import Config

def check_environment():
    """Check if the environment is properly configured."""
    print("🔍 Checking environment configuration...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found.")
        print("📝 Please create a .env file with your Twilio credentials.")
        print("   You can copy env_template.txt to .env and fill in your credentials.")
        return False
    
    # Check Twilio configuration
    missing = Config.validate_twilio_config()
    if missing:
        print("❌ Missing required Twilio configuration:")
        for item in missing:
            print(f"   - {item}")
        print("\n📝 Please check your .env file and add the missing credentials.")
        return False
    
    print("✅ Environment configuration looks good!")
    print(f"   Account SID: {Config.TWILIO_ACCOUNT_SID[:8]}...")
    print(f"   Phone Number: {Config.TWILIO_PHONE_NUMBER}")
    return True

def main():
    """Main startup function."""
    print("🚀 Starting Twilio Flask App\n")
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Get port from environment (Codespaces sets this)
    port = int(os.environ.get('PORT', 5000))
    
    print("\n🌟 Starting Flask application...")
    print(f"   Port: {port}")
    
    # Check if we're in Codespaces
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        print(f"   🚀 Running in GitHub Codespaces: {codespace_name}")
        print(f"   🌐 Your app will be available at the forwarded port URL")
        print("   📝 GitHub will automatically forward port 5000 and show you the URL")
    else:
        print(f"   URL: http://localhost:{port}")
    
    print("   Press Ctrl+C to stop\n")
    
    # Import and run the app
    try:
        from app import app
        app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error starting app: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 