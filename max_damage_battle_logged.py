import asyncio
from poke_env import ServerConfiguration
from logging_player import LoggingMaxDamagePlayer, CSVBattleLogger, SQLiteBattleLogger

LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)


async def max_damage_battle_csv(n_battles: int = 100):
    print("Starting max damage battles with CSV logging...")

    logger1 = CSVBattleLogger("battle_data/max_damage_player1.csv")
    logger2 = CSVBattleLogger("battle_data/max_damage_player2.csv")

    player1 = LoggingMaxDamagePlayer(
        battle_logger=logger1,
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    player2 = LoggingMaxDamagePlayer(
        battle_logger=logger2,
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    await player1.battle_against(player2, n_battles=n_battles)

    print(f"\nBattles complete! Data logged to battle_data/")
    print(f"Player {player1.username} won {player1.n_won_battles} / {player1.n_finished_battles}")
    print(f"Player {player2.username} won {player2.n_won_battles} / {player2.n_finished_battles}")


async def max_damage_battle_sqlite(n_battles: int = 100):
    print("Starting max damage battles with SQLite logging...")

    logger1 = SQLiteBattleLogger("battle_data/max_damage_player1.db")
    logger2 = SQLiteBattleLogger("battle_data/max_damage_player2.db")

    player1 = LoggingMaxDamagePlayer(
        battle_logger=logger1,
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    player2 = LoggingMaxDamagePlayer(
        battle_logger=logger2,
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    await player1.battle_against(player2, n_battles=n_battles)

    print(f"\nBattles complete! Data logged to battle_data/")
    print(f"Player {player1.username} won {player1.n_won_battles} / {player1.n_finished_battles}")
    print(f"Player {player2.username} won {player2.n_won_battles} / {player2.n_finished_battles}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "sqlite":
        print("Using SQLite logging format")
        asyncio.get_event_loop().run_until_complete(max_damage_battle_sqlite(n_battles=1))
    else:
        print("Using CSV logging format (use 'python max_damage_battle_logged.py sqlite' for SQLite)")
        asyncio.get_event_loop().run_until_complete(max_damage_battle_csv(n_battles=1))
