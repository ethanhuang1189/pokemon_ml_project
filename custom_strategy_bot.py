"""
Custom Strategy Bot with configurable move selection checks and battle logging.

This bot allows you to define custom logic for move selection by adding "checks"
that prioritize certain moves based on battle conditions.
"""
from typing import List, Callable, Optional
from poke_env.player import Player
from poke_env.battle import AbstractBattle
from logging_player import BattleDataLogger, CSVBattleLogger


class MoveCheck:
    """
    A check that evaluates moves and assigns priority scores.
    Higher scores = higher priority.
    """
    def __init__(self, name: str, check_function: Callable, priority: int = 1):
        """
        Args:
            name: Name of this check (for debugging)
            check_function: Function that takes (battle, move, target) and returns a score
            priority: Weight/importance of this check (higher = more important)
        """
        self.name = name
        self.check_function = check_function
        self.priority = priority

    def evaluate(self, battle: AbstractBattle, move, target) -> float:
        """Evaluate this check for a given move."""
        try:
            return self.check_function(battle, move, target) * self.priority
        except Exception as e:
            print(f"Warning: Check '{self.name}' failed: {e}")
            return 0.0


class CustomStrategyPlayer(Player):
    """
    A Pokemon player that uses a customizable system of checks to select moves.
    """

    def __init__(
        self,
        battle_logger: Optional[BattleDataLogger] = None,
        battle_format: str = "gen8randombattle",
        **kwargs
    ):
        super().__init__(battle_format=battle_format, **kwargs)
        self.battle_logger = battle_logger
        self.move_checks: List[MoveCheck] = []
        self.debug = False  # Set to True to see scoring details

    def add_check(self, name: str, check_function: Callable, priority: int = 1):
        """
        Add a move selection check.

        Args:
            name: Name of the check
            check_function: Function that scores a move (higher = better)
            priority: Weight of this check (default 1)

        Example:
            def prefer_super_effective(battle, move, target):
                if target and move.type and move.base_power > 0:
                    effectiveness = target.damage_multiplier(move)
                    if effectiveness > 1:
                        return 100  # High score for super effective
                return 0

            bot.add_check("super_effective", prefer_super_effective, priority=2)
        """
        self.move_checks.append(MoveCheck(name, check_function, priority))

    def choose_move(self, battle: AbstractBattle):
        # Note: Logging happens after move selection to capture the chosen move

        # If we have no checks, use a simple strategy
        if not self.move_checks:
            return self.choose_default_move(battle)

        # Check if we should switch (evaluate switches separately)
        available_switches = battle.available_switches
        opponent_active = battle.opponent_active_pokemon

        if available_switches and opponent_active:
            # Check if switching would be beneficial
            best_switch_score = 0
            best_switch = None

            for switch_pokemon in available_switches:
                switch_score = self._evaluate_switch(battle, switch_pokemon, opponent_active)
                if switch_score > best_switch_score:
                    best_switch_score = switch_score
                    best_switch = switch_pokemon

            # If switch score is very high (defensive switch needed), do it
            if best_switch_score > 150:  # High threshold for switching
                if self.debug:
                    print(f"\n*** SWITCHING to {best_switch.species} (score: {best_switch_score:.1f}) ***")
                order = self.create_order(best_switch)
                if self.battle_logger:
                    self._log_battle_turn(battle, order)
                return order

        # Get available moves
        available_moves = battle.available_moves

        if not available_moves:
            return self.choose_default_move(battle)

        # Score each move using all checks
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

        # Choose the highest scoring move
        best_move = max(move_scores.keys(), key=lambda m: move_scores[m])

        if self.debug:
            print(f"\nChosen: {best_move.id} (score: {move_scores[best_move]:.1f})")

        order = self.create_order(best_move)

        # Log after choosing the move
        if self.battle_logger:
            self._log_battle_turn(battle, order)

        return order

    def _evaluate_switch(self, battle: AbstractBattle, switch_pokemon, opponent_active) -> float:
        """
        Evaluate if switching to a specific Pokemon is beneficial.
        Returns higher score if switch_pokemon resists opponent better than current Pokemon.
        """
        score = 0.0
        active = battle.active_pokemon

        if not active or not opponent_active:
            return 0.0

        # Calculate defensive matchup for current Pokemon vs opponent
        current_defensive_score = self._calc_defensive_matchup(active, opponent_active)

        # Calculate defensive matchup for potential switch Pokemon vs opponent
        switch_defensive_score = self._calc_defensive_matchup(switch_pokemon, opponent_active)

        # If switch Pokemon has significantly better defensive matchup, prefer switching
        defensive_improvement = switch_defensive_score - current_defensive_score

        if defensive_improvement > 1.0:  # Switch Pokemon resists better
            score += 100 * defensive_improvement

        # Additional factors:

        # If current Pokemon is very low HP, prefer switching
        if active.current_hp_fraction < 0.25:
            score += 80
        elif active.current_hp_fraction < 0.5:
            score += 40

        # Prefer switch Pokemon with higher HP
        if switch_pokemon.current_hp_fraction > active.current_hp_fraction + 0.3:
            score += 50

        # Don't switch if already have good matchup and high HP
        if current_defensive_score > 0.5 and active.current_hp_fraction > 0.7:
            score -= 100

        return score

    def _calc_defensive_matchup(self, our_pokemon, opponent_pokemon) -> float:
        """
        Calculate how well our_pokemon handles opponent_pokemon defensively.
        Returns higher values for better defensive matchups (resisting opponent's attacks).
        """
        if not our_pokemon or not opponent_pokemon:
            return 0.0

        # Check type-based defensive advantage
        # We'll estimate how much damage opponent can do to us based on types

        # Get opponent's potential STAB moves (their type)
        worst_multiplier = 1.0

        for opponent_type in opponent_pokemon.types:
            if opponent_type:
                # Check how much damage this type would do to our Pokemon
                # We approximate by checking type matchups
                for our_type in our_pokemon.types:
                    if our_type:
                        # Check matchup - this is simplified
                        # In reality, we'd need type chart data
                        # For now, we'll use a heuristic
                        pass

        # Simplified approach: Check if we have type advantage
        # Use available moves to estimate
        if hasattr(our_pokemon, 'moves') and our_pokemon.moves:
            for move_id in our_pokemon.moves:
                try:
                    # Check if we have super effective moves against opponent
                    if opponent_pokemon:
                        # This is where we'd check damage multiplier
                        pass
                except:
                    pass

        # Return a score based on defensive stats and HP
        defense_score = 0.0

        # Higher defense/HP = better defensive matchup
        if hasattr(our_pokemon, 'base_stats'):
            defense_score += (our_pokemon.base_stats.get('def', 50) / 100.0)
            defense_score += (our_pokemon.base_stats.get('spd', 50) / 100.0)

        defense_score += our_pokemon.current_hp_fraction

        return defense_score

    def _log_battle_turn(self, battle: AbstractBattle, selected_move):
        """Log the current battle turn data."""
        try:
            from datetime import datetime

            active = battle.active_pokemon
            opponent = battle.opponent_active_pokemon

            # Extract move information
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
        """Fallback move selection (max damage)."""
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)


