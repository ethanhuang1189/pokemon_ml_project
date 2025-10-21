"""
Max Damage bot for Pokemon Showdown with comprehensive battle logging.

This bot connects to the official Pokemon Showdown server, challenges real players,
and logs all battle data for ML training purposes.
"""
import asyncio
from poke_env import ShowdownServerConfiguration, AccountConfiguration
from logging_player import LoggingMaxDamagePlayer, CSVBattleLogger, SQLiteBattleLogger


async def challenge_with_logging(
    username: str,
    password: str,
    opponent_username: str,
    n_challenges: int = 1,
    battle_format: str = "gen8randombattle",
    use_sqlite: bool = False
):
    """
    Challenge a player on Showdown with a max damage bot that logs battle data.

    Args:
        username: Your Showdown account username
        password: Your Showdown account password
        opponent_username: Username of the player to challenge
        n_challenges: Number of challenges to send (default 1)
        battle_format: Battle format (default "gen8randombattle")
        use_sqlite: If True, use SQLite; otherwise use CSV (default False)
    """
    # Create logger
    if use_sqlite:
        logger = SQLiteBattleLogger(f"battle_data/showdown_{username}.db")
        print(f"Using SQLite logging: battle_data/showdown_{username}.db")
    else:
        logger = CSVBattleLogger(f"battle_data/showdown_{username}.csv")
        print(f"Using CSV logging: battle_data/showdown_{username}.csv")

    # Create logging max damage player
    player = LoggingMaxDamagePlayer(
        battle_logger=logger,
        battle_format=battle_format,
        account_configuration=AccountConfiguration(username, password),
        server_configuration=ShowdownServerConfiguration,
        start_timer_on_battle_start=True,
    )

    print(f"\n{username} is challenging {opponent_username}...")
    print(f"Format: {battle_format}")
    print(f"Number of challenges: {n_challenges}\n")

    # Send challenges
    await player.send_challenges(opponent_username, n_challenges=n_challenges)

    # Wait for battles to complete
    while player.n_finished_battles < n_challenges:
        await asyncio.sleep(1)

    # Print results
    print(f"\n{'='*50}")
    print(f"Battle Results:")
    print(f"{'='*50}")

    for battle_tag, battle in player.battles.items():
        if battle.won:
            print(f"✓ {battle_tag}: WON")
        else:
            print(f"✗ {battle_tag}: LOST")

    print(f"\nTotal: {player.n_won_battles} wins out of {player.n_finished_battles} battles")
    print(f"Win rate: {player.n_won_battles / player.n_finished_battles * 100:.1f}%")
    print(f"\nBattle data saved to battle_data/showdown_{username}.{'db' if use_sqlite else 'csv'}")


async def accept_challenges_with_logging(
    username: str,
    password: str,
    battle_format: str = "gen8randombattle",
    use_sqlite: bool = False,
    max_concurrent_battles: int = 1
):
    """
    Accept challenges from other players on Showdown with logging.

    Args:
        username: Your Showdown account username
        password: Your Showdown account password
        battle_format: Battle format to accept (default "gen8randombattle")
        use_sqlite: If True, use SQLite; otherwise use CSV (default False)
        max_concurrent_battles: Maximum concurrent battles (default 1)
    """
    # Create logger
    if use_sqlite:
        logger = SQLiteBattleLogger(f"battle_data/showdown_{username}.db")
        print(f"Using SQLite logging: battle_data/showdown_{username}.db")
    else:
        logger = CSVBattleLogger(f"battle_data/showdown_{username}.csv")
        print(f"Using CSV logging: battle_data/showdown_{username}.csv")

    # Create logging max damage player
    player = LoggingMaxDamagePlayer(
        battle_logger=logger,
        battle_format=battle_format,
        account_configuration=AccountConfiguration(username, password),
        server_configuration=ShowdownServerConfiguration,
        start_timer_on_battle_start=True,
        max_concurrent_battles=max_concurrent_battles,
    )

    print(f"\n{username} is now accepting challenges...")
    print(f"Format: {battle_format}")
    print(f"Press Ctrl+C to stop\n")

    # Keep accepting challenges
    try:
        await player.accept_challenges(None, n_challenges=None)
    except KeyboardInterrupt:
        print("\n\nStopping...")

    # Print results
    print(f"\n{'='*50}")
    print(f"Session Results:")
    print(f"{'='*50}")
    print(f"Battles completed: {player.n_finished_battles}")
    print(f"Wins: {player.n_won_battles}")
    if player.n_finished_battles > 0:
        print(f"Win rate: {player.n_won_battles / player.n_finished_battles * 100:.1f}%")
    print(f"\nBattle data saved to battle_data/showdown_{username}.{'db' if use_sqlite else 'csv'}")


