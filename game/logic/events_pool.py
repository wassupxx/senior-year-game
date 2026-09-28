from game.models.event import RandomEvent
from game.models.action import Action

EVENTS = [
    RandomEvent(
        "E1", "Обед",
        {"stress": -3, "money": -5},
        {"money": -3, "homework": 2},
    ),
    RandomEvent(
        "E2", "Контрольная",
        {"homework": 3, "stress": -1},
        {"stress": 3, "bullying": 4},
    ),
    RandomEvent(
        "E3", "Прогул",
        {"friends": 5, "bullying": -2},
        {"stress": 3, "bullying": 4},
    ),
    RandomEvent(
        "E4", "Опоздание",
        {"friends": 2},
        {"bullying": 5},
    ),
    RandomEvent(
        "E5", "Встреча с параллелью",
        {"friends": 3},
        {"bullying": 4},
    ),
    RandomEvent(
        "E6", "Перемена",
        {"homework": 3, "stress": -2},
        {"money": -5, "bullying": 3},
    )
]

ACTIONS = [
    Action(
        "A1", "Сделать домашку с другом",
        cost={"homework": 3},
        self_effects={"friends": 3, "stress": -3},
        target_effects={"homework": 3, "stress": -1},
        description="−3 домашка. Тебе +3 друзья, −3 стресс. Ему +3 домашка, −1 стресс.",
    ),
    Action(
        "A2", "Сбежать с последнего урока вместе",
        cost={"homework": 3},
        self_effects={"bullying": -4, "stress": 2},
        target_effects={"stress": 4, "homework": -5},
        description="−3 домашка. Тебе −4 буллинг, +2 стресс. Ему +4 стресс, −5 домашка.",
    ),
    Action(
        "A3", "Списать у одноклассника",
        cost={"stress": 4},
        self_effects={"friends": 4, "money": -1},
        target_effects={"money": 1, "bullying": 2},
        description="+4 стресс. Тебе +4 друзья, −1 деньги. Ему +1 деньги, +2 буллинг.",
    ),
    Action(
        "A4", "Рассказать слух",
        cost={"friends": 1},
        self_effects={"bullying": -3},
        target_effects={"bullying": 4},
        description="−1 друзья. Тебе −3 буллинг. Ему +4 буллинг.",
    ),
    Action(
        "A5", "Подставить",
        cost={"friends": 2},
        self_effects={"stress": -3, "bullying": -2, "money": 3},
        target_effects={"bullying": 4, "stress": 3},
        description="−2 друзья. Тебе −3 стресс, −2 буллинг, +3 деньги. Ему +4 буллинг, +3 стресс.",
    ),
]