# ============================================================================
# PREDEFINED CHECK FUNCTIONS
# You can use these or create your own!
# ============================================================================

def check_super_effective(battle: AbstractBattle, move, target) -> float:
    """Prefer moves that are super effective."""
    if target and move.type and move.base_power > 0:
        effectiveness = target.damage_multiplier(move)
        if effectiveness > 1:
            return 100 * effectiveness  # Score based on effectiveness multiplier
    return 0


def check_stab_bonus(battle: AbstractBattle, move, target) -> float:
    """Prefer moves that get STAB (Same Type Attack Bonus)."""
    active_pokemon = battle.active_pokemon
    if active_pokemon and move.type:
        if move.type in [t.name for t in active_pokemon.types]:
            return 50  # Bonus for STAB moves
    return 0


def check_high_base_power(battle: AbstractBattle, move, target) -> float:
    """Prefer moves with higher base power."""
    return move.base_power if move.base_power else 0


def check_high_accuracy(battle: AbstractBattle, move, target) -> float:
    """Prefer more accurate moves."""
    return move.accuracy if move.accuracy else 100


def check_status_moves(battle: AbstractBattle, move, target) -> float:
    """Prefer status moves when opponent isn't statused yet."""
    if target and move.category.name == "STATUS" and not target.status:
        return 30  # Give status moves some priority if opponent isn't statused
    return 0


