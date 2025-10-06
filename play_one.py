import asyncio
from poke_env import LocalhostServerConfiguration, Player, ShowdownServerConfiguration, AccountConfiguration
from poke_env.player import RandomPlayer

#LOCAL_SERVER = ShowdownServerConfiguration(server_url="http://localhost:8000")


async def main():
    random_player = RandomPlayer()
    second_player = RandomPlayer()
    p1 = RandomPlayer(
        start_timer_on_battle_start=True,
        account_configuration=AccountConfiguration("Bot_Naila", "Naila"),
        server_configuration=ShowdownServerConfiguration,
    )

    p2 = RandomPlayer(
        start_timer_on_battle_start=True,
        account_configuration=AccountConfiguration("peeepoo_man", "Raeh147611"),
        server_configuration=ShowdownServerConfiguration,
    )
    await random_player.battle_against(second_player, n_battles=1)
    #await p1.battle_against(p2, n_challenges=1)
    #await p1.complete_current_battle()
    #for battle_tag, battle in p1.battles.items():
    for battle_tag, battle in random_player.battles.items():
        print(f"Format: {battle_tag}")
        if (battle.won == True):
            print(f"Winner is: {random_player}")
        else:
            print(f"Winner is: {second_player}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
