import random
from game.config import PLAYER_NAMES, PLAYER_COLORS, WIN_STABILITY, LOSE_BULLYING
from game.models.player import Player
from game.logic.events_pool import EVENTS, ACTIONS
from game.config import format_effects

class GameState:
    def __init__(self):
        self.players = [Player(name, color) for name, color in zip(PLAYER_NAMES, PLAYER_COLORS)]
        self.current_player_index = 0
        self.turn_number = 1
        self.log = []
        self.current_event = None
        self.game_over = False
        self.winner = None
        self.loser = None
        self.awaiting_action = True
        self.current_event_effects = None
        self.eliminated = []
        self.newly_eliminated = []

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def add_to_log(self, text):
        self.log.append(text)
        if len(self.log) > 5:
            self.log.pop(0)

    def roll_event(self):
        event = random.choice(EVENTS)               # 1. случайное событие из 6
        if random.random() < 0.5:                   # 2. монетка 50/50
            effects = event.effects_1
        else:
            effects = event.effects_2
        self.current_player.apply_effects(effects)  # 3. применяем эффект
        self.current_event = event                  # 4. сохраняем для UI
        self.add_to_log(
            f"{self.current_player.name}: {event.title} — {format_effects(effects)}"
        )
        self.current_event_effects = effects

    def can_do_action(self, action):
        return self.current_player.can_afford(action)

    def do_action(self, action, target_index=None):
        if not self.can_do_action(action):
            return False

        me = self.current_player
        me.apply_effects(action.cost)           # 1. платим
        me.apply_effects(action.self_effects)   # 2. получаем эффект себе

        target = None
        if target_index is not None and target_index != self.current_player_index:
            target = self.players[target_index]
        target.apply_effects(action.target_effects)   # 3. эффект цели

        if target:
            self.add_to_log(f"{me.name}: {action.title} → {target.name}")
        else:
            self.add_to_log(f"{me.name}: {action.title}")

        return True

    def next_turn(self):
        """Переход к следующему игроку. Проверяет выбывших и победителя."""

        self.newly_eliminated = []

        # 1. Помечаем всех, у кого буллинг >= 10, как выбывших
        for p in self.players:
            if p.difficult_teenager and p not in self.eliminated:
                self.eliminated.append(p)
                self.newly_eliminated.append(p)
                self.add_to_log(f"{p.name} выбыл (буллинг >= {LOSE_BULLYING})")

        # 2. Считаем, кто ещё активен
        active_players = [p for p in self.players if p not in self.eliminated]

        # 3. Если остался 1 или 0 активных — конец игры
        if len(active_players) <= 1:
            self.game_over = True
            self.winner = active_players[0] if active_players else None
            if self.winner:
                self.add_to_log(f"{self.winner.name} победил — остался последним!")
            return

        # 4. Проверяем победителя по стабильности
        for p in active_players:
            if p.successful_student:
                self.game_over = True
                self.winner = p
                self.add_to_log(f"{p.name} победил — стабильность >= {WIN_STABILITY}!")
                return

        # 5. Переход к следующему активному игроку
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        while self.players[self.current_player_index] in self.eliminated:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            # защита от бесконечного цикла
            if all(p in self.eliminated for p in self.players):
                break

        if self.current_player_index == 0:
            self.turn_number += 1

        self.current_event = None
        self.current_event_effects = None
