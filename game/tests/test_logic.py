import pytest

from game.models.player import Player
from game.models.action import Action
from game.models.event import RandomEvent
from game.logic.events_pool import EVENTS, ACTIONS
from game.logic.game_state import GameState

#стартовые значения

def test_player_initial_values():
    """Проверяет стартовые значения нового игрока"""
    player = Player("Test", "red")

    assert player.stress == 5
    assert player.money == 10
    assert player.friends == 15
    assert player.homework == 10
    assert player.bullying == 0

    assert player.mental_stability == 35.5

#трудный подросток :(

def test_difficult_teenager_boundary():
    """проверка граничных значений буллинга"""
    player = Player("Test", "red")

    assert player.bullying == 0
    assert player.difficult_teenager is False

    player.apply_effects({"bullying": 9})
    assert player.bullying == 9
    assert player.difficult_teenager is False

    player.apply_effects({"bullying": 1})
    assert player.bullying == 10
    assert player.difficult_teenager is True

    player.apply_effects({"bullying": 1})
    assert player.bullying == 11
    assert player.difficult_teenager is True

#успешный ученик :)

def test_successful_student_below_boundary():
    """При стабильности < 60 игрок ещё не победил"""
    player = Player("Test", "red")

    # Получаем mental_stability = 59
    player.money = 10
    player.friends = 32
    player.bullying = 2
    player.stress = 4

    assert player.mental_stability == 59
    assert player.successful_student is False

def test_successful_student_at_boundary():
    """При стабильности >= 60 игрок побеждает"""
    player = Player("Test", "red")

    # Получаем mental_stability = 60
    player.money = 10
    player.friends = 32
    player.bullying = 0
    player.stress = 6

    assert player.mental_stability == 60
    assert player.successful_student is True

    player.stress -= 2
    assert player.mental_stability == 61
    assert player.successful_student is True

#события

def test_events_count():
    """Проверяет наличие событий E1-E6."""
    assert len(EVENTS) == 6

    ids = {event.id for event in EVENTS}
    assert ids == {"E1", "E2", "E3", "E4", "E5", "E6"}

def test_events_have_required_fields():
    """Каждое событие должно иметь id, title и два варианта эффектов"""
    for event in EVENTS:
        assert event.id
        assert event.title
        assert isinstance(event.effects_1, dict)
        assert isinstance(event.effects_2, dict)

#действия

def test_actions_count():
    """Проверяет наличие действий A1-A5"""
    assert len(ACTIONS) == 5

    ids = {action.id for action in ACTIONS}
    assert ids == {"A1", "A2", "A3", "A4", "A5"}

def test_actions_have_required_fields():
    """Каждое действие должно иметь основные поля"""
    for action in ACTIONS:
        assert action.id
        assert action.title
        assert isinstance(action.cost, dict)
        assert isinstance(action.self_effects, dict)
        assert isinstance(action.target_effects, dict)
        assert isinstance(action.description, str)

def test_can_afford():
    """провряет функцию can_afford игнорируя неположительные значения"""
    player = Player("Test", "red")
    action = Action(
        "A",
        "Test action",
        {"money": 5, "friends": 0, "stress": -2},
        {},
        {},
        ""
    )
    player.money = 10
    player.friends = -1
    player.stress = 0
    assert player.can_afford(action) is True

    player.money = 4
    assert player.can_afford(action) is False

def test_apply_multiple_effects():
    """проверяет применение эффектов к ресурсам игрока"""
    player = Player("Test", "red")
    player.apply_effects({
        "money": 3,
        "friends": -2,
        "stress": 1
    })

    assert player.money == 13
    assert player.friends == 13
    assert player.stress == 6

#ход игры

def test_game_state_initialization():
    """Проверяет начальное состояние игры"""
    gs = GameState()

    assert len(gs.players) == 4
    assert gs.current_player_index == 0
    assert gs.turn_number == 1
    assert gs.current_event is None
    assert gs.game_over is False
    assert gs.winner is None
    assert gs.loser is None
    assert gs.awaiting_action is True
    assert gs.current_event_effects is None

