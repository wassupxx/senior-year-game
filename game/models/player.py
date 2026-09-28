class Player():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stress = 5
        self.money = 10
        self.friends = 15
        self.homework = 10
        self.bullying = 0

    @property
    def mental_stability(self):
        return self.money * 1.5 + self.friends * 1.5 - self.bullying - self.stress // 2

    @property
    def difficult_teenager(self):
        return self.bullying >= 10

    @property
    def successful_student(self):
        return self.mental_stability >= 60


