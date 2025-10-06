import asyncio
from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.player import RandomPlayer
import numpy as np
from poke_env.teambuilder import Teambuilder
from vgc2025regj_teams import koraidon_regj_1
import requests

class SingleTeamBuilder(Teambuilder):
    def __init__(self, team):
        self.team = self.join_team(self.parse_showdown_team(team))

    def yield_team(self):
        return self.team

class LoggingRandomPlayer(RandomPlayer):
    def choose_move(self, battle):
        # no await here because choose_move is synchronous
        move = super().choose_move(battle)

        # move is a SingleBattleOrder object — it describes what the bot will do
        if move.is_attack:
            print(f"[{self.username}] Turn {battle.turn}: chose move {move.move.id}")
        elif move.is_switch:
            print(f"[{self.username}] Turn {battle.turn}: switched to {move.switch.name}")
        else:
            print(f"[{self.username}] Turn {battle.turn}: chose {move}")

        return move


async def main():

    builder = SingleTeamBuilder(koraidon_regj_1)

    bot = LoggingRandomPlayer(
        account_configuration=AccountConfiguration("peeepoo_man", "Raeh147611"),
        server_configuration=ShowdownServerConfiguration,
        #battle_format="gen9vgc2025regj",
        #team=builder,
    )

    
    print("Bot is online. Challenge 'peeepoo_man' from your OOmeNN account on Showdown.")
    await bot.send_challenges("OOmeNN", 1)
    print("Battle finished!")

if __name__ == "__main__":
    asyncio.run(main())
