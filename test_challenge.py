"""
Quick test to verify Bot_Naila can send challenges on local server
"""
import asyncio
from poke_env import AccountConfiguration, ServerConfiguration
from poke_env.player import RandomPlayer

# Local server config
LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)

async def test_challenge():
    print("Testing Bot_Naila challenge capability...")
    print("=" * 50)

    # Create Bot_Naila
    bot = RandomPlayer(
        battle_format="gen8randombattle",
        server_configuration=LOCAL_SERVER,
        account_configuration=AccountConfiguration("Bot_Naila", "Naila"),
    )

    print("✓ Bot_Naila created")

    # Get target username
    target = input("Enter your Showdown username to test challenge: ").strip()

    if not target:
        print("✗ No username provided")
        return

    print(f"\n📤 Sending challenge to '{target}'...")
    print("⏰ Make sure you're logged into Showdown now!")
    print()

    # Wait a moment for user to log in
    await asyncio.sleep(3)

    try:
        # Send challenge
        await bot.send_challenges(target, n_challenges=1)

        print("✓ Challenge sent!")
        print(f"✓ Check Showdown for challenge from Bot_Naila")
        print()
        print("Waiting for battle to complete (60 seconds max)...")

        # Wait for battle
        timeout = 60
        elapsed = 0
        while bot.n_finished_battles < 1 and elapsed < timeout:
            await asyncio.sleep(1)
            elapsed += 1

            if bot.battles:
                for battle_tag, battle in bot.battles.items():
                    print(f"⚔️  Battle active: {battle_tag}")
                    print(f"   URL: http://localhost:8000/{battle_tag}")

        if bot.n_finished_battles > 0:
            print()
            print("=" * 50)
            print("✓ BATTLE COMPLETED!")
            if bot.n_won_battles > 0:
                print("   Bot won!")
            else:
                print("   You won!")
            print("=" * 50)
        else:
            print()
            print("⏰ Timeout - battle didn't start")
            print("   Possible issues:")
            print("   - User not logged in")
            print("   - Username incorrect")
            print("   - Challenge declined")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print()
    print("Bot_Naila Challenge Test")
    print("=" * 50)
    print()
    print("Prerequisites:")
    print("1. Showdown server running (localhost:8000)")
    print("2. You logged into Showdown with a username")
    print()

    asyncio.run(test_challenge())
