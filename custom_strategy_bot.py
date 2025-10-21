from typing import List, Callable, Optional
from poke_env.player import Player
from poke_env.battle import AbstractBattle
from logging_player import BattleDataLogger, CSVBattleLogger

class MoveCheck:
    def __init__(self, name: str, check_function: Callable, priority: int = 1):
        self.name = name
        self.check_function = check_function
        self.priority = priority

    def evaluate(self, battle: AbstractBattle, move, target) -> float:
        try:
            return self.check_function(battle, move, target) * self.priority
        except Exception as e:
            print(f"Warning: Check '{self.name}' failed: {e}")
            return 0.0

class CustomStrategyPlayer(Player):
    def __init__(self, battle_logger: Optional[BattleDataLogger] = None, battle_format: str = "gen8randombattle", **kwargs):
        super().__init__(battle_format=battle_format, **kwargs)
        self.battle_logger = battle_logger
        self.move_checks: List[MoveCheck] = []
        self.debug = False

    def add_check(self, name: str, check_function: Callable, priority: int = 1):
        self.move_checks.append(MoveCheck(name, check_function, priority))

    def choose_move(self, battle: AbstractBattle):
        if not self.move_checks:
            return self.choose_default_move(battle)

        active = battle.active_pokemon
        opponent_active = battle.opponent_active_pokemon

        if battle.can_dynamax and active and opponent_active:
            if opponent_active.current_hp_fraction > 0.6 and active.current_hp_fraction > 0.4:
                if self.debug:
                    print(f"\n*** DYNAMAXING {active.species} ***")

        available_switches = battle.available_switches

        if available_switches and opponent_active:
            best_switch_score = 0
            best_switch = None

            for switch_pokemon in available_switches:
                switch_score = self._evaluate_switch(battle, switch_pokemon, opponent_active)
                if switch_score > best_switch_score:
                    best_switch_score = switch_score
                    best_switch = switch_pokemon

            if best_switch_score > 150:
                if self.debug:
                    print(f"\n*** SWITCHING to {best_switch.species} (score: {best_switch_score:.1f}) ***")
                order = self.create_order(best_switch)
                if self.battle_logger:
                    self._log_battle_turn(battle, order)
                return order

        available_moves = battle.available_moves

        if not available_moves:
            return self.choose_default_move(battle)

        move_scores = {}

        for move in available_moves:
            total_score = 0.0

            if self.debug:
                print(f"\nEvaluating {move.id}:")

            for check in self.move_checks:
                score = check.evaluate(battle, move, opponent_active)
                total_score += score

                if self.debug and score > 0:
                    print(f"  {check.name}: +{score:.1f}")

            move_scores[move] = total_score

            if self.debug:
                print(f"  Total: {total_score:.1f}")

        best_move = max(move_scores.keys(), key=lambda m: move_scores[m])

        if self.debug:
            print(f"\nChosen: {best_move.id} (score: {move_scores[best_move]:.1f})")

        order = self.create_order(best_move, dynamax=battle.can_dynamax and active and opponent_active and opponent_active.current_hp_fraction > 0.6 and active.current_hp_fraction > 0.4)

        if self.battle_logger:
            self._log_battle_turn(battle, order)

        return order

    def _evaluate_switch(self, battle: AbstractBattle, switch_pokemon, opponent_active) -> float:
        score = 0.0
        active = battle.active_pokemon

        if not active or not opponent_active:
            return 0.0

        current_defensive_score = self._calc_defensive_matchup(active, opponent_active)
        switch_defensive_score = self._calc_defensive_matchup(switch_pokemon, opponent_active)
        defensive_improvement = switch_defensive_score - current_defensive_score

        if defensive_improvement > 1.0:
            score += 100 * defensive_improvement

        if active.current_hp_fraction < 0.25:
            score += 80
        elif active.current_hp_fraction < 0.5:
            score += 40

        if switch_pokemon.current_hp_fraction > active.current_hp_fraction + 0.3:
            score += 50

        if current_defensive_score > 0.5 and active.current_hp_fraction > 0.7:
            score -= 100

        return score

    def _calc_defensive_matchup(self, our_pokemon, opponent_pokemon) -> float:
        if not our_pokemon or not opponent_pokemon:
            return 0.0

        defense_score = 0.0

        if hasattr(our_pokemon, 'base_stats'):
            defense_score += (our_pokemon.base_stats.get('def', 50) / 100.0)
            defense_score += (our_pokemon.base_stats.get('spd', 50) / 100.0)

        defense_score += our_pokemon.current_hp_fraction

        return defense_score

    def _log_battle_turn(self, battle: AbstractBattle, selected_move):
        try:
            from datetime import datetime

            active = battle.active_pokemon
            opponent = battle.opponent_active_pokemon

            selected_move_name = None
            selected_move_type = None
            selected_move_category = None
            selected_move_base_power = None
            selected_move_accuracy = None

            if hasattr(selected_move, 'order'):
                move = selected_move.order
                if hasattr(move, 'id'):
                    selected_move_name = move.id
                    selected_move_type = str(move.type) if hasattr(move, 'type') else None
                    selected_move_category = str(move.category) if hasattr(move, 'category') else None
                    selected_move_base_power = move.base_power if hasattr(move, 'base_power') else None
                    selected_move_accuracy = move.accuracy if hasattr(move, 'accuracy') else None

            turn_data = {
                'timestamp': datetime.now().isoformat(),
                'battle_tag': battle.battle_tag,
                'turn': battle.turn,
                'player_username': self.username,
                'active_pokemon': active.species if active else None,
                'active_hp': active.current_hp if active else None,
                'active_max_hp': active.max_hp if active else None,
                'active_hp_fraction': active.current_hp_fraction if active else None,
                'active_status': str(active.status) if active and active.status else None,
                'active_atk': active.base_stats.get('atk') if active else None,
                'active_def': active.base_stats.get('def') if active else None,
                'active_spa': active.base_stats.get('spa') if active else None,
                'active_spd': active.base_stats.get('spd') if active else None,
                'active_spe': active.base_stats.get('spe') if active else None,
                'opponent_pokemon': opponent.species if opponent else None,
                'opponent_hp': opponent.current_hp if opponent else None,
                'opponent_max_hp': opponent.max_hp if opponent else None,
                'opponent_hp_fraction': opponent.current_hp_fraction if opponent else None,
                'opponent_status': str(opponent.status) if opponent and opponent.status else None,
                'opponent_atk': opponent.base_stats.get('atk') if opponent else None,
                'opponent_def': opponent.base_stats.get('def') if opponent else None,
                'opponent_spa': opponent.base_stats.get('spa') if opponent else None,
                'opponent_spd': opponent.base_stats.get('spd') if opponent else None,
                'opponent_spe': opponent.base_stats.get('spe') if opponent else None,
                'selected_move': selected_move_name,
                'selected_move_type': selected_move_type,
                'selected_move_category': selected_move_category,
                'selected_move_base_power': selected_move_base_power,
                'selected_move_accuracy': selected_move_accuracy,
                'available_moves': '|'.join([m.id for m in battle.available_moves]) if battle.available_moves else '',
                'available_switches': '|'.join([p.species for p in battle.available_switches]) if battle.available_switches else '',
                'damage_dealt': 0,
                'fainted': 1 if opponent and opponent.fainted else 0,
                'won_battle': 1 if battle.finished and battle.won else (0 if battle.finished else None)
            }

            self.battle_logger.log_turn_data(turn_data)
        except Exception as e:
            print(f"Error logging turn data: {e}")

    def choose_default_move(self, battle: AbstractBattle):
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)

