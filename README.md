# Twilio Flask App

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/yourusername/yourrepo)

A Flask application that integrates with Twilio to handle SMS messages and voice calls. The app can receive webhooks from Twilio, process incoming messages/calls, and respond intelligently based on the content received.

## 🚀 Quick Start with GitHub Codespaces

Click the badge above or the "Code" → "Create codespace" button to get started instantly! No local setup required.

## Features

- **SMS Webhook Handler**: Receives and processes incoming SMS messages
- **Voice Webhook Handler**: Handles incoming voice calls with interactive responses
- **Message History**: Stores and retrieves message history
- **Call History**: Tracks incoming and outgoing calls
- **Outbound SMS**: Send SMS messages programmatically
- **Twilio Data Fetching**: Retrieve recent messages and calls from your Twilio account
- **Intelligent Responses**: Context-aware responses based on message content

## Prerequisites

- Python 3.7+
- A Twilio account with:
  - Account SID
  - Auth Token
  - A Twilio phone number
- ngrok (for local development with webhooks)

## Setup Instructions

### Option 1: GitHub Codespaces (Recommended)

The easiest way to get started is using GitHub Codespaces:

1. **Open in Codespaces**: Click the "Code" button on GitHub and select "Create codespace on main"
2. **Wait for setup**: Codespaces will automatically install dependencies
3. **Start the app**: Run `python start_codespaces.py` (optimized for Codespaces)
4. **Access your app**: Use the Ports tab in VS Code to open your app in a browser
5. **Add Twilio credentials**: Edit the `.env` file with your Twilio Account SID, Auth Token, and Phone Number

### Option 2: Local Development

#### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

#### 2. Configure Twilio Credentials

Create a `.env` file in the project root with your Twilio credentials:

```bash
# Twilio Account Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**To get your Twilio credentials:**
1. Sign up at [Twilio Console](https://console.twilio.com/)
2. Find your Account SID and Auth Token on the dashboard
3. Purchase a phone number from the Phone Numbers section

#### 3. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

#### 4. Set Up Webhooks (for receiving messages/calls)

**For GitHub Codespaces:**
1. Start your app with `python start_codespaces.py`
2. Use the Ports tab in VS Code to get your public URL
3. Configure webhooks in Twilio Console with your Codespaces URL

**For local development:**
Use ngrok to expose your local server:

```bash
# Install ngrok if you haven't already
# Then expose your local Flask app
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and configure your Twilio phone number webhooks:

1. Go to [Twilio Console > Phone Numbers](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming)
2. Click on your phone number
3. Set the webhook URLs:
   - **SMS Webhook**: `https://your-url/webhook/sms`
   - **Voice Webhook**: `https://your-url/webhook/voice`

## API Endpoints

### Core Endpoints

- `GET /` - Home page with API information
- `POST /webhook/sms` - Twilio SMS webhook endpoint
- `POST /webhook/voice` - Twilio voice webhook endpoint
- `POST /webhook/voice/gather` - Handle voice input gathering

### Data Endpoints

- `GET /messages` - Get local message history
- `GET /calls` - Get local call history
- `GET /twilio-data` - Fetch recent data from Twilio account

### Action Endpoints

- `POST /send-sms` - Send an SMS message

## Usage Examples

### Send an SMS

```bash
curl -X POST http://localhost:5000/send-sms \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "message": "Hello from Flask!"
  }'
```

### Get Message History

```bash
curl http://localhost:5000/messages
```

### Get Twilio Account Data

```bash
curl http://localhost:5000/twilio-data
```

## SMS Response Logic

The app responds intelligently to incoming SMS messages:

- **Greetings** (`hello`, `hi`, `hey`) → Welcome message
- **Help requests** (`help`, `support`) → Assistance information
- **Info requests** (`info`) → App information
- **Numbers** → Tells you if the number is even or odd
- **Farewells** (`bye`, `goodbye`, `thanks`) → Polite goodbye
- **Default** → Acknowledges the message and offers help

## Voice Call Features

When someone calls your Twilio number:

1. **Greeting**: Personalized welcome message with caller's number
2. **Input Gathering**: Prompts for speech or DTMF input
3. **Response**: Repeats back what was said or pressed
4. **Graceful Hangup**: Ends the call politely

## Project Structure

```
scavenger/
├── .devcontainer/
│   └── devcontainer.json    # GitHub Codespaces configuration
├── app.py                   # Main Flask application
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── start_codespaces.py      # Codespaces-optimized startup script
├── run.py                   # Local startup script
├── test_app.py              # Setup verification script
├── webhook_validator.py     # Production security utilities
├── env_template.txt         # Environment variables template
└── README.md               # This file
```

## Development

### GitHub Codespaces Development

GitHub Codespaces provides the best development experience:

- **Automatic setup**: Dependencies are installed automatically
- **Port forwarding**: Your app is accessible via a public URL
- **VS Code integration**: Full IDE experience in the browser
- **No local setup required**: Everything runs in the cloud

To start developing:
1. Open the repository in GitHub Codespaces
2. Run `python start_codespaces.py`
3. Use the Ports tab to access your app

### Local Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Security Notes

- Never commit your `.env` file with real credentials
- Use environment variables for all sensitive configuration
- Consider implementing webhook signature validation for production
- Use HTTPS in production environments

## Troubleshooting

### Common Issues

1. **"Twilio client not configured"**
   - Check that your `.env` file exists and has the correct credentials
   - Verify your Twilio Account SID and Auth Token are correct

2. **Webhooks not receiving data**
   - Ensure ngrok is running and the URL is correct
   - Check that webhook URLs in Twilio Console match your ngrok URL
   - Verify your Flask app is running and accessible

3. **SMS sending fails**
   - Confirm your Twilio phone number is correct
   - Check that the destination number is in a supported format (+1234567890)
   - Verify your Twilio account has sufficient balance

## Next Steps

- Add database storage for persistent message/call history
- Implement user authentication and authorization
- Add more sophisticated natural language processing
- Create a web interface for managing messages and calls
- Add support for MMS (multimedia messages)
- Implement conversation state management

## License

This project is open source and available under the MIT License.