def test_current_player():
    """current_player должен соответствовать current_player_index"""
    gs = GameState()

    assert gs.current_player == gs.players[0]

    gs.current_player_index = 1

    assert gs.current_player == gs.players[1]

def test_add_to_log():
    """Новые записи должны добавляться в лог"""
    gs = GameState()
    gs.add_to_log("Первое событие")

    assert gs.log[-1] == "Первое событие"

def test_log_contains_max_five_items():
    """в логе должно оставаться максимум 5 последних записей"""
    gs = GameState()
    for i in range(7):
        gs.add_to_log(f"Запись {i}")

    assert len(gs.log) == 5
    assert gs.log == [
        "Запись 2",
        "Запись 3",
        "Запись 4",
        "Запись 5",
        "Запись 6",
    ]

def test_roll_event_uses_first_effect(monkeypatch):
    """roll_event должен выбрать одно событие,при random < 0.5 используется effects_1"""
    gs = GameState()
    selected_event = EVENTS[0]

    monkeypatch.setattr(
        "game.logic.game_state.random.choice",
        lambda events: selected_event
    )

    monkeypatch.setattr(
        "game.logic.game_state.random.random",
        lambda: 0.1
    )

    gs.roll_event()

    assert gs.current_event == selected_event
    assert gs.current_event_effects == selected_event.effects_1

def test_roll_event_uses_second_effect(monkeypatch):
    """при random >= 0.5 используется effects_2"""
    gs = GameState()
    selected_event = EVENTS[0]

    monkeypatch.setattr(
        "game.logic.game_state.random.choice",
        lambda events: selected_event
    )

    monkeypatch.setattr(
        "game.logic.game_state.random.random",
        lambda: 0.9
    )

    gs.roll_event()

    assert gs.current_event_effects == selected_event.effects_2

def test_roll_event_changes_player_resources(monkeypatch):
    """roll_event должен применять выбранный эффект к текущему игроку"""
    gs = GameState()
    selected_event = RandomEvent(
        "TEST",
        "Тестовое событие",
        {"money": 5},
        {"money": -5},
    )

    monkeypatch.setattr(
        "game.logic.game_state.random.choice",
        lambda events: selected_event
    )

    monkeypatch.setattr(
        "game.logic.game_state.random.random",
        lambda: 0.1
    )

    old_money = gs.current_player.money
    gs.roll_event()

    assert gs.current_player.money == old_money + 5

def test_roll_event_adds_to_log(monkeypatch):
    """после события оно должно попасть в лог"""
    gs = GameState()
    selected_event = EVENTS[0]

    monkeypatch.setattr(
        "game.logic.game_state.random.choice",
        lambda events: selected_event
    )

    monkeypatch.setattr(
        "game.logic.game_state.random.random",
        lambda: 0.1
    )

    gs.roll_event()

    assert len(gs.log) == 1
    assert selected_event.title in gs.log[0]

def test_can_do_action_when_affordable():
    """can_do_action возвращает True, если действие доступно"""
    gs = GameState()
    action = ACTIONS[0]

    assert gs.can_do_action(action) is True

def test_can_do_action_when_not_affordable():
    """can_do_action возвращает False, если ресурсов недостаточно"""
    gs = GameState()
    action = Action(
        "TEST",
        "Expensive action",
        {"money": 999},
        {},
        {},
    )

    assert gs.can_do_action(action) is False

def test_do_action_without_target():
    """действие без цели должно применяться к текущему игроку"""
    gs = GameState()
    action = Action(
        "TEST",
        "Test action",
        {"money": 2},
        {"friends": 3},
        {},
    )

    player = gs.current_player
    old_money = player.money
    old_friends = player.friends

    result = gs.do_action(action)

    assert result
    assert player.money == old_money - 2
    assert player.friends == old_friends + 3

def test_do_action_with_target():
    """действие с целью должно применить эффекты к двум игрокам"""
    gs = GameState()
    action = Action(
        "TEST",
        "Test action",
        {"money": 2},
        {"stress": -1},
        {"bullying": 3},
    )

    player = gs.current_player
    target = gs.players[1]

    old_money = player.money
    old_stress = player.stress
    old_bullying = target.bullying

    result = gs.do_action(action, target_index=1)

    assert result
    assert player.money == old_money - 2
    assert player.stress == old_stress - 1
    assert target.bullying == old_bullying + 3

