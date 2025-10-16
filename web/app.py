"""
Flask backend for Pokemon Battle Website
Simple bot vs bot battles with Showdown viewing capability
"""
import asyncio
import threading
import json
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
from poke_env import ServerConfiguration, AccountConfiguration
from poke_env.player import RandomPlayer, MaxBasePowerPlayer
import sys
import os
from datetime import datetime
from queue import Queue
import time

# Add parent directory to path to import bot classes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_strategy_bot import CustomStrategyPlayer, check_super_effective, check_stab_bonus, check_avoid_ineffective, check_high_base_power

app = Flask(__name__)
CORS(app)

# Local Showdown server configuration
LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)

# Store active battles and their status
active_battles = {}

class BattleMonitor:
    """Monitor and track battle progress"""
    def __init__(self, battle_id):
        self.battle_id = battle_id
        self.events = Queue()
        self.bot = None
        self.opponent = None
        self.bot_type = None
        self.opponent_type = None
        self.battle_log = []
        self.status = "initializing"

    def log_event(self, event_type, data):
        """Log an event for this battle"""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.battle_log.append(event)
        self.events.put(event)

    def get_summary(self):
        """Get a summary of the battle"""
        battle_url = None
        if self.bot and hasattr(self.bot, 'battles') and self.bot.battles:
            # Get the most recent battle
            for battle_tag in self.bot.battles.keys():
                battle_url = f"http://localhost:8000/{battle_tag}"
                break

        # Determine winner
        winner = None
        if self.status == "completed" and self.bot:
            bot_wins = self.bot.n_won_battles
            opponent_bot = None
            # Try to get opponent wins
            for event in self.battle_log:
                if event.get("type") == "battle_end":
                    opponent_wins = event["data"].get("opponent_wins", 0)
                    if bot_wins > opponent_wins:
                        winner = self.bot_type
                    elif opponent_wins > bot_wins:
                        winner = self.opponent_type
                    break

        return {
            "battle_id": self.battle_id,
            "status": self.status,
            "bot": self.bot.username if self.bot else None,
            "opponent": self.opponent if self.opponent else None,
            "bot_type": self.bot_type,
            "opponent_type": self.opponent_type,
            "bot_wins": self.bot.n_won_battles if self.bot else 0,
            "bot_finished": self.bot.n_finished_battles if self.bot else 0,
            "event_count": len(self.battle_log),
            "battle_url": battle_url,
            "winner": winner
        }

def create_bot(bot_type, username="WebBot"):
    """Create a bot instance based on the type"""
    if bot_type == "random":
        return RandomPlayer(
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
            account_configuration=AccountConfiguration(username, None)
        )
    elif bot_type == "maxdamage":
        return MaxBasePowerPlayer(
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
            account_configuration=AccountConfiguration(username, None)
        )
    elif bot_type == "custom":
        bot = CustomStrategyPlayer(
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
            account_configuration=AccountConfiguration(username, None)
        )
        # Add strategy checks
        bot.add_check("super_effective", check_super_effective, priority=3)
        bot.add_check("stab", check_stab_bonus, priority=2)
        bot.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)
        bot.add_check("base_power", check_high_base_power, priority=1)
        return bot
    else:
        raise ValueError(f"Unknown bot type: {bot_type}")

async def run_battle(battle_id, bot_type, opponent_type, n_battles=1):
    """Run a battle asynchronously and track it"""
    monitor = active_battles[battle_id]

    try:
        monitor.status = "creating_bots"
        monitor.bot_type = bot_type
        monitor.opponent_type = opponent_type
        monitor.log_event("info", {"message": f"Creating {bot_type} bot..."})

        bot = create_bot(bot_type, f"Player1_{battle_id[:8]}")
        monitor.bot = bot

        # Create opponent bot
        monitor.log_event("info", {"message": f"Creating opponent {opponent_type} bot..."})
        opponent_bot = create_bot(opponent_type, f"Player2_{battle_id[:8]}")
        monitor.opponent = opponent_bot.username

        monitor.status = "battling"
        monitor.log_event("battle_start", {
            "bot_type": bot_type,
            "opponent": opponent_bot.username,
            "opponent_type": opponent_type,
            "n_battles": n_battles
        })

        # Battle the bots against each other
        await bot.battle_against(opponent_bot, n_battles=n_battles)

        # Track battle URL during battle
        await asyncio.sleep(2)  # Wait for battle to start
        if bot.battles:
            for battle_tag in bot.battles.keys():
                battle_url = f"http://localhost:8000/{battle_tag}"
                monitor.log_event("battle_url", {
                    "url": battle_url,
                    "battle_tag": battle_tag
                })
                break

        # Wait for battle to finish
        while bot.n_finished_battles < n_battles:
            await asyncio.sleep(0.5)

        monitor.status = "completed"
        monitor.log_event("battle_end", {
            "wins": bot.n_won_battles,
            "losses": bot.n_finished_battles - bot.n_won_battles,
            "total": bot.n_finished_battles,
            "opponent_wins": opponent_bot.n_won_battles
        })

    except Exception as e:
        monitor.status = "error"
        monitor.log_event("error", {"message": str(e)})
        print(f"Error in battle {battle_id}: {e}")

