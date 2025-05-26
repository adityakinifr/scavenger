#!/usr/bin/env python3
"""
GitHub Codespaces startup script for the Twilio Flask app.
This script is optimized for running in GitHub Codespaces environment.
"""

import os
import sys
import subprocess
from config import Config

def get_codespace_info():
    """Get information about the current Codespace."""
    codespace_name = os.environ.get('CODESPACE_NAME')
    github_user = os.environ.get('GITHUB_USER')
    port = int(os.environ.get('PORT', 5000))
    
    return {
        'name': codespace_name,
        'user': github_user,
        'port': port,
        'is_codespace': bool(codespace_name)
    }

def check_environment():
    """Check if the environment is properly configured for Codespaces."""
    print("🔍 Checking GitHub Codespaces environment...")
    
    info = get_codespace_info()
    
    if info['is_codespace']:
        print(f"✅ Running in GitHub Codespaces: {info['name']}")
        print(f"👤 GitHub User: {info['user']}")
        print(f"🔌 Port: {info['port']}")
    else:
        print("⚠️  Not running in GitHub Codespaces")
        print("   This script is optimized for Codespaces but will work locally too.")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n📝 No .env file found.")
        print("   Creating a template .env file for you...")
        
        # Create .env from template
        try:
            with open('env_template.txt', 'r') as template:
                content = template.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ Created .env file from template")
            print("   Please edit .env and add your Twilio credentials")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    # Check Twilio configuration
    missing = Config.validate_twilio_config()
    if missing:
        print(f"\n⚠️  Missing Twilio configuration: {missing}")
        print("   The app will start but some features won't work until you add credentials.")
        return True  # Allow app to start anyway
    
    print("✅ Twilio configuration found!")
    print(f"   Account SID: {Config.TWILIO_ACCOUNT_SID[:8]}...")
    print(f"   Phone Number: {Config.TWILIO_PHONE_NUMBER}")
    return True

def show_codespace_instructions():
    """Show instructions specific to GitHub Codespaces."""
    info = get_codespace_info()
    
    print("\n" + "="*60)
    print("🚀 GITHUB CODESPACES SETUP COMPLETE!")
    print("="*60)
    
    if info['is_codespace']:
        print(f"📱 Your Twilio Flask app is running in Codespace: {info['name']}")
        print(f"🔌 Port {info['port']} is automatically forwarded by GitHub")
        print("\n🌐 TO ACCESS YOUR APP:")
        print("   1. Look for the 'Ports' tab in VS Code (next to Terminal)")
        print("   2. Find port 5000 and click the 'Open in Browser' icon")
        print("   3. Or use the forwarded URL that GitHub provides")
        
        print("\n📞 TO SET UP TWILIO WEBHOOKS:")
        print("   1. Copy the forwarded URL from the Ports tab")
        print("   2. Go to Twilio Console > Phone Numbers")
        print("   3. Set SMS webhook to: [YOUR_URL]/webhook/sms")
        print("   4. Set Voice webhook to: [YOUR_URL]/webhook/voice")
        
        print("\n🔧 TO ADD TWILIO CREDENTIALS:")
        print("   1. Edit the .env file in this Codespace")
        print("   2. Add your Twilio Account SID, Auth Token, and Phone Number")
        print("   3. Restart the app with: python start_codespaces.py")
    else:
        print("🖥️  Running locally - see README.md for local setup instructions")
    
    print("\n📚 USEFUL ENDPOINTS:")
    print("   GET  /           - API information")
    print("   GET  /messages   - Message history")
    print("   GET  /calls      - Call history")
    print("   POST /send-sms   - Send SMS message")
    print("   GET  /twilio-data - Fetch data from Twilio account")
    
    print("\n🧪 TO TEST YOUR SETUP:")
    print("   Run: python test_app.py")
    
    print("\n" + "="*60)

def main():
    """Main startup function for Codespaces."""
    print("🚀 Starting Twilio Flask App in GitHub Codespaces\n")
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed.")
        sys.exit(1)
    
    # Show Codespaces-specific instructions
    show_codespace_instructions()
    
    print("\n🌟 Starting Flask application...")
    print("   Press Ctrl+C to stop")
    print("   Use the Ports tab in VS Code to access your app\n")
    
    # Get port from environment
    port = int(os.environ.get('PORT', 5000))
    
    # Import and run the app
    try:
        from app import app
        app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        print("   Your Codespace will remain active for future use.")
    except Exception as e:
        print(f"\n❌ Error starting app: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 