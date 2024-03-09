import pygame

class Hero:
    def __init__(self, hp, damage, cost, icon):
        self.hp = hp
        self.damage = damage
        self.icon = pygame.image.load(icon)
        self.cost = cost

class Warrior(Hero):
    def __init__(self):
        super().__init__(hp=100, damage=15, cost=2, icon="images/card_wars/деревянный_стол_фон.png")

class Mage(Hero):
    def __init__(self):
        super().__init__(hp=80, damage=25, cost=0, icon="images/card_wars/рубашка_карты.jpg")

class Archer(Hero):
    def __init__(self):
        super().__init__(hp=90, damage=20, cost=1, icon="images/card_wars/синяя_равнина.png")

class Archers(Hero):
    def __init__(self):
        super().__init__(hp=900, damage=0, cost=1, icon="images/card_wars/синяя_равнина.png")
