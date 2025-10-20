"""
Script to run battles between different bots and analyze the results
"""
import asyncio
import json
from poke_env.player import RandomPlayer, MaxBasePowerPlayer
from poke_env import ServerConfiguration
from custom_strategy_bot import CustomStrategyPlayer, check_super_effective, check_stab_bonus, check_avoid_ineffective, check_high_base_power, check_high_accuracy

LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)

async def run_bot_comparison(n_battles=50):
    """Run battles between all bot combinations"""

    results = {
        "random_vs_maxdamage": {"p1_wins": 0, "p2_wins": 0},
        "random_vs_custom": {"p1_wins": 0, "p2_wins": 0},
        "maxdamage_vs_custom": {"p1_wins": 0, "p2_wins": 0},
    }

    print(f"Running {n_battles} battles for each matchup...\n")

    # Random vs MaxDamage
    print("=== Random vs MaxDamage ===")
    random1 = RandomPlayer(battle_format="gen9randombattle", server_configuration=LOCAL_SERVER, max_concurrent_battles=10)
    maxdamage1 = MaxBasePowerPlayer(battle_format="gen9randombattle", server_configuration=LOCAL_SERVER, max_concurrent_battles=10)

    await random1.battle_against(maxdamage1, n_battles=n_battles)
    results["random_vs_maxdamage"]["p1_wins"] = random1.n_won_battles
    results["random_vs_maxdamage"]["p2_wins"] = maxdamage1.n_won_battles

    print(f"Random: {random1.n_won_battles} wins")
    print(f"MaxDamage: {maxdamage1.n_won_battles} wins\n")

    await random1.close()
    await maxdamage1.close()

    # Random vs Custom
    print("=== Random vs Custom Strategy ===")
    random2 = RandomPlayer(battle_format="gen9randombattle", server_configuration=LOCAL_SERVER, max_concurrent_battles=10)
    custom1 = CustomStrategyPlayer(battle_logger=None, battle_format="gen9randombattle", server_configuration=LOCAL_SERVER, max_concurrent_battles=10)
    custom1.add_check("super_effective", check_super_effective, priority=3)
    custom1.add_check("stab", check_stab_bonus, priority=2)
    custom1.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)
    custom1.add_check("base_power", check_high_base_power, priority=1)
    custom1.add_check("accuracy", check_high_accuracy, priority=1)

    await random2.battle_against(custom1, n_battles=n_battles)
    results["random_vs_custom"]["p1_wins"] = random2.n_won_battles
    results["random_vs_custom"]["p2_wins"] = custom1.n_won_battles

    print(f"Random: {random2.n_won_battles} wins")
    print(f"Custom: {custom1.n_won_battles} wins\n")

    await random2.close()
    await custom1.close()

    # MaxDamage vs Custom
    print("=== MaxDamage vs Custom Strategy ===")
    maxdamage2 = MaxBasePowerPlayer(battle_format="gen9randombattle", server_configuration=LOCAL_SERVER, max_concurrent_battles=10)
    custom2 = CustomStrategyPlayer(battle_logger=None, battle_format="gen9randombattle", server_configuration=LOCAL_SERVER, max_concurrent_battles=10)
    custom2.add_check("super_effective", check_super_effective, priority=3)
    custom2.add_check("stab", check_stab_bonus, priority=2)
    custom2.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)
    custom2.add_check("base_power", check_high_base_power, priority=1)
    custom2.add_check("accuracy", check_high_accuracy, priority=1)

    await maxdamage2.battle_against(custom2, n_battles=n_battles)
    results["maxdamage_vs_custom"]["p1_wins"] = maxdamage2.n_won_battles
    results["maxdamage_vs_custom"]["p2_wins"] = custom2.n_won_battles

    print(f"MaxDamage: {maxdamage2.n_won_battles} wins")
    print(f"Custom: {custom2.n_won_battles} wins\n")

    await maxdamage2.close()
    await custom2.close()

    # Save results
    with open('project_site/battle_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("Results saved to project_site/battle_results.json")
    return results

if __name__ == "__main__":
    asyncio.run(run_bot_comparison(n_battles=50))
