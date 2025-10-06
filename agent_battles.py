import asyncio
from poke_env import RandomPlayer, LocalhostServerConfiguration, ServerConfiguration
from poke_env.player import Player

LOCAL_SERVER = ServerConfiguration("ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?")
async def agent_battles():
    # Use the built-in local configuration
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    second_player = RandomPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
    )

    print("Starting battle...")
    await random_player.battle_against(second_player, n_battles=100)
    print("Battle complete!")
    print(
    f"Player {random_player.username} won {random_player.n_won_battles} out of {random_player.n_finished_battles} played"
    )
    print(
        f"Player {second_player.username} won {second_player.n_won_battles} out of {second_player.n_finished_battles} played"
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(agent_battles())