async def ladder_with_logging(
    username: str,
    password: str,
    n_battles: int = 10,
    battle_format: str = "gen8randombattle",
    use_sqlite: bool = False
):
    """
    Play on the ladder (ranked battles) with logging.

    Args:
        username: Your Showdown account username
        password: Your Showdown account password
        n_battles: Number of ladder battles to play (default 10)
        battle_format: Battle format (default "gen8randombattle")
        use_sqlite: If True, use SQLite; otherwise use CSV (default False)
    """
    # Create logger
    if use_sqlite:
        logger = SQLiteBattleLogger(f"battle_data/ladder_{username}.db")
        print(f"Using SQLite logging: battle_data/ladder_{username}.db")
    else:
        logger = CSVBattleLogger(f"battle_data/ladder_{username}.csv")
        print(f"Using CSV logging: battle_data/ladder_{username}.csv")

    # Create logging max damage player
    player = LoggingMaxDamagePlayer(
        battle_logger=logger,
        battle_format=battle_format,
        account_configuration=AccountConfiguration(username, password),
        server_configuration=ShowdownServerConfiguration,
        start_timer_on_battle_start=True,
    )

    print(f"\n{username} is playing on the ladder...")
    print(f"Format: {battle_format}")
    print(f"Number of battles: {n_battles}\n")

    # Play on ladder
    await player.ladder(n_battles)

    # Print results
    print(f"\n{'='*50}")
    print(f"Ladder Results:")
    print(f"{'='*50}")
    print(f"Battles completed: {player.n_finished_battles}")
    print(f"Wins: {player.n_won_battles}")
    print(f"Win rate: {player.n_won_battles / player.n_finished_battles * 100:.1f}%")
    print(f"\nBattle data saved to battle_data/ladder_{username}.{'db' if use_sqlite else 'csv'}")


if __name__ == "__main__":
    import sys

    # Example usage - modify these values or use command line arguments
    USERNAME = "Bot_Naila"
    PASSWORD = "Naila"

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

        if mode == "challenge":
            # Challenge a specific player
            if len(sys.argv) < 3:
                print("Usage: python showdown_max_damage_logger.py challenge <opponent_username> [sqlite]")
                sys.exit(1)

            opponent = sys.argv[2]
            use_sqlite = len(sys.argv) > 3 and sys.argv[3] == "sqlite"

            asyncio.get_event_loop().run_until_complete(
                challenge_with_logging(
                    username=USERNAME,
                    password=PASSWORD,
                    opponent_username=opponent,
                    n_challenges=1,
                    use_sqlite=use_sqlite
                )
            )

        elif mode == "accept":
            # Accept challenges from anyone
            use_sqlite = len(sys.argv) > 2 and sys.argv[2] == "sqlite"

            asyncio.get_event_loop().run_until_complete(
                accept_challenges_with_logging(
                    username=USERNAME,
                    password=PASSWORD,
                    use_sqlite=use_sqlite
                )
            )

        elif mode == "ladder":
            # Play on the ladder
            n_battles = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            use_sqlite = len(sys.argv) > 3 and sys.argv[3] == "sqlite"

            asyncio.get_event_loop().run_until_complete(
                ladder_with_logging(
                    username=USERNAME,
                    password=PASSWORD,
                    n_battles=n_battles,
                    use_sqlite=use_sqlite
                )
            )

        else:
            print(f"Unknown mode: {mode}")
            print("Available modes: challenge, accept, ladder")
            sys.exit(1)

    else:
        print("Pokemon Showdown Max Damage Logger")
        print("=" * 50)
        print("\nUsage:")
        print("  Challenge a player:")
        print("    python showdown_max_damage_logger.py challenge <opponent_username> [sqlite]")
        print("\n  Accept challenges:")
        print("    python showdown_max_damage_logger.py accept [sqlite]")
        print("\n  Play on ladder:")
        print("    python showdown_max_damage_logger.py ladder [n_battles] [sqlite]")
        print("\nNOTE: Edit USERNAME and PASSWORD in the script first!")
        print("=" * 50)
