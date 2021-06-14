class Shield:

    def __init__(self, name, chance=3, plus=1): #constructor
        self.name = name
        self.chance = chance
        self.plus = plus

    def __repr__(self):
        return self.name
    def __str__(self):
        return str(self.name)