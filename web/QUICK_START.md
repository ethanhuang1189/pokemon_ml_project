# Quick Start Guide

## Getting Started in 3 Steps

### 1. Start the Server

**Windows:**
```bash
Double-click start.bat
```

**Mac/Linux:**
```bash
cd web
python app.py
```

### 2. Open Your Browser

Navigate to: **http://localhost:5000**

### 3. Battle!

1. **Select Your Bot** - Click one of the three bot cards (Random, Max Damage, or Custom Strategy)
2. **Select Opponent** - Choose which bot to battle against
3. **Configure** - Set the number of battles (1-10)
4. **Start Battle** - Click "Start Battle" and watch the action!

## What You'll See

- **Real-time Events**: Watch each turn as it happens
- **Battle Stats**: See wins, losses, and progress
- **Battle History**: Track all completed battles

## Bot Descriptions

### Random Bot
- Makes completely random move choices
- Simple and unpredictable
- Good for testing

### Max Damage Bot
- Always chooses the move with highest base power
- Straightforward aggressive strategy
- Predictable but effective

### Custom Strategy Bot
- Uses advanced strategy:
  - Prioritizes super effective moves
  - Considers STAB (Same Type Attack Bonus)
  - Avoids not very effective moves
  - Factors in accuracy and base power
- Most sophisticated AI

## Tips

- Try different bot matchups to see which strategies work best!
- Run multiple battles (5-10) to get statistically significant results
- Watch the event log to understand bot decision-making
- Check battle history to track performance over time

## Troubleshooting

**Server won't start?**
- Make sure you ran `pip install -r requirements.txt`
- Check that port 5000 isn't being used by another app

**Page won't load?**
- Ensure the Flask server is running (check terminal)
- Try http://localhost:5000 (not https)
- Clear your browser cache

**Battles failing?**
- Check the Flask console for error messages
- Make sure parent directory has `custom_strategy_bot.py` and `logging_player.py`

## Have Fun!

Experiment with different matchups and see which bot comes out on top!
