# Pokemon Battle Arena - Web Interface

A web application that allows you to select and battle different Pokemon AI bots, with the option to **watch battles live on Pokemon Showdown**!

## Features

- **Bot Selection**: Choose from 3 different bot strategies:
  - **Random Bot**: Makes completely random moves
  - **Max Damage Bot**: Always selects the highest base power move
  - **Custom Strategy Bot**: Uses sophisticated strategy including type effectiveness, STAB, and more

- **Two Battle Modes**:
  - **Bot vs Bot**: Watch two AI bots battle each other
  - **You vs Bot**: Battle against bots with your own Showdown account!
- **Watch Live on Showdown**: Click a button to open the battle in the full Pokemon Showdown interface!
- **Real-time Battle Updates**: Watch battles progress in real-time with Server-Sent Events
- **Battle History**: Track all your battles and their outcomes
- **Configurable Battles**: Choose your bot, opponent bot, and number of battles
- **Beautiful UI**: Modern, responsive design with gradient backgrounds and smooth animations
- **Play Yourself**: Challenge bots and play the battle manually on Showdown

## Prerequisites

1. **Python 3.8+** installed
2. All Python dependencies installed

## Installation

1. Install Python dependencies:
```bash
cd web
pip install -r requirements.txt
```

2. Make sure the parent directory contains:
   - `custom_strategy_bot.py`
   - `logging_player.py`
   - All other bot implementations

## Running the Application

### Option 1: Watch Battles Live on Showdown (Recommended!)

**Windows:**
```bash
Double-click: start_with_showdown.bat
```

This will:
1. Start the Pokemon Showdown server (port 8000)
2. Start the web application (port 5000)
3. Enable the "Watch Live" button to view battles in Showdown!

**Open in browser:**
- Web Interface: http://localhost:5000
- Showdown (for watching): http://localhost:8000

### Option 2: Simple Mode (No Visual Battles)

```bash
cd web
python app.py
```

Or double-click `start.bat`

Then open: http://localhost:5000

Battles run internally without the graphical Showdown interface.

## How to Watch Battles Live

1. Use `start_with_showdown.bat` to start both servers
2. Open http://localhost:5000
3. Select bots and start a battle
4. Click the **"Watch Live: Open in Showdown"** button when it appears
5. Watch the battle in full graphical glory with Pokemon sprites and animations!

See **WATCH_LIVE_GUIDE.md** for detailed instructions.

## How to Use

1. **Select Your Bot**: Click on one of the three bot cards to select your bot
2. **Select Opponent Bot**: Choose which bot your bot will battle against
3. **Configure Battle**: Choose the number of battles (1-10)
4. **Start Battle**: Click "Start Battle" to begin
5. **Watch Progress**: View real-time battle events and statistics
6. **View History**: Check the battle history section to see past battles

## API Endpoints

The Flask backend provides the following REST API:

- `GET /api/bots` - Get list of available bots for player
- `GET /api/opponents` - Get list of available opponent bots
- `POST /api/battle/start` - Start a new bot vs bot battle
  ```json
  {
    "bot_type": "random|maxdamage|custom",
    "opponent_type": "random|maxdamage|custom",
    "n_battles": 1
  }
  ```
- `GET /api/battle/<battle_id>/status` - Get battle status
- `GET /api/battle/<battle_id>/events` - Stream battle events (SSE)
- `GET /api/battles` - List all battles

## Project Structure

```
web/
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main HTML page
└── static/
    ├── style.css      # Styles and animations
    └── script.js      # Frontend JavaScript logic
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Real-time Communication**: Server-Sent Events (SSE)
- **Pokemon Battle Engine**: poke-env library

## Troubleshooting

### "Module not found" errors
- Make sure you're in the `web` directory when running `app.py`
- Install all requirements: `pip install -r requirements.txt`
- Check that parent directory contains bot implementation files (`custom_strategy_bot.py`, `logging_player.py`)

### Battles not starting
- Check Flask console output for error messages
- Ensure all dependencies are installed
- Verify port 5000 is not being used by another application

### Page not loading
- Make sure Flask server is running
- Check that you're navigating to `http://localhost:5000` (not https)
- Try a different browser if issues persist

## Development

To modify bot strategies:

1. Edit `custom_strategy_bot.py` to add new checks
2. Modify `app.py` in the `create_bot()` function to customize bot behavior
3. Add new bot types by extending the `/api/bots` endpoint

## Future Enhancements

- Add user authentication
- Save battle replays
- Add more bot strategies
- Implement ELO rating system
- Add spectator mode for watching ongoing battles
- Create battle statistics dashboard

## License

MIT License - Feel free to use and modify for your projects!