def test_do_action_fails_without_resources():
    """недоступное действие не должно выполняться"""
    gs = GameState()
    action = Action(
        "TEST",
        "Too expensive",
        {"money": 999},
        {"friends": 10},
        {},
    )

    player = gs.current_player
    old_friends = player.friends

    result = gs.do_action(action)

    assert result is False
    assert player.friends == old_friends

def test_next_turn_changes_player():
    """после хода должен стать текущим следующий игрок"""
    gs = GameState()

    assert gs.current_player_index == 0

    gs.next_turn()

    assert gs.current_player_index == 1

def test_next_turn_wraps_to_first_player():
    """после последнего игрока ход возвращается к первому"""
    gs = GameState()
    gs.current_player_index = len(gs.players) - 1
    gs.turn_number = 3

    gs.next_turn()

    assert gs.current_player_index == 0

def test_next_turn_increases_turn_number():
    """Номер хода должен увеличиваться после полного круга игроков."""
    gs = GameState()
    gs.current_player_index = len(gs.players) - 1
    old_turn = gs.turn_number

    gs.next_turn()

    assert gs.turn_number == old_turn + 1

def test_next_turn_clears_current_event():
    """после перехода хода текущее событие должно сбрасываться"""
    gs = GameState()
    gs.current_event = EVENTS[0]
    gs.current_event_effects = EVENTS[0].effects_1

    gs.next_turn()

    assert gs.current_event is None
    assert gs.current_event_effects is None

#конец игры

def test_player_with_bullying_10_loses():
    """игрок с bullying >= 10 должен проиграть на следующем ходу"""
    gs = GameState()
    loser = gs.players[0]
    loser.bullying = 10

    gs.next_turn()

    assert gs.game_over is False
    assert loser.difficult_teenager is True
    assert loser in gs.eliminated
    assert gs.winner is None

def test_player_with_bullying_above_10_loses():
    """игрок с bullying > 10 также должен проиграть"""
    gs = GameState()
    loser = gs.players[0]
    loser.bullying = 15

    gs.next_turn()

    assert gs.game_over is False
    assert loser.difficult_teenager is True
    assert loser in gs.eliminated

def test_player_with_bullying_9_does_not_lose():
    """при bullying = 9 игрок ещё не проиграл"""
    gs = GameState()

    player = gs.players[0]
    player.bullying = 9

    gs.next_turn()

    assert gs.game_over is False
    assert player.difficult_teenager is False
    assert player not in gs.eliminated

def test_successful_student_wins():
    """игрок со стабильностью >= 60 должен победить"""
    gs = GameState()
    winner = gs.players[0]
    winner.money = 30
    winner.friends = 30
    winner.bullying = 0
    winner.stress = 0

    gs.next_turn()

    assert gs.game_over is True
    assert gs.winner == winner
    assert gs.loser is None

def test_successful_student_at_stability_60():
    """проверка победы при стабильности ровно 60"""
    gs = GameState()
    winner = gs.players[0]

    winner.money = 20
    winner.friends = 20
    winner.bullying = 0
    winner.stress = 0

    assert winner.mental_stability == 60

    gs.next_turn()

    assert gs.game_over is True
    assert gs.winner == winner

def test_stability_below_60_does_not_win():
    """при стабильности < 60 игрок ещё не победил"""
    gs = GameState()
    player = gs.players[0]

    player.money = 20
    player.friends = 19
    player.bullying = 0
    player.stress = 0

    assert player.mental_stability == 58.5

    gs.next_turn()

    assert gs.game_over is False
    assert gs.winner is None

def test_game_over_stops_further_turn_processing():
    """после окончания игры next_turn не должен продолжать игру"""
    gs = GameState()
    winner = gs.players[0]

    winner.money = 20
    winner.friends = 20
    winner.bullying = 0
    winner.stress = 0

    gs.next_turn()

    assert gs.game_over is True

    current_index = gs.current_player_index
    current_turn = gs.turn_number

    gs.next_turn()

    assert gs.current_player_index == current_index
    assert gs.turn_number == current_turn