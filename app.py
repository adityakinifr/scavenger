from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os
from datetime import datetime
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Twilio client
if Config.TWILIO_ACCOUNT_SID and Config.TWILIO_AUTH_TOKEN:
    twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    logger.info("Twilio client initialized successfully")
else:
    twilio_client = None
    missing_config = Config.validate_twilio_config()
    logger.warning(f"Twilio credentials not found: {missing_config}. Some features may not work.")

# In-memory storage for demonstration (use a database in production)
message_history = []
call_history = []

@app.route('/')
def home():
    """Home page with basic information about the app."""
    return jsonify({
        "message": "Twilio Flask App",
        "description": "A Flask app that integrates with Twilio to handle SMS and voice calls",
        "endpoints": {
            "sms_webhook": "/webhook/sms",
            "voice_webhook": "/webhook/voice",
            "send_sms": "/send-sms",
            "get_messages": "/messages",
            "get_calls": "/calls"
        }
    })

@app.route('/webhook/sms', methods=['POST'])
def sms_webhook():
    """Handle incoming SMS messages from Twilio."""
    try:
        # Get message data from Twilio
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        message_body = request.form.get('Body')
        message_sid = request.form.get('MessageSid')
        
        # Log the incoming message
        logger.info(f"Received SMS from {from_number}: {message_body}")
        
        # Store message in history
        message_data = {
            "sid": message_sid,
            "from": from_number,
            "to": to_number,
            "body": message_body,
            "timestamp": datetime.now().isoformat(),
            "direction": "inbound"
        }
        message_history.append(message_data)
        
        # Create response based on message content
        response = MessagingResponse()
        reply_message = generate_sms_response(message_body, from_number)
        response.message(reply_message)
        
        # Log the response
        logger.info(f"Responding to {from_number}: {reply_message}")
        
        return str(response)
    
    except Exception as e:
        logger.error(f"Error processing SMS webhook: {str(e)}")
        response = MessagingResponse()
        response.message("Sorry, I encountered an error processing your message.")
        return str(response)

@app.route('/webhook/voice', methods=['POST'])
def voice_webhook():
    """Handle incoming voice calls from Twilio."""
    try:
        # Get call data from Twilio
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        call_sid = request.form.get('CallSid')
        call_status = request.form.get('CallStatus')
        
        # Log the incoming call
        logger.info(f"Received call from {from_number}, status: {call_status}")
        
        # Store call in history
        call_data = {
            "sid": call_sid,
            "from": from_number,
            "to": to_number,
            "status": call_status,
            "timestamp": datetime.now().isoformat(),
            "direction": "inbound"
        }
        call_history.append(call_data)
        
        # Create voice response
        response = VoiceResponse()
        
        # Generate voice response based on caller
        voice_message = generate_voice_response(from_number)
        response.say(voice_message, voice='alice')
        
        # Optionally gather input
        gather = response.gather(
            input='speech dtmf',
            timeout=10,
            action='/webhook/voice/gather',
            method='POST'
        )
        gather.say("Press any key or say something after the beep.", voice='alice')
        
        # Fallback if no input
        response.say("Thank you for calling. Goodbye!", voice='alice')
        response.hangup()
        
        return str(response)
    
    except Exception as e:
        logger.error(f"Error processing voice webhook: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, I encountered an error. Please try again later.", voice='alice')
        response.hangup()
        return str(response)

@app.route('/webhook/voice/gather', methods=['POST'])
def voice_gather():
    """Handle gathered input from voice calls."""
    try:
        speech_result = request.form.get('SpeechResult', '')
        digits = request.form.get('Digits', '')
        from_number = request.form.get('From')
        
        logger.info(f"Gathered from {from_number} - Speech: {speech_result}, Digits: {digits}")
        
        response = VoiceResponse()
        
        if speech_result:
            reply = f"You said: {speech_result}. Thank you for your input!"
        elif digits:
            reply = f"You pressed: {digits}. Thank you!"
        else:
            reply = "I didn't catch that. Thank you for calling!"
        
        response.say(reply, voice='alice')
        response.hangup()
        
        return str(response)
    
    except Exception as e:
        logger.error(f"Error processing voice gather: {str(e)}")
        response = VoiceResponse()
        response.say("Thank you for calling. Goodbye!", voice='alice')
        response.hangup()
        return str(response)