def check_super_effective(battle: AbstractBattle, move, target) -> float:
    if target and move.type and move.base_power > 0:
        effectiveness = target.damage_multiplier(move)
        if effectiveness > 1:
            return 100 * effectiveness
    return 0

def check_stab_bonus(battle: AbstractBattle, move, target) -> float:
    active_pokemon = battle.active_pokemon
    if active_pokemon and move.type:
        if move.type in [t.name for t in active_pokemon.types]:
            return 50
    return 0

def check_high_base_power(battle: AbstractBattle, move, target) -> float:
    return move.base_power if move.base_power else 0

def check_high_accuracy(battle: AbstractBattle, move, target) -> float:
    return move.accuracy if move.accuracy else 100

def check_status_moves(battle: AbstractBattle, move, target) -> float:
    if target and move.category.name == "STATUS" and not target.status:
        return 30
    return 0

def check_avoid_ineffective(battle: AbstractBattle, move, target) -> float:
    if target and move.type and move.base_power > 0:
        effectiveness = target.damage_multiplier(move)
        if effectiveness < 1:
            return -50 * (1 - effectiveness)
    return 0

def check_setup_on_resist(battle: AbstractBattle, move, target) -> float:
    active = battle.active_pokemon

    if not move.boosts or not active or not target:
        return 0

    total_boost = sum(move.boosts.values())
    if total_boost <= 0:
        return 0

    if target.current_hp_fraction < 0.3:
        return 60

    if active.current_hp_fraction > 0.7:
        return 50

    return 0

