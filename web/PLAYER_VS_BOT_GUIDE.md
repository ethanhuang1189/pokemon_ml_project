# Battle Bots with Your Own Account!

Now you can battle against the AI bots using your own Showdown account!

## How It Works

1. **Choose Mode**: Select "You vs Bot" mode
2. **Enter Your Username**: Type your Showdown username
3. **Pick Opponent**: Choose which bot to battle
4. **Bot Challenges YOU**: Bot_Naila will send you a challenge
5. **Accept & Battle!**: Accept the challenge and play!

## Step-by-Step Guide

### 1. Start the Servers

Run: `start_with_showdown.bat`

This starts both:
- Pokemon Showdown (port 8000)
- Web Interface (port 5000)

### 2. Open Web Interface

Go to: **http://localhost:5000**

### 3. Select "You vs Bot" Mode

Click the **"You vs Bot"** card

### 4. Enter Your Username

- Type your Showdown username (any name works on local server)

Click **"Continue"**

### 5. Choose Your Opponent

Pick which bot you want to battle:
- **Random Bot**: Makes random moves (easy)
- **Max Damage Bot**: Always uses highest power moves (medium)
- **Custom Strategy Bot**: Uses advanced AI strategy (hard)

### 6. Start the Bot

Click **"Start Battle"**

You'll see instructions like:
```
🎮 READY TO BATTLE!

1. Log into Showdown as 'YourName'
2. Wait for challenge notification from Bot_Naila
3. Accept the challenge and battle!

The bot will send you a challenge in a few seconds...
```

### 7. Open Showdown

In another tab, go to: **http://localhost:8000**

### 8. Log In

For local server:
1. Click "Choose name"
2. Enter your username (same as step 4)
3. Click anywhere to close

### 9. Wait for Challenge

Within a few seconds, you'll see a notification:
```
🔔 Bot_Naila challenged you to a gen8randombattle battle!
[Accept] [Reject]
```

### 10. Accept & Battle!

Click **"Accept"** and the battle begins!

Play the battle on Showdown like normal:
- Select your moves
- Switch Pokemon
- Use items
- Try to beat the AI!

### 11. Watch the Dashboard

Back on the web interface (localhost:5000), you'll see:
- Battle progress
- Live battle link
- Statistics

## Tips

### For Local Server
- Any username works
- No verification needed
- Bot challenges you instantly

### For Official Showdown
- Set LOCAL_SERVER to ShowdownServerConfiguration in app.py
- Use real Showdown account
- Bot_Naila must be logged into official server
- Update Bot_Naila credentials in app.py

### Battle Strategy
- **vs Random Bot**: Easy win, good for testing
- **vs Max Damage**: Moderate challenge, predictable
- **vs Custom Strategy**: Hardest, uses type matchups and STAB

### Multiple Battles
- Set battles to 2+ for series
- You'll need to challenge the bot again after each battle
- Stats track across all battles

## Troubleshooting

### Not receiving challenge?

Check:
1. You're logged into Showdown with correct username
2. Showdown server is running (localhost:8000)
3. Web interface shows "Sending challenge to [your name]..."
4. Check Showdown notifications (top right)

### Can't log into Showdown?

For local server:
- Just type any name, no verification
- Click away from login popup
- Name must match what you entered in web interface

### Challenge not appearing?

- Refresh Showdown page
- Make sure you're on the Home tab
- Look for red notification badge
- Check that Bot_Naila is online

### Want to battle on official Showdown?

1. Edit `web/app.py`:
```python
# Change to:
from poke_env import ShowdownServerConfiguration
LOCAL_SERVER = ShowdownServerConfiguration
```

2. Use your real Showdown credentials
3. Bot will battle on official server
4. Share battle links with friends!

## Example Session

```
1. Select "You vs Bot"
2. Enter username: "CoolTrainer"
3. Select opponent: "Custom Strategy Bot"
4. Click "Start Battle"
5. See: "Bot_Naila will challenge you..."
6. Open Showdown → Login as "CoolTrainer"
7. Wait a few seconds...
8. Notification: "Bot_Naila challenged you!"
9. Click "Accept"
10. Battle starts!
11. Play your moves
12. Win or lose → Stats update
13. Click "Start New Battle" for rematch!
```

## Advanced: Team Battles

For custom teams (not random):
1. Change format in bot creation
2. Edit app.py battle_format parameter
3. Use: gen8ou, gen8vgc2021, etc.

## Have Fun!

Test your skills against AI opponents and see if you can beat the smart bots!
