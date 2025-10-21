import asyncio
from poke_env import ShowdownServerConfiguration, AccountConfiguration
from poke_env.player import MaxBasePowerPlayer


async def run_ladder_bot(username: str, password: str, n_battles: int = 10):
    bot = MaxBasePowerPlayer(
        battle_format="gen8randombattle",
        server_configuration=ShowdownServerConfiguration,
        account_configuration=AccountConfiguration(username, password),
        start_timer_on_battle_start=True,
    )

    print("="*60)
    print(f"Max Damage Bot - Ladder Mode")
    print("="*60)
    print(f"Username: {username}")
    print(f"Format: gen8randombattle")
    print(f"Battles to play: {n_battles}")
    print(f"\nStrategy: Select moves with highest base power")
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
    print("MAX DAMAGE BOT - OFFICIAL SHOWDOWN LADDER")
    print("="*60)
    print("\nUsage:")
    print(f"  python maxdamage_ladder.py [username] [password] [n_battles]")
    print(f"\nCurrent settings:")
    print(f"  Username: {USERNAME}")
    print(f"  Battles: {N_BATTLES}")
    print("="*60 + "\n")

    asyncio.run(run_ladder_bot(USERNAME, PASSWORD, N_BATTLES))
