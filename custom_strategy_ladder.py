"""
Custom Strategy Bot for LADDER battles on official Pokemon Showdown.

This version connects to the official Pokemon Showdown server and plays on the ladder
against real players, logging all battle data.
"""
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
    check_preserve_pp,
    check_setup_moves,
)


async def run_ladder_bot(username: str, password: str, n_battles: int = 10):
    """
    Run custom strategy bot on the official Pokemon Showdown ladder.

    Args:
        username: Your Pokemon Showdown username
        password: Your Pokemon Showdown password
        n_battles: Number of ladder battles to play
    """
    # Create logger
    logger = CSVBattleLogger(f"battle_data/ladder_{username}.csv")

    # Create custom strategy bot
    bot = CustomStrategyPlayer(
        battle_logger=logger,
        battle_format="gen8randombattle",
        server_configuration=ShowdownServerConfiguration,
        account_configuration=AccountConfiguration(username, password),
        start_timer_on_battle_start=True,
    )

    # ========================================================================
    # CONFIGURE YOUR STRATEGY CHECKS HERE!
    # ========================================================================

    # Check 1: Strongly prefer super effective moves
    bot.add_check("super_effective", check_super_effective, priority=3)

    # Check 2: Prefer STAB moves
    bot.add_check("stab", check_stab_bonus, priority=2)

    # Check 3: Avoid not very effective moves
    bot.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)

    # Check 4: Consider base power
    bot.add_check("base_power", check_high_base_power, priority=1)

    # Check 5: Prefer accurate moves
    bot.add_check("accuracy", check_high_accuracy, priority=1)

    # Check 6: Try to inflict status
    bot.add_check("status", check_status_moves, priority=1)

    # Example custom check:
    def prefer_priority_moves(battle, move, target):
        """Prefer moves with priority when opponent is low HP."""
        if target and move.priority > 0:
            if target.current_hp_fraction < 0.3:  # Opponent below 30% HP
                return 75  # High score for priority moves
        return 0

    bot.add_check("priority_finisher", prefer_priority_moves, priority=2)

    # ========================================================================

    # Uncomment to see move scoring details during battles:
    # bot.debug = True

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

    # Play on the ladder
    await bot.ladder(n_battles)

    # Print results
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

    # Default credentials
    USERNAME = "Bot_Naila"
    PASSWORD = "Naila"
    N_BATTLES = 10

    # Parse command line arguments
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

    # Run the bot
    asyncio.run(run_ladder_bot(USERNAME, PASSWORD, N_BATTLES))
