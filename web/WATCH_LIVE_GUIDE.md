# Watch Battles Live on Pokemon Showdown

Now you can watch your bots battle in real-time on the Pokemon Showdown interface!

## Setup

### Step 1: Start Pokemon Showdown Server

**Windows (Easy Way):**
```bash
Double-click: start_with_showdown.bat
```

**Manual Way:**
```bash
# Terminal 1 - Start Showdown
cd showdown-relay/pokemon-showdown
node pokemon-showdown start --no-security

# Terminal 2 - Start Web App
cd web
python app.py
```

### Step 2: Open the Web Interface

Go to: **http://localhost:5000**

### Step 3: Start a Battle

1. Select your bot
2. Select opponent bot
3. Click "Start Battle"

### Step 4: Watch Live!

When the battle starts, you'll see a **"Watch Live: Open in Showdown"** button appear!

Click it to open the battle in the Pokemon Showdown interface where you can:
- See the actual Pokemon sprites
- Watch moves in real-time
- View damage calculations
- See status effects and animations

## What You'll See

### In the Web Interface (http://localhost:5000)
- Bot selection
- Battle configuration
- Real-time event log
- Statistics and win/loss tracking
- **Live battle link**

### In Pokemon Showdown (http://localhost:8000)
- Full graphical battle interface
- Pokemon sprites and animations
- Move-by-move visualization
- Chat log with battle commentary

## Two Ways to Watch

### Option 1: Web Dashboard + Showdown (Recommended)
- Start battle from web interface
- Click "Watch Live" button when it appears
- Watch the graphical battle in Showdown
- Track stats in the web dashboard

### Option 2: Web Dashboard Only
- Just use the web interface
- See battle events in text form
- No need to open Showdown
- Lighter weight

## Troubleshooting

### "Watch Live" button not appearing?
- Make sure Showdown server is running on port 8000
- Check that both bots connected successfully
- Wait a few seconds for the battle to initialize

### Can't open Showdown link?
```bash
# Check if Showdown is running:
# Open http://localhost:8000 in browser
# You should see the Showdown homepage
```

### Showdown server won't start?
```bash
cd showdown-relay/pokemon-showdown
npm install
node pokemon-showdown start --no-security
```

### Bots not connecting to Showdown?
- Ensure `--no-security` flag is used when starting Showdown
- Check that no other service is using port 8000
- Restart both servers

## Tips

- **Multiple Battles**: When running multiple battles, a new Showdown tab opens for each one
- **Battle Speed**: Battles happen in real-time - watch moves execute one by one
- **Best Experience**: Use two monitors - web dashboard on one, Showdown battles on the other
- **Recording**: You can use OBS or similar to record the Showdown battles

## Technical Details

- **Web App Port**: 5000 (Flask server)
- **Showdown Port**: 8000 (Pokemon Showdown server)
- **Connection**: Bots connect via WebSocket to localhost:8000
- **Battle Format**: gen8randombattle (Generation 8 Random Battle)

## Advanced: Using Official Showdown

If you want to battle on the official Pokemon Showdown server (play.pokemonshowdown.com):

1. Edit `web/app.py`:
```python
# Change LOCAL_SERVER to:
LOCAL_SERVER = ShowdownServerConfiguration
```

2. Add authentication for your bots:
```python
bot = create_bot(bot_type, username)
# Set account configuration with your Showdown credentials
```

3. Battles will appear on the official server
4. You can share battle links with others!

## Enjoy!

Watch your bots strategize, make moves, and battle it out in full graphical glory!
