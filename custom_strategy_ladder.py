import asyncio
from poke_env import ShowdownServerConfiguration, AccountConfiguration
from custom_strategy_bot import (
    CustomStrategyPlayer,
    CSVBattleLogger,
    check_super_effective,
    check_stab_bonus,
    check_high_base_power,
    check_high_accuracy,
    check_status_moves,
    check_avoid_ineffective,
    check_setup_on_resist,
    check_switch_on_bad_matchup,
    check_offensive_pressure,
)


async def run_ladder_bot(username: str, password: str, n_battles: int = 10):
    logger = CSVBattleLogger(f"battle_data/ladder_{username}.csv")

    bot = CustomStrategyPlayer(
        battle_logger=logger,
        battle_format="gen8randombattle",
        server_configuration=ShowdownServerConfiguration,
        account_configuration=AccountConfiguration(username, password),
        start_timer_on_battle_start=True,
    )


    bot.add_check("super_effective", check_super_effective, priority=4)

    bot.add_check("avoid_ineffective", check_avoid_ineffective, priority=3)
    bot.add_check("switch_bad_matchup", check_switch_on_bad_matchup, priority=3)

    bot.add_check("stab", check_stab_bonus, priority=2)

    bot.add_check("offensive_pressure", check_offensive_pressure, priority=2)

    bot.add_check("base_power", check_high_base_power, priority=1)

    bot.add_check("accuracy", check_high_accuracy, priority=1)

    bot.add_check("status", check_status_moves, priority=1)

    bot.add_check("setup_on_resist", check_setup_on_resist, priority=2)

    def prefer_priority_moves(battle, move, target):
        if target and move.priority > 0:
            if target.current_hp_fraction < 0.3:
                return 75
        return 0

    bot.add_check("priority_finisher", prefer_priority_moves, priority=3)



    print("="*60)
    print(f"Custom Strategy Bot - Ladder Mode")
    print("="*60)
    print(f"Username: {username}")
    print(f"Format: gen8randombattle")
    print(f"Battles to play: {n_battles}")
    print(f"\nActive strategy checks:")
    for i, check in enumerate(bot.move_checks, 1):
        print(f"  {i}. {check.name} (priority: {check.priority})")
    print("="*60)
    print("\nSearching for ladder opponents...\n")

    await bot.ladder(n_battles)

    print("\n" + "="*60)
    print("LADDER RESULTS")
    print("="*60)
    print(f"Battles completed: {bot.n_finished_battles}")
    print(f"Wins: {bot.n_won_battles}")
    print(f"Losses: {bot.n_finished_battles - bot.n_won_battles}")

    if bot.n_finished_battles > 0:
        win_rate = (bot.n_won_battles / bot.n_finished_battles) * 100
        print(f"Win rate: {win_rate:.1f}%")

    print(f"\nBattle data saved to: battle_data/ladder_{username}.csv")
    print("="*60)


if __name__ == "__main__":
    import sys

    USERNAME = "Bot_Naila"
    PASSWORD = "Naila"
    N_BATTLES = 10

    if len(sys.argv) > 1:
        USERNAME = sys.argv[1]
    if len(sys.argv) > 2:
        PASSWORD = sys.argv[2]
    if len(sys.argv) > 3:
        N_BATTLES = int(sys.argv[3])

    print("\n" + "="*60)
    print("CUSTOM STRATEGY BOT - OFFICIAL SHOWDOWN LADDER")
    print("="*60)
    print("\nUsage:")
    print(f"  python custom_strategy_ladder.py [username] [password] [n_battles]")
    print(f"\nCurrent settings:")
    print(f"  Username: {USERNAME}")
    print(f"  Battles: {N_BATTLES}")
    print("="*60 + "\n")

    asyncio.run(run_ladder_bot(USERNAME, PASSWORD, N_BATTLES))
