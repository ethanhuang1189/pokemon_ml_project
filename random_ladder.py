"""
Random Bot for LADDER battles on official Pokemon Showdown.

This version connects to the official Pokemon Showdown server and plays on the ladder
against real players using random move selection.
"""
import asyncio
from poke_env import ShowdownServerConfiguration, AccountConfiguration
from poke_env.player import RandomPlayer


async def run_ladder_bot(username: str, password: str, n_battles: int = 10):
    """
    Run random bot on the official Pokemon Showdown ladder.

    Args:
        username: Your Pokemon Showdown username
        password: Your Pokemon Showdown password
        n_battles: Number of ladder battles to play
    """
    # Create random bot
    bot = RandomPlayer(
        battle_format="gen8randombattle",
        server_configuration=ShowdownServerConfiguration,
        account_configuration=AccountConfiguration(username, password),
        start_timer_on_battle_start=True,
    )

    print("="*60)
    print(f"Random Bot - Ladder Mode")
    print("="*60)
    print(f"Username: {username}")
    print(f"Format: gen8randombattle")
    print(f"Battles to play: {n_battles}")
    print(f"\nStrategy: Random move selection")
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
    print("RANDOM BOT - OFFICIAL SHOWDOWN LADDER")
    print("="*60)
    print("\nUsage:")
    print(f"  python random_ladder.py [username] [password] [n_battles]")
    print(f"\nCurrent settings:")
    print(f"  Username: {USERNAME}")
    print(f"  Battles: {N_BATTLES}")
    print("="*60 + "\n")

    # Run the bot
    asyncio.run(run_ladder_bot(USERNAME, PASSWORD, N_BATTLES))