def start_battle_thread(battle_id, bot_type, opponent_type, n_battles):
    """Start a battle in a new event loop (for threading)"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_battle(battle_id, bot_type, opponent_type, n_battles))
    loop.close()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/bots', methods=['GET'])
def get_bots():
    """Get list of available bots"""
    bots = [
        {
            "id": "random",
            "name": "Random Bot",
            "description": "Makes completely random moves"
        },
        {
            "id": "maxdamage",
            "name": "Max Damage Bot",
            "description": "Always chooses the move with the highest base power"
        },
        {
            "id": "custom",
            "name": "Custom Strategy Bot",
            "description": "Uses a sophisticated strategy with type effectiveness, STAB, and more"
        }
    ]
    return jsonify(bots)

@app.route('/api/opponents', methods=['GET'])
def get_opponents():
    """Get list of available opponent bots"""
    opponents = [
        {
            "id": "random",
            "name": "Random Bot",
            "description": "Random move selection"
        },
        {
            "id": "maxdamage",
            "name": "Max Damage Bot",
            "description": "Highest base power moves"
        },
        {
            "id": "custom",
            "name": "Custom Strategy Bot",
            "description": "Advanced strategy"
        }
    ]
    return jsonify(opponents)

@app.route('/api/battle/start', methods=['POST'])
def start_battle():
    """Start a new battle"""
    data = request.json
    bot_type = data.get('bot_type')
    opponent_type = data.get('opponent_type', 'random')
    n_battles = data.get('n_battles', 1)

    if not bot_type or not opponent_type:
        return jsonify({"error": "bot_type and opponent_type are required"}), 400

    # Generate unique battle ID
    battle_id = f"battle_{int(time.time() * 1000)}"

    # Create battle monitor
    monitor = BattleMonitor(battle_id)
    active_battles[battle_id] = monitor

    # Start battle in background thread
    thread = threading.Thread(
        target=start_battle_thread,
        args=(battle_id, bot_type, opponent_type, n_battles)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "battle_id": battle_id,
        "status": "started"
    })

@app.route('/api/battle/<battle_id>/status', methods=['GET'])
def get_battle_status(battle_id):
    """Get the status of a battle"""
    if battle_id not in active_battles:
        return jsonify({"error": "Battle not found"}), 404

    monitor = active_battles[battle_id]
    return jsonify(monitor.get_summary())

@app.route('/api/battle/<battle_id>/events')
def battle_events_stream(battle_id):
    """Stream battle events using Server-Sent Events"""
    if battle_id not in active_battles:
        return jsonify({"error": "Battle not found"}), 404

    monitor = active_battles[battle_id]

    def generate():
        # Send existing events first
        for event in monitor.battle_log:
            yield f"data: {json.dumps(event)}\n\n"

        # Stream new events
        while monitor.status not in ["completed", "error"]:
            try:
                event = monitor.events.get(timeout=1)
                yield f"data: {json.dumps(event)}\n\n"
            except:
                # Send keepalive
                yield f": keepalive\n\n"

        # Send final status
        yield f"data: {json.dumps({'type': 'done', 'status': monitor.status})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/battles', methods=['GET'])
def list_battles():
    """List all battles"""
    battles = [monitor.get_summary() for monitor in active_battles.values()]
    return jsonify(battles)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    print("Pokemon Battle Website starting...")
    print("Server will be available at http://localhost:5000")
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
