# Battle Data Logging System

This system logs detailed battle data from Pokemon battles for machine learning training purposes.

## Files Created

1. **logging_player.py** - Core logging functionality
   - `BattleDataLogger` - Base logger class
   - `CSVBattleLogger` - Logs to CSV files
   - `SQLiteBattleLogger` - Logs to SQLite database
   - `LoggingRandomPlayer` - Random player with logging
   - `LoggingMaxDamagePlayer` - Max damage player with logging

2. **max_damage_battle_logged.py** - Max damage bot battles with logging
3. **random_battle_logged.py** - Random bot battles with logging

## Data Logged Per Turn

The system logs the following data for each turn:

### Battle Metadata
- `timestamp` - When the turn occurred
- `battle_tag` - Unique battle identifier
- `turn` - Turn number
- `player_username` - Username of the player

### Active Pokemon Stats
- `active_pokemon` - Species name
- `active_hp` - Current HP
- `active_max_hp` - Maximum HP
- `active_hp_fraction` - HP as fraction (0-1)
- `active_status` - Status condition (paralysis, burn, etc.)
- `active_atk/def/spa/spd/spe` - Base stats

### Opponent Pokemon Stats
- `opponent_pokemon` - Species name
- `opponent_hp` - Current HP
- `opponent_max_hp` - Maximum HP
- `opponent_hp_fraction` - HP as fraction (0-1)
- `opponent_status` - Status condition
- `opponent_atk/def/spa/spd/spe` - Base stats

### Move Information
- `selected_move` - Move chosen this turn
- `selected_move_type` - Move type (Fire, Water, etc.)
- `selected_move_category` - Physical/Special/Status
- `selected_move_base_power` - Base power of move
- `selected_move_accuracy` - Move accuracy

### Available Options
- `available_moves` - Pipe-separated list of available moves
- `available_switches` - Pipe-separated list of available switches

### Battle Outcome
- `damage_dealt` - Damage dealt to opponent this turn
- `fainted` - Whether opponent fainted (1 or 0)
- `won_battle` - Whether battle was won (1, 0, or NULL if ongoing)

## Usage

### CSV Logging (Default)

```bash
# Max damage battles
python max_damage_battle_logged.py

# Random battles
python random_battle_logged.py
```

Output files: `battle_data/max_damage_player1.csv` and `battle_data/max_damage_player2.csv`

### SQLite Logging

```bash
# Max damage battles
python max_damage_battle_logged.py sqlite

# Random battles
python random_battle_logged.py sqlite
```

Output files: `battle_data/max_damage_player1.db` and `battle_data/max_damage_player2.db`

## Using the Data for ML Training

### Loading CSV Data

```python
import pandas as pd

# Load battle data
df = pd.read_csv('battle_data/max_damage_player1.csv')

# Filter for won battles only
won_battles = df[df['won_battle'] == 1]

# Analyze move effectiveness
move_stats = df.groupby('selected_move').agg({
    'damage_dealt': 'mean',
    'won_battle': 'mean'
})
```

### Loading SQLite Data

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('battle_data/max_damage_player1.db')

# Query all data
df = pd.read_sql_query("SELECT * FROM battle_turns", conn)

# Query specific battles
winning_turns = pd.read_sql_query(
    "SELECT * FROM battle_turns WHERE won_battle = 1",
    conn
)

conn.close()
```

### Example ML Feature Engineering

```python
import pandas as pd

df = pd.read_csv('battle_data/max_damage_player1.csv')

# Create features
df['hp_advantage'] = df['active_hp_fraction'] - df['opponent_hp_fraction']
df['speed_advantage'] = df['active_spe'] - df['opponent_spe']
df['is_attacking'] = df['selected_move_base_power'] > 0

# Prepare for training
features = ['active_hp_fraction', 'opponent_hp_fraction',
            'hp_advantage', 'speed_advantage',
            'selected_move_base_power']

X = df[features].fillna(0)
y = df['won_battle'].fillna(0)

# Split into train/test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Custom Logging

You can create your own logging player by inheriting from `LoggingPlayer`:

```python
from logging_player import LoggingPlayer, CSVBattleLogger
from poke_env.player.battle_order import BattleOrder
from poke_env.battle import AbstractBattle

class MyCustomLoggingPlayer(LoggingPlayer):
    def __init__(self, logger, *args, **kwargs):
        super().__init__(logger, *args, **kwargs)

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        # Your custom move selection logic
        move = self.choose_random_move(battle)

        # Log the turn
        self._log_battle_turn(battle, move)

        return move

# Usage
logger = CSVBattleLogger("my_data.csv")
player = MyCustomLoggingPlayer(logger=logger)
```

## Tips

1. **CSV vs SQLite**:
   - Use CSV for easy analysis in Excel/pandas
   - Use SQLite for large datasets and complex queries

2. **Data Volume**:
   - Each battle generates ~20-50 rows (one per turn)
   - 100 battles = ~2,000-5,000 rows
   - Plan storage accordingly

3. **Training Considerations**:
   - Balance your dataset (equal won/lost battles)
   - Consider turn order (early turns vs late game)
   - Account for Pokemon type matchups
   - Normalize HP and stat values

4. **Server Requirement**:
   - Make sure your local Pokemon Showdown server is running
   - Default: `ws://localhost:8000/showdown/websocket`
