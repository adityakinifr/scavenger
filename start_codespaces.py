#!/usr/bin/env python3
"""
GitHub Codespaces optimized startup script for Portland Scavenger Hunt Bot
Handles environment detection, port configuration, and provides helpful setup guidance.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Detect if we're running in GitHub Codespaces."""
    return os.environ.get('CODESPACES') == 'true'

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        import twilio
        import openai
        from dotenv import load_dotenv
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("Creating .env file from template...")
        
        # Copy template to .env
        template_path = Path('env_template.txt')
        if template_path.exists():
            with open(template_path, 'r') as template:
                content = template.read()
            
            with open('.env', 'w') as env_file:
                env_file.write(content)
            
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your actual API keys")
            return False
        else:
            print("❌ env_template.txt not found")
            return False
    
    # Check for required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_PHONE_NUMBER'
    ]
    
    optional_vars = [
        'OPENAI_API_KEY'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.environ.get(var) or os.environ.get(var).startswith('your_'):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.environ.get(var) or os.environ.get(var).startswith('your_'):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️  Missing optional environment variables: {', '.join(missing_optional)}")
        print("   OpenAI integration will use fallback string matching")
    
    print("✅ Environment variables configured")
    return True

def get_codespace_info():
    """Get Codespace-specific information."""
    if not check_environment():
        return None
    
    codespace_name = os.environ.get('CODESPACE_NAME', 'unknown')
    github_user = os.environ.get('GITHUB_USER', 'unknown')
    
    # Construct the likely URL (GitHub provides this in a specific format)
    base_url = f"https://{codespace_name}-5000.app.github.dev"
    
    return {
        'name': codespace_name,
        'user': github_user,
        'url': base_url,
        'webhook_sms': f"{base_url}/webhook/sms",
        'webhook_voice': f"{base_url}/webhook/voice"
    }

def print_setup_instructions():
    """Print setup instructions for the Portland Scavenger Hunt."""
    print("\n" + "="*60)
    print("🎯 PORTLAND SCAVENGER HUNT BOT SETUP")
    print("="*60)
    
    codespace_info = get_codespace_info()
    
    if codespace_info:
        print(f"🌐 Codespace: {codespace_info['name']}")
        print(f"👤 User: {codespace_info['user']}")
        print(f"🔗 App URL: {codespace_info['url']}")
        print()
        print("📱 TWILIO WEBHOOK CONFIGURATION:")
        print(f"   SMS Webhook: {codespace_info['webhook_sms']}")
        print(f"   Voice Webhook: {codespace_info['webhook_voice']}")
        print()
        print("⚠️  IMPORTANT: Make sure port 5000 is set to 'Public' in the Ports tab!")
    
    print("\n🎮 GAME FEATURES:")
    print("   • 5 Portland locations to discover")
    print("   • OpenAI-powered natural language processing")
    print("   • Progressive hint system (3 hints per clue)")
    print("   • Dynamic scoring: 40→30→20→10 points")
    print("   • Player tracking and leaderboards")
    
    print("\n🔑 REQUIRED API KEYS:")
    print("   1. Twilio Account SID, Auth Token, Phone Number")
    print("      Get from: https://console.twilio.com/")
    print("   2. OpenAI API Key (optional but recommended)")
    print("      Get from: https://platform.openai.com/")
    
    print("\n📝 SETUP STEPS:")
    print("   1. Edit .env file with your API keys")
    print("   2. Configure Twilio webhooks (URLs shown above)")
    print("   3. Make sure Codespace port 5000 is Public")
    print("   4. Test by sending 'READY' to your Twilio number")
    
    print("\n🎯 GAME COMMANDS:")
    print("   • READY - Start the scavenger hunt")
    print("   • STATUS - Check progress and score")
    print("   • HELP - Get game instructions")
    print("   • QUIT - Exit current game")
    
    print("\n🌲 PORTLAND LOCATIONS:")
    print("   1. International Rose Test Garden")
    print("   2. Powell's City of Books")
    print("   3. Voodoo Doughnut")
    print("   4. Pioneer Courthouse Square")
    print("   5. Tom McCall Waterfront Park")

def run_tests():
    """Run the scavenger hunt test suite."""
    print("\n🧪 Running Portland Scavenger Hunt Tests...")
    try:
        result = subprocess.run([sys.executable, "test_scavenger_game.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️  test_scavenger_game.py not found, skipping tests")
        return True

def start_app():
    """Start the Flask application."""
    print("\n🚀 Starting Portland Scavenger Hunt Bot...")
    
    # Set environment variables for Codespaces
    os.environ['FLASK_ENV'] = 'development'
    port = int(os.environ.get('PORT', 5000))
    
    try:
        from app import app
        print(f"✅ Flask app loaded successfully")
        print(f"🌐 Starting server on port {port}")
        
        if check_environment():
            print("📱 Your Codespace is ready for Twilio webhooks!")
            print("🎯 Send 'READY' to your Twilio number to start the game!")
        
        # Start the Flask app
        app.run(debug=True, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
        return False

def main():
    """Main startup sequence."""
    print("🎯 Portland Scavenger Hunt Bot - Codespaces Startup")
    print("="*55)
    
    # Check if we're in Codespaces
    if check_environment():
        print("✅ Running in GitHub Codespaces")
    else:
        print("⚠️  Not detected as Codespaces environment")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return 1
    
    # Check environment file
    env_ready = check_env_file()
    
    # Print setup instructions
    print_setup_instructions()
    
    if not env_ready:
        print("\n⚠️  Please configure your .env file before starting the app")
        print("   Edit .env and add your Twilio and OpenAI API keys")
        return 1
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but continuing anyway...")
    
    # Start the application
    try:
        start_app()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Portland Scavenger Hunt Bot")
        return 0
    except Exception as e:
        print(f"\n❌ Startup failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 