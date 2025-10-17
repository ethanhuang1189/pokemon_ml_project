"""
Quick test battle to get a live battle link
"""
import asyncio
from poke_env import ServerConfiguration, AccountConfiguration
from poke_env.player import RandomPlayer, MaxBasePowerPlayer

# Local Showdown server configuration
LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)

async def test_battle():
    """Run a quick battle and print the link"""

    # Create two bots
    bot1 = RandomPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
        account_configuration=AccountConfiguration("TestBot1", None)
    )

    bot2 = MaxBasePowerPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
        account_configuration=AccountConfiguration("TestBot2", None)
    )

    print("Starting battle between RandomPlayer and MaxDamagePlayer...")
    print("Waiting for battle to start...\n")

    # Start the battle
    battle_task = asyncio.create_task(bot1.battle_against(bot2, n_battles=1))

    # Wait for battle to start and get URL
    battle_url = None
    for i in range(40):  # Wait up to 10 seconds
        await asyncio.sleep(0.25)
        if bot1.battles:
            for battle_tag in bot1.battles.keys():
                battle_url = f"http://localhost:8000/{battle_tag}"
                print(f"BATTLE IS LIVE!")
                print(f"Watch here: {battle_url}")
                print(f"\nBattle tag: {battle_tag}")
                print("\nWaiting for battle to complete...")
                break
            break

    if not battle_url:
        print("ERROR: Battle didn't start in time!")
        return

    # Wait for battle to complete
    await battle_task

    print(f"\nBattle completed!")
    print(f"Results: {bot1.username} won {bot1.n_won_battles} / {bot1.n_finished_battles}")
    print(f"Results: {bot2.username} won {bot2.n_won_battles} / {bot2.n_finished_battles}")
    print(f"\nReplay still available at: {battle_url}")

if __name__ == "__main__":
    asyncio.run(test_battle())
