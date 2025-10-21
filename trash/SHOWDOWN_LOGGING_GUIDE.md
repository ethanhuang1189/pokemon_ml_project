# Pokemon Showdown Battle Logging Guide

This guide shows you how to use bots to battle real players on Pokemon Showdown while logging all battle data for ML training.

## Available Scripts

### 1. `random_battle_logged.py` - Random Bot (Configured)
Already configured with Bot_Naila credentials. Just run it!

### 2. `showdown_max_damage_logger.py` - Max Damage Bot (Customizable)
Flexible script for challenge/accept/ladder modes with any account.

## Quick Start - Random Bot

The `random_battle_logged.py` script is pre-configured for Bot_Naila:

```bash
# CSV logging (default) - 1 battle
python random_battle_logged.py

# SQLite logging - 1 battle
python random_battle_logged.py sqlite
```

**To change number of battles**, edit line 68 or 71 in the script:
```python
random_battle_csv(n_battles=10)  # Change from 1 to desired number
```

## Setup for Max Damage Logger

### 1. Create a Pokemon Showdown Account

1. Go to https://play.pokemonshowdown.com/
2. Click "Register" in the top right
3. Create a username and password
4. Verify your account via email if required

### 2. Configure the Script

Edit `showdown_max_damage_logger.py` and update these lines:

```python
USERNAME = "your_showdown_username"
PASSWORD = "your_showdown_password"
```

## Max Damage Logger - Usage Modes

### Mode 1: Challenge a Specific Player

Challenge a specific player to a battle:

```bash
# CSV logging (default)
python showdown_max_damage_logger.py challenge PlayerUsername

# SQLite logging
python showdown_max_damage_logger.py challenge PlayerUsername sqlite
```

**Example:**
```bash
python showdown_max_damage_logger.py challenge OOmeNN
```

This will:
- Connect to Pokemon Showdown
- Challenge the specified player
- Log all battle data to `battle_data/showdown_your_username.csv`

### Mode 2: Accept Challenges

Accept challenges from any player:

```bash
# CSV logging (default)
python showdown_max_damage_logger.py accept

# SQLite logging
python showdown_max_damage_logger.py accept sqlite
```

This will:
- Connect to Pokemon Showdown
- Wait for incoming challenges
- Accept and battle anyone who challenges you
- Log all battles
- Run until you press Ctrl+C

**Great for collecting diverse battle data!**

### Mode 3: Ladder Battles

Play ranked ladder battles:

```bash
# Play 10 ladder battles (default)
python showdown_max_damage_logger.py ladder

# Play 50 ladder battles
python showdown_max_damage_logger.py ladder 50

# Play 20 ladder battles with SQLite
python showdown_max_damage_logger.py ladder 20 sqlite
```

This will:
- Connect to Pokemon Showdown
- Play the specified number of ranked battles
- Log all battle data
- Face random opponents from the ladder

**Best for collecting competitive battle data!**

## Output Files

All battle data is saved to the `battle_data/` directory:

### Random Bot
- `battle_data/Bot_Naila_random.csv` (or `.db`)

### Max Damage Logger - Challenge Mode
- `battle_data/showdown_<username>.csv` (or `.db`)

### Max Damage Logger - Ladder Mode
- `battle_data/ladder_<username>.csv` (or `.db`)

## Battle Formats

### Random Bot
- Uses `gen9randombattle` (Generation 9 Random Battle)
- Change on line 22 or 47 in `random_battle_logged.py`

### Max Damage Logger
- Default: `gen8randombattle` (Generation 8 Random Battle)
- Change the `battle_format` parameter in the script

```python
# Common formats:
battle_format = "gen8randombattle"    # Gen 8 Random Battle
battle_format = "gen9randombattle"    # Gen 9 Random Battle
battle_format = "gen8ou"              # Gen 8 OU (need team)
battle_format = "gen9ou"              # Gen 9 OU (need team)
```

**Note:** For non-random formats, you'll need to provide a team. Random battles are easiest for data collection.

## Data Collected

The logger captures all the same data as the local battles:

- Turn-by-turn battle state
- Pokemon stats (HP, attack, defense, etc.)
- Move information (type, power, accuracy)
- Available moves and switches
- Damage dealt each turn
- Battle outcomes (win/loss)