def check_avoid_ineffective(battle: AbstractBattle, move, target) -> float:
    """Penalize moves that are not very effective."""
    if target and move.type and move.base_power > 0:
        effectiveness = target.damage_multiplier(move)
        if effectiveness < 1:
            return -50 * (1 - effectiveness)  # Negative score for ineffective moves
    return 0


def check_preserve_pp(battle: AbstractBattle, move, target) -> float:
    """Slight penalty for using low PP moves (to preserve them)."""
    if move.current_pp and move.max_pp:
        pp_ratio = move.current_pp / move.max_pp
        if pp_ratio < 0.3:  # Less than 30% PP remaining
            return -20
    return 0


def check_setup_moves(battle: AbstractBattle, move, target) -> float:
    """Prefer setup moves (stat boosting) early in battle."""
    if move.boosts and battle.turn < 3:  # First few turns
        # Check if move boosts our stats
        active_pokemon = battle.active_pokemon
        if active_pokemon:
            total_boost = sum(move.boosts.values())
            if total_boost > 0:
                return 40  # Good to set up early
    return 0


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import asyncio
    from poke_env import ServerConfiguration, AccountConfiguration

    LOCAL_SERVER = ServerConfiguration(
        "ws://localhost:8000/showdown/websocket",
        "http://localhost:8000/action.php?"
    )

    async def run_custom_bot_vs_opponent():
        """Example: Run custom strategy bot against another bot for testing."""

        # Create logger
        logger = CSVBattleLogger("battle_data/custom_strategy_bot.csv")

        # Create custom strategy bot
        # Note: Local server doesn't require password authentication
        bot = CustomStrategyPlayer(
            battle_logger=logger,
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
            account_configuration=AccountConfiguration("Bot_Naila", None),
        )

        # ========================================================================
        # ADD YOUR CUSTOM CHECKS HERE!
        # ========================================================================

        # Check 1: Strongly prefer super effective moves
        bot.add_check("super_effective", check_super_effective, priority=3)

        # Check 2: Prefer STAB moves
        bot.add_check("stab", check_stab_bonus, priority=2)

        # Check 3: Avoid not very effective moves
        bot.add_check("avoid_ineffective", check_avoid_ineffective, priority=2)

        # Check 4: Consider base power
        bot.add_check("base_power", check_high_base_power, priority=1)

        # Check 5: Prefer accurate moves
        bot.add_check("accuracy", check_high_accuracy, priority=1)

        # Check 6: Try to inflict status
        bot.add_check("status", check_status_moves, priority=1)

        # You can also add custom inline checks:
        def custom_check(battle, move, target):
            # Example: Prefer moves with "thunder" in the name
            if "thunder" in move.id.lower():
                return 25
            return 0

        bot.add_check("prefer_thunder", custom_check, priority=1)

        # ========================================================================

        # Create opponent (max damage bot for comparison)
        from poke_env.player import MaxBasePowerPlayer
        opponent = MaxBasePowerPlayer(
            battle_format="gen8randombattle",
            server_configuration=LOCAL_SERVER,
        )

        # Uncomment to see scoring details:
        # bot.debug = True

        print("Starting custom strategy bot battles...")
        print(f"Active checks: {[check.name for check in bot.move_checks]}")
        print(f"{bot.username} vs {opponent.username}\n")

        # Battle against the opponent
        n_battles = 5
        await bot.battle_against(opponent, n_battles=n_battles)

        print(f"\n{'='*50}")
        print(f"Results:")
        print(f"{'='*50}")
        print(f"{bot.username}: {bot.n_won_battles} wins / {bot.n_finished_battles} battles")
        print(f"{opponent.username}: {opponent.n_won_battles} wins / {opponent.n_finished_battles} battles")
        print(f"\nBattle data saved to battle_data/custom_strategy_bot.csv")

    asyncio.run(run_custom_bot_vs_opponent())
