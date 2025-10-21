import asyncio
from poke_env import ShowdownServerConfiguration, AccountConfiguration
from logging_player import LoggingRandomPlayer, CSVBattleLogger, SQLiteBattleLogger


async def random_battle_csv(n_battles: int = 100):
    print("Starting random battles with CSV logging on Pokemon Showdown...")

    logger1 = CSVBattleLogger("battle_data/Bot_Naila_random.csv")

    player1 = LoggingRandomPlayer(
        battle_logger=logger1,
        battle_format="gen9randombattle",
        account_configuration=AccountConfiguration("Bot_Naila", "Naila"),
        server_configuration=ShowdownServerConfiguration,
        start_timer_on_battle_start=True,
    )

    await player1.ladder(n_battles)

    print(f"\nBattles complete! Data logged to battle_data/Bot_Naila_random.csv")
    print(f"Player {player1.username} won {player1.n_won_battles} / {player1.n_finished_battles}")
    if player1.n_finished_battles > 0:
        print(f"Win rate: {player1.n_won_battles / player1.n_finished_battles * 100:.1f}%")


async def random_battle_sqlite(n_battles: int = 100):
    print("Starting random battles with SQLite logging on Pokemon Showdown...")

    logger1 = SQLiteBattleLogger("battle_data/Bot_Naila_random.db")

    player1 = LoggingRandomPlayer(
        battle_logger=logger1,
        battle_format="gen9randombattle",
        account_configuration=AccountConfiguration("Bot_Naila", "Naila"),
        server_configuration=ShowdownServerConfiguration,
        start_timer_on_battle_start=True,
    )

    await player1.ladder(n_battles)

    print(f"\nBattles complete! Data logged to battle_data/Bot_Naila_random.db")
    print(f"Player {player1.username} won {player1.n_won_battles} / {player1.n_finished_battles}")
    if player1.n_finished_battles > 0:
        print(f"Win rate: {player1.n_won_battles / player1.n_finished_battles * 100:.1f}%")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "sqlite":
        print("Using SQLite logging format")
        asyncio.get_event_loop().run_until_complete(random_battle_sqlite(n_battles=1))
    else:
        print("Using CSV logging format (use 'python random_battle_logged.py sqlite' for SQLite)")
        asyncio.get_event_loop().run_until_complete(random_battle_csv(n_battles=1))