See `BATTLE_LOGGING_README.md` for the complete data schema.

## Tips for Data Collection

### 1. Random Bot Ladder (Easy Start)
```bash
python random_battle_logged.py
```
- Pre-configured with Bot_Naila
- Plays random moves (baseline data)
- Gen 9 Random Battle format

### 2. Max Damage Ladder (Better Strategy)
```bash
python showdown_max_damage_logger.py ladder 100
```
- Face real competitive players
- Always picks highest damage move
- Higher quality decision-making data

### 3. Accept Challenges (Most Volume)
```bash
python showdown_max_damage_logger.py accept
```
- Leave running overnight
- Collect battles from anyone
- Large volume of diverse data

### 4. Challenge Friends (Controlled Testing)
```bash
python showdown_max_damage_logger.py challenge FriendUsername
```
- Test specific scenarios
- Consistent opponent for comparison
- Good for debugging your ML models

## Example: Collecting Training Data

Here's a complete workflow:

### Step 1: Collect Diverse Data
```bash
# Start with random bot (baseline)
python random_battle_logged.py
# Edit script to set n_battles=50

# Run max damage ladder for better strategy data
python showdown_max_damage_logger.py ladder 50
# (requires configuration first)

# Or accept challenges for variety
python showdown_max_damage_logger.py accept
# (let it run for a few hours, press Ctrl+C when done)
```

### Step 2: Load and Analyze
```python
import pandas as pd

# Load Bot_Naila random data
random_df = pd.read_csv('battle_data/Bot_Naila_random.csv')

# Or load max damage data if you configured it
# ladder_df = pd.read_csv('battle_data/ladder_your_username.csv')
# showdown_df = pd.read_csv('battle_data/showdown_your_username.csv')

# Analyze the data
print(f"Total battles: {random_df['battle_tag'].nunique()}")
print(f"Total turns: {len(random_df)}")
print(f"Win rate: {random_df.groupby('battle_tag')['won_battle'].first().mean():.1%}")

# Compare different strategies if you have both
# all_data = pd.concat([random_df, ladder_df], ignore_index=True)
```

### Step 3: Train Your Model
```python
# Filter for important features
features = [
    'active_hp_fraction', 'opponent_hp_fraction',
    'selected_move_base_power', 'active_spe', 'opponent_spe'
]

X = all_data[features].fillna(0)
y = all_data['won_battle'].fillna(0)

# Train a model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)
```

## Troubleshooting

### Connection Issues
- Make sure you have internet connection
- Verify your username/password are correct
- Check if Pokemon Showdown is down: https://play.pokemonshowdown.com/

### No Opponents Found (Ladder)
- Try a more popular format like `gen9randombattle`
- Play during peak hours (evenings US time)

### Challenges Not Accepted
- Make sure your opponent is online
- They must accept your challenge
- Try accepting challenges instead

### Rate Limiting
- Pokemon Showdown may rate limit bots
- Don't run too many battles too quickly
- Take breaks between sessions

## Advanced: Custom Battle Formats

For non-random formats, you need a team. Here's how to add one:

```python
# In showdown_max_damage_logger.py, add team parameter:
player = LoggingMaxDamagePlayer(
    logger=logger,
    battle_format="gen8ou",
    team="[PASTE YOUR TEAM HERE]",  # Showdown team format
    account_configuration=AccountConfiguration(username, password),
    server_configuration=ShowdownServerConfiguration,
    start_timer_on_battle_start=True,
)
```

Get teams from:
- https://www.smogon.com/forums/threads/sample-teams.3661450/
- Pokemon Showdown teambuilder (export as text)

## Ethics & Fair Play

- **Be respectful**: Your bot should be clearly identified as a bot
- **Don't spam**: Don't send excessive challenges
- **Learn from data**: Use the data to improve, not to exploit
- **Follow Showdown rules**: Check Pokemon Showdown's bot policy

## Next Steps

Once you've collected data:

1. **Analyze battle patterns** - Which moves are most effective?
2. **Train ML models** - Predict optimal moves
3. **Create a smarter bot** - Use your trained model
4. **Compare performance** - Max damage vs. your ML model

See `BATTLE_LOGGING_README.md` for ML training examples!
