# Portland Scavenger Hunt Bot 🎯

A Twilio-powered SMS scavenger hunt game that takes players on an adventure through Portland's most iconic locations! Using OpenAI's natural language processing, the bot understands responses in natural language and provides an engaging, interactive experience.

## 🌲 Game Features

- **5 Portland Locations**: Explore iconic spots like the International Rose Test Garden, Powell's Books, Voodoo Doughnut, Pioneer Courthouse Square, and Tom McCall Waterfront Park
- **Smart AI Processing**: OpenAI-powered natural language understanding accepts various ways of saying the same answer
- **Progressive Hint System**: Get up to 3 hints per clue, but each hint reduces your points
- **Dynamic Scoring**: 40 points (no hints), 30 points (1 hint), 20 points (2 hints), 10 points (3 hints)
- **Player Tracking**: Individual score tracking by phone number
- **Game Statistics**: View leaderboards and game stats via API endpoints

## 🎮 How to Play

1. **Start**: Text `READY` to the Twilio phone number
2. **Answer**: Respond to clues about Portland locations in natural language
3. **Get Hints**: If stuck, the bot will provide helpful hints (but reduce your score)
4. **Complete**: Visit all 5 locations to complete the scavenger hunt!

### Game Commands
- `READY` - Start or restart the game
- `STATUS` - Check your current progress and score
- `HELP` - Get game instructions
- `QUIT` - Exit the current game

## 🚀 Quick Setup Options

### Option 1: GitHub Codespaces (Recommended)
1. Click the "Code" button and select "Create codespace on main"
2. Wait for the environment to set up automatically
3. Copy `env_template.txt` to `.env` and add your API keys
4. Run the startup script: `python start_codespaces.py`

### Option 2: Local Development
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see Configuration section)
4. Run: `python app.py`

## 🔧 Configuration

### Required Environment Variables

Create a `.env` file with the following variables:

```bash
# Twilio Configuration (get from https://console.twilio.com/)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# OpenAI Configuration (get from https://platform.openai.com/)
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### Getting API Keys

#### Twilio Setup
1. Sign up at [Twilio Console](https://console.twilio.com/)
2. Get a phone number with SMS capabilities
3. Copy your Account SID and Auth Token
4. Set up webhook URLs (see Webhook Configuration)

#### OpenAI Setup
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Create an API key in your account settings
3. Add credits to your account for API usage

### Webhook Configuration

Configure your Twilio phone number webhooks:
- **SMS Webhook URL**: `https://your-domain.com/webhook/sms`
- **Voice Webhook URL**: `https://your-domain.com/webhook/voice`

For Codespaces, your domain will be: `https://your-codespace-name-5000.app.github.dev`

## 📊 API Endpoints

### Game Endpoints
- `GET /` - Game information and instructions
- `GET /game-stats` - Overall game statistics
- `GET /leaderboard` - Top 10 player scores
- `POST /webhook/sms` - SMS webhook (configured in Twilio)
- `POST /webhook/voice` - Voice webhook (configured in Twilio)

### Admin Endpoints
- `GET /messages` - Message history
- `GET /calls` - Call history
- `POST /send-sms` - Send SMS (admin use)
- `GET /twilio-data` - Fetch recent Twilio data

## 🏗️ Project Structure

```
scavenger/
├── app.py                 # Main Flask application
├── scavenger_game.py      # Game logic and OpenAI integration
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from template)
├── env_template.txt       # Environment template
├── README.md              # This file
├── start_codespaces.py    # Codespaces startup script
├── test_app.py           # Test script
├── run.py                # Local startup script
└── .devcontainer/        # Codespaces configuration
    └── devcontainer.json
```

## 🎯 Game Locations

The scavenger hunt features these iconic Portland locations:

1. **International Rose Test Garden** - Washington Park's famous rose garden
2. **Powell's City of Books** - The world's largest independent bookstore
3. **Voodoo Doughnut** - Iconic donut shop with unique flavors
4. **Pioneer Courthouse Square** - Portland's "living room"
5. **Tom McCall Waterfront Park** - Scenic riverside park and Saturday Market

## 🧪 Testing

### Test the Setup
```bash
python test_app.py
```

### Test Game Logic
```bash
# Start the app
python app.py

# In another terminal, test the game endpoints
curl http://localhost:5000/
curl http://localhost:5000/game-stats
```

### Test SMS Functionality
Send a text message with "READY" to your Twilio number to start the game!

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`

2. **Twilio 401 Errors**: 
   - Check your webhook URLs are correct
   - Ensure your Codespace port is public (not private)
   - Verify your Twilio credentials

3. **OpenAI Errors**:
   - Verify your API key is correct
   - Check you have credits in your OpenAI account
   - The game will fall back to simple string matching if OpenAI fails

4. **Port Issues in Codespaces**:
   - Make sure port 5000 is set to "Public" in the Ports tab
   - Use the correct Codespace URL format

### Debug Mode
Set `FLASK_ENV=development` in your `.env` file for detailed error messages.

## 🚀 Deployment

### GitHub Codespaces
- Automatically configured for development
- Port 5000 is exposed and can be made public
- Perfect for testing and development

### Production Deployment
For production deployment, consider:
- Using a proper database instead of in-memory storage
- Setting up proper logging and monitoring
- Using environment-specific configuration
- Implementing rate limiting and security measures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎉 Have Fun!

Enjoy exploring Portland through this interactive scavenger hunt! The game is designed to be educational and fun, showcasing some of Portland's most beloved locations. 

Send `READY` to get started! 🌲
