from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os
from datetime import datetime
import logging
from config import Config
from scavenger_game import game

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
    """Home page with information about the Portland Scavenger Hunt."""
    return jsonify({
        "message": "Portland Scavenger Hunt Bot 🎯",
        "description": "A Twilio-powered scavenger hunt game exploring Portland's iconic locations",
        "game_info": {
            "locations": 5,
            "max_points_per_clue": 40,
            "total_possible_points": 200,
            "features": [
                "OpenAI-powered natural language processing",
                "Progressive hint system",
                "Score tracking by phone number",
                "Portland-specific locations and clues"
            ]
        },
        "how_to_play": {
            "start": "Text 'READY' to your Twilio number",
            "answer": "Respond with location names in natural language",
            "hints": "Get up to 3 hints per clue",
            "scoring": "40 pts (no hints), 30 pts (1 hint), 20 pts (2 hints), 10 pts (3 hints)"
        },
        "endpoints": {
            "sms_webhook": "/webhook/sms",
            "voice_webhook": "/webhook/voice",
            "game_stats": "/game-stats",
            "leaderboard": "/leaderboard"
        }
    })

@app.route('/webhook/sms', methods=['POST'])
def sms_webhook():
    """Handle incoming SMS messages for the scavenger hunt game."""
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
        
        # Process the message through the scavenger hunt game
        response = MessagingResponse()
        reply_message = process_scavenger_hunt_message(message_body, from_number)
        response.message(reply_message)
        
        # Log the response
        logger.info(f"Responding to {from_number}: {reply_message[:100]}...")
        
        # Store response in history
        response_data = {
            "sid": f"response_{message_sid}",
            "from": to_number,
            "to": from_number,
            "body": reply_message,
            "timestamp": datetime.now().isoformat(),
            "direction": "outbound"
        }
        message_history.append(response_data)
        
        return str(response)
    
    except Exception as e:
        logger.error(f"Error processing SMS webhook: {str(e)}")
        response = MessagingResponse()
        response.message("Sorry, I encountered an error. Please try texting 'READY' to start the Portland Scavenger Hunt! 🎯")
        return str(response)

@app.route('/webhook/voice', methods=['POST'])
def voice_webhook():
    """Handle incoming voice calls with scavenger hunt information."""
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
        
        # Create voice response about the scavenger hunt
        response = VoiceResponse()
        
        voice_message = f"""Hello! You've reached the Portland Scavenger Hunt hotline. 
        This is a text-based game where you explore Portland's iconic locations. 
        To play, send a text message with the word READY to this number. 
        You'll receive clues about 5 amazing Portland locations and earn points for correct answers. 
        The game uses artificial intelligence to understand your responses in natural language. 
        Have fun exploring Portland!"""
        
        response.say(voice_message, voice='alice')
        response.hangup()
        
        return str(response)
    
    except Exception as e:
        logger.error(f"Error processing voice webhook: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, I encountered an error. Please send a text message with READY to play the Portland Scavenger Hunt.", voice='alice')
        response.hangup()
        return str(response)

def process_scavenger_hunt_message(message_body, from_number):
    """Process incoming message through the scavenger hunt game logic."""
    message_lower = message_body.lower().strip()
    
    # Handle game commands
    if message_lower in ['ready', 'start', 'begin', 'play']:
        return game.start_game(from_number)
    
    elif message_lower in ['status', 'score', 'progress']:
        return game.get_status(from_number)
    
    elif message_lower in ['help', 'info', 'instructions']:
        return """🎯 Portland Scavenger Hunt Help

How to play:
• Send 'READY' to start the game
• Answer clues about Portland locations
• Use natural language - I understand various ways to say the same thing!
• Get hints if you're stuck (but they reduce your points)

Scoring:
• First try: 40 points
• With 1 hint: 30 points
• With 2 hints: 20 points  
• With 3 hints: 10 points

Commands:
• READY - Start/restart game
• STATUS - Check your progress
• HELP - Show this message

Ready to explore Portland? Send 'READY'! 🌲"""
    
    elif message_lower in ['quit', 'stop', 'exit']:
        # Reset player's game
        if from_number in game.players:
            del game.players[from_number]
        return "👋 Thanks for playing the Portland Scavenger Hunt! Send 'READY' anytime to play again! 🌲"
    
    else:
        # Process as a game answer
        return game.process_answer(from_number, message_body)

@app.route('/game-stats', methods=['GET'])
def get_game_stats():
    """Get overall game statistics."""
    total_players = len(game.players)
    active_players = sum(1 for p in game.players.values() if p["game_started"])
    completed_games = sum(1 for p in game.players.values() if len(p["completed_clues"]) == 5)
    
    # Calculate average score for completed games
    completed_scores = [p["total_score"] for p in game.players.values() if len(p["completed_clues"]) == 5]
    avg_score = sum(completed_scores) / len(completed_scores) if completed_scores else 0
    
    return jsonify({
        "total_players": total_players,
        "active_players": active_players,
        "completed_games": completed_games,
        "average_score": round(avg_score, 1),
        "game_info": {
            "total_clues": len(game.clues),
            "max_possible_score": 200,
            "locations": [clue["location"] for clue in game.clues]
        }
    })

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard of top scores."""
    # Get all completed games with scores
    completed_players = []
    for phone, player_data in game.players.items():
        if len(player_data["completed_clues"]) == 5:
            completed_players.append({
                "phone": phone[-4:],  # Only show last 4 digits for privacy
                "score": player_data["total_score"],
                "completion_time": player_data.get("start_time", "Unknown")
            })
    
    # Sort by score (descending)
    leaderboard = sorted(completed_players, key=lambda x: x["score"], reverse=True)[:10]
    
    return jsonify({
        "leaderboard": leaderboard,
        "total_completed_games": len(completed_players)
    })

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

@app.route('/send-sms', methods=['POST'])
def send_sms():
    """Send an SMS message via Twilio (for admin use)."""
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
        
        logger.info(f"Sent SMS to {to_number}: {message_body}")
        
        return jsonify({
            "success": True,
            "message_sid": message.sid,
            "status": message.status
        })
    
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/twilio-data', methods=['GET'])
def get_twilio_data():
    """Fetch recent data from Twilio account."""
    try:
        if not twilio_client:
            return jsonify({"error": "Twilio client not configured"}), 500
        
        # Fetch recent messages
        recent_messages = twilio_client.messages.list(limit=20)
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

if __name__ == '__main__':
    # Get port from environment (Codespaces sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # In Codespaces, we need to bind to all interfaces
    app.run(debug=True, host='0.0.0.0', port=port) 