def check_switch_on_bad_matchup(battle: AbstractBattle, move, target) -> float:
    active = battle.active_pokemon

    if not target or not active or not move.type or move.base_power == 0:
        return 0

    effectiveness = target.damage_multiplier(move)

    if effectiveness < 0.5:
        return -100

    return 0

def check_offensive_pressure(battle: AbstractBattle, move, target) -> float:
    if not target or not move.base_power or move.base_power == 0:
        return 0

    if target.current_hp_fraction > 0.5:
        return move.base_power * 0.5

    return 0

if __name__ == "__main__":
    import asyncio
    from poke_env import ServerConfiguration, AccountConfiguration

    LOCAL_SERVER = ServerConfiguration(
        "ws://localhost:8000/showdown/websocket",
        "http://localhost:8000/action.php?"
    )

    async def run_custom_bot_vs_opponent():
        logger = CSVBattleLogger("battle_data/custom_strategy_bot.csv")

        bot = CustomStrategyPlayer(
            battle_logger=logger,
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
            account_configuration=AccountConfiguration("Bot_Naila", None),
        )

        bot.add_check("super_effective", check_super_effective, priority=4)
        bot.add_check("stab", check_stab_bonus, priority=2)
        bot.add_check("avoid_ineffective", check_avoid_ineffective, priority=3)
        bot.add_check("switch_bad_matchup", check_switch_on_bad_matchup, priority=3)
        bot.add_check("setup_on_resist", check_setup_on_resist, priority=2)
        bot.add_check("offensive_pressure", check_offensive_pressure, priority=2)
        bot.add_check("base_power", check_high_base_power, priority=1)
        bot.add_check("accuracy", check_high_accuracy, priority=1)
        bot.add_check("status", check_status_moves, priority=1)

        from poke_env.player import MaxBasePowerPlayer
        opponent = MaxBasePowerPlayer(
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
        )

        print("Starting custom strategy bot battles...")
        print(f"Active checks: {[check.name for check in bot.move_checks]}")
        print(f"{bot.username} vs {opponent.username}\n")

        n_battles = 5
        await bot.battle_against(opponent, n_battles=n_battles)

        print(f"\n{'='*50}")
        print(f"Results:")
        print(f"{'='*50}")
        print(f"{bot.username}: {bot.n_won_battles} wins / {bot.n_finished_battles} battles")
        print(f"{opponent.username}: {opponent.n_won_battles} wins / {opponent.n_finished_battles} battles")
        print(f"\nBattle data saved to battle_data/custom_strategy_bot.csv")

    asyncio.run(run_custom_bot_vs_opponent())
