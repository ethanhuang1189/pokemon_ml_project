import asyncio
from poke_env import Player, ShowdownServerConfiguration, AccountConfiguration, ServerConfiguration
from poke_env.player import RandomPlayer

#LOCAL_SERVER = ShowdownServerConfiguration(server_url="http://localhost:8000")
#custom_config = ServerConfiguration("ws://my.custom.host:5432/showdown/websocket", "authentication-endpoint.com/action.php?")

async def challengePlayer(challenger, challenger_name, challenged_player):
    print(f"{challenger_name} is challenging {challenged_player}")
    await challenger.send_challenges(challenged_player, n_challenges=1)
    for battle_tag, battle in challenger.battles.items():
        print(f"Format: {battle_tag}")
        if (battle.won == True):
            print(f"Winner is: {challenger_name}")
        else:
            print(f"Winner is: {challenged_player}")
    return 0


async def main():

    bot_naila = RandomPlayer(
        start_timer_on_battle_start=True,
        account_configuration=AccountConfiguration("peeepoo_man", "Raeh147611"),
        server_configuration=ShowdownServerConfiguration,
    )

    #player = Player(server_configuration=custom_config)

    #await bot_naila.send_challenges(bot_naila, player)
    await challengePlayer(bot_naila, "Bot_Naila", "OOmeNN")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())