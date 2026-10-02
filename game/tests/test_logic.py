from game.logic.events_pool import EVENTS, ACTIONS
from game.models.player import Player
from game.models.action import Action

#стартовые значения

def test_player_initial_values():
    player = Player("Test", "red")

    assert player.stress == 5
    assert player.money == 10
    assert player.friends == 15
    assert player.homework == 10
    assert player.bullying == 0

def test_mental_stability():
    player = Player("Test", "red")

    assert player.mental_stability == 35.5

#трудный подросток :(

def test_difficult_teenager_boundary():
    player = Player("Test", "red")

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
    player = Player("Test", "red")

    # Получаем mental_stability = 59
    player.money = 10
    player.friends = 32
    player.bullying = 2
    player.stress = 4

    assert player.mental_stability == 59
    assert player.successful_student is False

def test_successful_student_at_boundary():
    player = Player("Test", "red")

    # Получаем mental_stability = 60
    player.money = 10
    player.friends = 32
    player.bullying = 0
    player.stress = 6

    assert player.mental_stability == 60
    assert player.successful_student is True

def test_successful_student_above_boundary():
    player = Player("Test", "red")

    # Получаем mental_stability = 61
    player.money = 10
    player.friends = 32
    player.bullying = 0
    player.stress = 4

    assert player.mental_stability == 61
    assert player.successful_student is True

#события

def test_events_count():
    assert len(EVENTS) == 6

def test_event_ids():
    ids = [event.id for event in EVENTS]

    assert ids == ["E1", "E2", "E3", "E4", "E5", "E6"]

def test_events_have_titles():
    for event in EVENTS:
        assert event.title != ""

def test_events_have_two_effect_variants():
    for event in EVENTS:
        assert isinstance(event.effects_1, dict)
        assert isinstance(event.effects_2, dict)

#действия

def test_actions_count():
    assert len(ACTIONS) == 5

def test_action_ids():
    ids = [action.id for action in ACTIONS]

    assert ids == ["A1", "A2", "A3", "A4", "A5"]

def test_actions_have_titles():
    for action in ACTIONS:
        assert action.title != ""

def test_actions_have_cost():
    for action in ACTIONS:
        assert isinstance(action.cost, dict)

def test_actions_have_effects():
    for action in ACTIONS:
        assert isinstance(action.self_effects, dict)
        assert isinstance(action.target_effects, dict)

#проверка каждого действия

def test_action_a1():
    action = ACTIONS[0]

    assert action.id == "A1"
    assert action.title == "Сделать домашку с другом"

    assert action.cost == {"homework": 3}
    assert action.self_effects == {"friends": 3, "stress": -3}
    assert action.target_effects == {"homework": 3, "stress": -1}

def test_action_a2():
    action = ACTIONS[1]

    assert action.id == "A2"
    assert action.title == "Сбежать с последнего урока вместе"

    assert action.cost == {"homework": 3}
    assert action.self_effects == {"bullying": -4, "stress": 2}
    assert action.target_effects == {"stress": 4, "homework": -5}

def test_action_a3():
    action = ACTIONS[2]

    assert action.id == "A3"
    assert action.title == "Списать у одноклассника"

    assert action.cost == {"stress": 4}
    assert action.self_effects == {"friends": 4, "money": -1}
    assert action.target_effects == {"money": 1, "bullying": 2}

def test_action_a4():
    action = ACTIONS[3]

    assert action.id == "A4"
    assert action.title == "Рассказать слух"

    assert action.cost == {"friends": 1}
    assert action.self_effects == {"bullying": -3}
    assert action.target_effects == {"bullying": 4}

def test_action_a5():
    action = ACTIONS[4]

    assert action.id == "A5"
    assert action.title == "Подставить"

    assert action.cost == {"friends": 2}
    assert action.self_effects == {
        "stress": -3,
        "bullying": -2,
        "money": 3,
    }
    assert action.target_effects == {
        "bullying": 4,
        "stress": 3,
    }

def test_can_afford():
    """
    провряет функцию can_afford игнорируя неположительные значения
    """
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
    player = Player("Test", "red")
    player.apply_effects({
        "money": 3,
        "friends": -2,
        "stress": 1
    })

    assert player.money == 13
    assert player.friends == 13
    assert player.stress == 6