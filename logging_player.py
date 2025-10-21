import csv
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from poke_env.player import Player, RandomPlayer, MaxBasePowerPlayer
from poke_env.battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder


class BattleDataLogger:

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def log_turn_data(self, turn_data: Dict[str, Any]):
        raise NotImplementedError


class CSVBattleLogger(BattleDataLogger):

    def __init__(self, output_path: str):
        super().__init__(output_path)
        self.fieldnames = [
            'timestamp', 'battle_tag', 'turn', 'player_username',
            'active_pokemon', 'active_hp', 'active_max_hp', 'active_hp_fraction',
            'active_status', 'active_atk', 'active_def', 'active_spa', 'active_spd', 'active_spe',
            'opponent_pokemon', 'opponent_hp', 'opponent_max_hp', 'opponent_hp_fraction',
            'opponent_status', 'opponent_atk', 'opponent_def', 'opponent_spa', 'opponent_spd', 'opponent_spe',
            'selected_move', 'selected_move_type', 'selected_move_category',
            'selected_move_base_power', 'selected_move_accuracy',
            'available_moves', 'available_switches',
            'damage_dealt', 'fainted', 'won_battle'
        ]

        if not self.output_path.exists():
            with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def log_turn_data(self, turn_data: Dict[str, Any]):
        with open(self.output_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(turn_data)


class SQLiteBattleLogger(BattleDataLogger):

    def __init__(self, output_path: str):
        super().__init__(output_path)
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.output_path)
        cursor = conn.cursor()


        conn.commit()
        conn.close()

    def log_turn_data(self, turn_data: Dict[str, Any]):
        conn = sqlite3.connect(self.output_path)
        cursor = conn.cursor()

        columns = ', '.join(turn_data.keys())
        placeholders = ', '.join(['?' for _ in turn_data])

        cursor.execute(
            f'INSERT INTO battle_turns ({columns}) VALUES ({placeholders})',
            list(turn_data.values())
        )

        conn.commit()
        conn.close()


class LoggingPlayer(Player):

    def __init__(self, battle_logger: BattleDataLogger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.battle_logger = battle_logger
        self.previous_hp_data: Dict[str, Dict] = {}

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        raise NotImplementedError

    def _extract_turn_data(self, battle: AbstractBattle, selected_move: BattleOrder) -> Dict[str, Any]:
        active = battle.active_pokemon
        opponent = battle.opponent_active_pokemon

        battle_key = battle.battle_tag
        damage_dealt = 0.0
        if battle_key in self.previous_hp_data and opponent:
            prev_hp = self.previous_hp_data[battle_key].get('opponent_hp', opponent.current_hp)
            damage_dealt = prev_hp - opponent.current_hp

        if battle_key not in self.previous_hp_data:
            self.previous_hp_data[battle_key] = {}
        if opponent:
            self.previous_hp_data[battle_key]['opponent_hp'] = opponent.current_hp

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
            'damage_dealt': damage_dealt,
            'fainted': 1 if opponent and opponent.fainted else 0,
            'won_battle': 1 if battle.finished and battle.won else (0 if battle.finished else None)
        }

        return turn_data

    def _log_battle_turn(self, battle: AbstractBattle, selected_move: BattleOrder):
        try:
            turn_data = self._extract_turn_data(battle, selected_move)
            self.battle_logger.log_turn_data(turn_data)
        except Exception as e:
            print(f"Error logging turn data: {e}")


class LoggingRandomPlayer(LoggingPlayer, RandomPlayer):

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        move = self.choose_random_move(battle)
        self._log_battle_turn(battle, move)
        return move


class LoggingMaxDamagePlayer(LoggingPlayer, MaxBasePowerPlayer):

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        move = MaxBasePowerPlayer.choose_move(self, battle)
        self._log_battle_turn(battle, move)
        return move
