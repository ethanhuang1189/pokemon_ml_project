import asyncio
from poke_env import RandomPlayer
from poke_env.data import GenData




async def main():
    Bot_Naila = RandomPlayer()
    second_player = RandomPlayer()
    #p1 = RandomPlayer(
    #    start_timer_on_battle_start=True,
    #    account_configuration=AccountConfiguration("Bot_Naila", "Naila"),
    #    server_configuration=ShowdownServerConfiguration,
    #)

    #p2 = RandomPlayer(
    #    start_timer_on_battle_start=True,
    #    account_configuration=AccountConfiguration("peeepoo_man", "Raeh147611"),
    #    server_configuration=ShowdownServerConfiguration,
    #)
    print("Starting Battle\n")
    await Bot_Naila.battle_against(second_player, n_battles=10)
    #await p1.battle_against(p2, n_challenges=1)
    #await p1.complete_current_battle()
    #for battle_tag, battle in p1.battles.items():
    print(
    f"Player {Bot_Naila.username} won {Bot_Naila.n_won_battles} out of {Bot_Naila.n_finished_battles} played"
    )
    print(
        f"Player {second_player.username} won {second_player.n_won_battles} out of {second_player.n_finished_battles} played"
    )

    # Looping over battles

    for battle_tag, battle in Bot_Naila.battles.items():
        if (battle.won == True):
            print(f"Bot_Naila won")
        else:
            print("second_player won")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
