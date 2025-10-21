from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
from poke_env.player import RandomPlayer, MaxBasePowerPlayer
from poke_env import ServerConfiguration
import sys
import os

# Add parent directory to path to import custom bots
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from custom_strategy_bot import (
    CustomStrategyPlayer,
    check_super_effective,
    check_stab_bonus,
    check_avoid_ineffective,
    check_high_base_power,
    check_high_accuracy
)

app = Flask(__name__)
CORS(app)

# Server configuration for local Showdown server
LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)

class BattleTracker:
    """Tracks all moves and events during a battle"""
    def __init__(self):
        self.turns = []
        self.current_turn = {"turn_number": 0, "events": []}

    def start_turn(self, turn_number):
        """Start tracking a new turn"""
        if self.current_turn["events"]:
            self.turns.append(self.current_turn)
        self.current_turn = {"turn_number": turn_number, "events": []}

    def add_event(self, event_text):
        """Add an event to the current turn"""
        self.current_turn["events"].append(event_text)

    def finalize(self):
        """Finalize the last turn"""
        if self.current_turn["events"]:
            self.turns.append(self.current_turn)

    def get_battle_log(self):
        """Get formatted battle log"""
        return self.turns

class TrackedRandomPlayer(RandomPlayer):
    def __init__(self, battle_tracker, bot_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.battle_tracker = battle_tracker
        self.bot_name = bot_name
        self._battles = {}

    def choose_move(self, battle):
        # Track battle instance
        if battle.battle_tag not in self._battles:
            self._battles[battle.battle_tag] = battle

        # Update turn if needed
        if battle.turn > self.battle_tracker.current_turn["turn_number"]:
            self.battle_tracker.start_turn(battle.turn)

        # Get move
        move = super().choose_move(battle)

        # Log the move
        move_name = self._extract_move_name(move, battle)
        active_pokemon = battle.active_pokemon
        pokemon_name = active_pokemon.species if active_pokemon else "Unknown"

        self.battle_tracker.add_event(f"{self.bot_name}'s {pokemon_name} used {move_name}")

        return move

    def _extract_move_name(self, order, battle):
        """Extract readable move name from order"""
        if hasattr(order, 'order') and order.order:
            move = order.order
            if hasattr(move, 'id'):
                return move.id.replace('-', ' ').title()
            elif hasattr(move, 'species'):
                return f"Switch to {move.species}"
        return "Unknown Move"

class TrackedMaxDamagePlayer(MaxBasePowerPlayer):
    def __init__(self, battle_tracker, bot_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.battle_tracker = battle_tracker
        self.bot_name = bot_name
        self._battles = {}

    def choose_move(self, battle):
        if battle.battle_tag not in self._battles:
            self._battles[battle.battle_tag] = battle

        if battle.turn > self.battle_tracker.current_turn["turn_number"]:
            self.battle_tracker.start_turn(battle.turn)

        move = super().choose_move(battle)

        move_name = self._extract_move_name(move, battle)
        active_pokemon = battle.active_pokemon
        pokemon_name = active_pokemon.species if active_pokemon else "Unknown"

        self.battle_tracker.add_event(f"{self.bot_name}'s {pokemon_name} used {move_name}")

        return move

    def _extract_move_name(self, order, battle):
        if hasattr(order, 'order') and order.order:
            move = order.order
            if hasattr(move, 'id'):
                return move.id.replace('-', ' ').title()
            elif hasattr(move, 'species'):
                return f"Switch to {move.species}"
        return "Unknown Move"

class TrackedCustomStrategyPlayer(CustomStrategyPlayer):
    def __init__(self, battle_tracker, bot_name, *args, **kwargs):
        super().__init__(battle_logger=None, *args, **kwargs)
        self.battle_tracker = battle_tracker
        self.bot_name = bot_name
        self._battles = {}

    def choose_move(self, battle):
        if battle.battle_tag not in self._battles:
            self._battles[battle.battle_tag] = battle

        if battle.turn > self.battle_tracker.current_turn["turn_number"]:
            self.battle_tracker.start_turn(battle.turn)

        move = super().choose_move(battle)

        move_name = self._extract_move_name(move, battle)
        active_pokemon = battle.active_pokemon
        pokemon_name = active_pokemon.species if active_pokemon else "Unknown"

        self.battle_tracker.add_event(f"{self.bot_name}'s {pokemon_name} used {move_name}")

        return move

    def _extract_move_name(self, order, battle):
        if hasattr(order, 'order') and order.order:
            move = order.order
            if hasattr(move, 'id'):
                return move.id.replace('-', ' ').title()
            elif hasattr(move, 'species'):
                return f"Switch to {move.species}"
        return "Unknown Move"

def create_player(bot_type, bot_name, battle_tracker):
    """Create a player instance based on bot type"""
    if bot_type == "random":
        return TrackedRandomPlayer(
            battle_tracker,
            bot_name,
            battle_format="gen9randombattle",
            server_configuration=LOCAL_SERVER,
            max_concurrent_battles=1
        )
    elif bot_type == "maxdamage":
        return TrackedMaxDamagePlayer(
            battle_tracker,
            bot_name,
            battle_format="gen9randombattle",
            server_configuration=LOCAL_SERVER,
            max_concurrent_battles=1
        )
    elif bot_type == "custom":
        player = TrackedCustomStrategyPlayer(
            battle_tracker,
            bot_name,
            battle_format="gen9randombattle",
            server_configuration=LOCAL_SERVER,
            max_concurrent_battles=1
        )
        # Add strategy checks
        player.add_check("super_effective", check_super_effective, priority=3)
        player.add_check("stab", check_stab_bonus, priority=2)
        player.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)
        player.add_check("base_power", check_high_base_power, priority=1)
        player.add_check("accuracy", check_high_accuracy, priority=1)
        return player
    else:
        raise ValueError(f"Unknown bot type: {bot_type}")

async def run_battle(bot1_type, bot2_type):
    """Run a local battle between two bots and return results"""
    battle_tracker = BattleTracker()

    player1 = create_player(bot1_type, "Bot 1", battle_tracker)
    player2 = create_player(bot2_type, "Bot 2", battle_tracker)

    try:
        # Start the battle - this runs locally without Showdown server
        await player1.battle_against(player2, n_battles=1)

        # Finalize tracking
        battle_tracker.finalize()

        # Determine winner
        if player1.n_won_battles > player2.n_won_battles:
            winner = f"Bot 1 ({bot1_type.title()})"
        elif player2.n_won_battles > player1.n_won_battles:
            winner = f"Bot 2 ({bot2_type.title()})"
        else:
            winner = "Tie"

        battle_log = battle_tracker.get_battle_log()

        return {
            "winner": winner,
            "battle_log": battle_log,
            "bot1_wins": player1.n_won_battles,
            "bot2_wins": player2.n_won_battles
        }
    finally:
        await player1.close()
        await player2.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/battle', methods=['POST'])
def battle():
    data = request.json
    bot1_type = data.get('bot1')
    bot2_type = data.get('bot2')

    if not bot1_type or not bot2_type:
        return jsonify({"error": "Both bot types must be specified"}), 400

    # Run the battle
    try:
        result = asyncio.run(run_battle(bot1_type, bot2_type))
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