@app.route('/send-sms', methods=['POST'])
def send_sms():
    """Send an SMS message via Twilio."""
    try:
        if not twilio_client:
            return jsonify({"error": "Twilio client not configured"}), 500
        
        data = request.get_json()
        to_number = data.get('to')
        message_body = data.get('message')
        
        if not to_number or not message_body:
            return jsonify({"error": "Missing 'to' or 'message' parameter"}), 400
        
        # Send message via Twilio
        message = twilio_client.messages.create(
            body=message_body,
            from_=Config.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        
        # Store in history
        message_data = {
            "sid": message.sid,
            "from": Config.TWILIO_PHONE_NUMBER,
            "to": to_number,
            "body": message_body,
            "timestamp": datetime.now().isoformat(),
            "direction": "outbound"
        }
        message_history.append(message_data)
        
        logger.info(f"Sent SMS to {to_number}: {message_body}")
        
        return jsonify({
            "success": True,
            "message_sid": message.sid,
            "status": message.status
        })
    
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get message history."""
    return jsonify({
        "messages": message_history,
        "count": len(message_history)
    })

@app.route('/calls', methods=['GET'])
def get_calls():
    """Get call history."""
    return jsonify({
        "calls": call_history,
        "count": len(call_history)
    })

@app.route('/twilio-data', methods=['GET'])
def get_twilio_data():
    """Fetch recent data from Twilio account."""
    try:
        if not twilio_client:
            return jsonify({"error": "Twilio client not configured"}), 500
        
        # Fetch recent messages
        recent_messages = twilio_client.messages.list(limit=10)
        messages_data = []
        for msg in recent_messages:
            messages_data.append({
                "sid": msg.sid,
                "from": msg.from_,
                "to": msg.to,
                "body": msg.body,
                "status": msg.status,
                "direction": msg.direction,
                "date_created": msg.date_created.isoformat() if msg.date_created else None
            })
        
        # Fetch recent calls
        recent_calls = twilio_client.calls.list(limit=10)
        calls_data = []
        for call in recent_calls:
            calls_data.append({
                "sid": call.sid,
                "from": call.from_,
                "to": call.to,
                "status": call.status,
                "direction": call.direction,
                "duration": call.duration,
                "date_created": call.date_created.isoformat() if call.date_created else None
            })
        
        return jsonify({
            "messages": messages_data,
            "calls": calls_data,
            "account_sid": Config.TWILIO_ACCOUNT_SID
        })
    
    except Exception as e:
        logger.error(f"Error fetching Twilio data: {str(e)}")
        return jsonify({"error": str(e)}), 500

def generate_sms_response(message_body, from_number):
    """Generate an appropriate SMS response based on the incoming message."""
    message_lower = message_body.lower().strip()
    
    # Simple keyword-based responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return f"Hello! Thanks for messaging us. How can I help you today?"
    
    elif any(word in message_lower for word in ['help', 'support']):
        return "I'm here to help! You can ask me about our services or send 'info' for more details."
    
    elif 'info' in message_lower:
        return "This is a Twilio-powered Flask app. It can handle SMS and voice calls. Send 'help' for assistance."
    
    elif any(word in message_lower for word in ['bye', 'goodbye', 'thanks']):
        return "Thank you for contacting us! Have a great day!"
    
    elif message_lower.isdigit():
        number = int(message_lower)
        return f"I received the number {number}. That's {'even' if number % 2 == 0 else 'odd'}!"
    
    else:
        return f"Thanks for your message: '{message_body}'. I'm a simple bot, but I'm learning! Send 'help' for more options."

def generate_voice_response(from_number):
    """Generate an appropriate voice response based on the caller."""
    return f"Hello! Thank you for calling our Twilio-powered Flask application. Your number is {from_number}."

if __name__ == '__main__':
    # Get port from environment (Codespaces sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # In Codespaces, we need to bind to all interfaces
    app.run(debug=True, host='0.0.0.0', port=port) 