class Player():
    def __init__(self, name, color):
        """
        Создаёт нового ученика со стартовыми ресурсами.

        :param name: имя игрока
        :param color: RGB-кортеж цвета
        """
        self.name = name
        self.color = color
        self.stress = 5
        self.money = 10
        self.friends = 15
        self.homework = 10
        self.bullying = 0

    @property
    def mental_stability(self):
        """
        Ментальная стабильность — главный счёт игрока.
        """
        return self.money * 1.5 + self.friends * 1.5 - self.bullying - self.stress // 2

    @property
    def difficult_teenager(self):
        """
        Проверяет, проиграл ли игрок.
        """
        return self.bullying >= 10

    @property
    def successful_student(self):
        """
        Проверяет, победил ли игрок.
        """
        return self.mental_stability >= 60

    def can_afford(self, action):
        """
        Хватает ли ресурсов, чтобы выполнить действие.

        Проверяет только те ресурсы, у которых cost > 0

        :return: True, если действие можно выполнить
        """
        for item, cost in action.cost.items():
            if cost > 0 and getattr(self, item) < cost:
                return False
        return True

    def apply_effects(self, effects):
        """
        Применяет изменения ресурсов к игроку.
        """
        for item, delta in effects.items():
            setattr(self, item, getattr(self, item) + delta)