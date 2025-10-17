"""
Super simple Pokemon battle website
"""
import asyncio
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from poke_env import ServerConfiguration, AccountConfiguration
from poke_env.player import RandomPlayer, MaxBasePowerPlayer
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_strategy_bot import CustomStrategyPlayer, check_super_effective, check_stab_bonus, check_avoid_ineffective, check_high_base_power

app = Flask(__name__)
CORS(app)

LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)

def create_bot(bot_type, username):
    if bot_type == "random":
        return RandomPlayer(battle_format="gen8randombattle", server_configuration=LOCAL_SERVER, account_configuration=AccountConfiguration(username, None))
    elif bot_type == "maxdamage":
        return MaxBasePowerPlayer(battle_format="gen8randombattle", server_configuration=LOCAL_SERVER, account_configuration=AccountConfiguration(username, None))
    elif bot_type == "custom":
        bot = CustomStrategyPlayer(battle_format="gen8randombattle", server_configuration=LOCAL_SERVER, account_configuration=AccountConfiguration(username, None))
        bot.add_check("super_effective", check_super_effective, priority=3)
        bot.add_check("stab", check_stab_bonus, priority=2)
        bot.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)
        bot.add_check("base_power", check_high_base_power, priority=1)
        return bot

async def battle(bot1_type, bot2_type):
    import time
    timestamp = int(time.time() * 1000)

    bot1 = create_bot(bot1_type, f"Bot1_{timestamp}")
    bot2 = create_bot(bot2_type, f"Bot2_{timestamp}")

    battle_task = asyncio.create_task(bot1.battle_against(bot2, n_battles=1))

    # Get battle URL
    battle_url = None
    for i in range(40):
        await asyncio.sleep(0.25)
        if bot1.battles:
            battle_url = f"http://localhost:8000/{list(bot1.battles.keys())[0]}"
            break

    await battle_task

    # Cleanup
    try:
        await bot1.ps_client.stop_listening()
        await bot2.ps_client.stop_listening()
    except:
        pass

    winner = bot1_type if bot1.n_won_battles > 0 else bot2_type
    return {"winner": winner, "bot1_wins": bot1.n_won_battles, "bot2_wins": bot2.n_won_battles, "battle_url": battle_url}

@app.route('/')
def index():
    return render_template('index_basic.html')

@app.route('/battle', methods=['POST'])
def run_battle():
    data = request.json
    result = asyncio.run(battle(data['bot1'], data['bot2']))
    return jsonify(result)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    print("Server starting at http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
