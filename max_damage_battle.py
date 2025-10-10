import asyncio
from poke_env import MaxBasePowerPlayer, ServerConfiguration

LOCAL_SERVER = ServerConfiguration("ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?")

async def max_damage_battle():
    """Pit two MaxBasePowerPlayer bots against each other.

    Each bot always chooses the move with the highest base power available.
    """
    # Create first MaxBasePowerPlayer
    max_damage_player_1 = MaxBasePowerPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    # Create second MaxBasePowerPlayer
    max_damage_player_2 = MaxBasePowerPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    print("Starting battle between two max damage bots...")
    await max_damage_player_1.battle_against(max_damage_player_2, n_battles=100)
    print("Battle complete!")

    print(
        f"Player {max_damage_player_1.username} won {max_damage_player_1.n_won_battles} out of {max_damage_player_1.n_finished_battles} played"
    )
    print(
        f"Player {max_damage_player_2.username} won {max_damage_player_2.n_won_battles} out of {max_damage_player_2.n_finished_battles} played"
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(max_damage_battle())
