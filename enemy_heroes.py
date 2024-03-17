import pygame

class Hero:
    def __init__(self, hp, damage, cost, icon):
        self.hp = hp
        self.damage = damage
        self.icon = pygame.image.load(icon)
        self.cost = cost

class Warrior(Hero):
    def __init__(self):
        super().__init__(hp=5, damage=1, cost=0, icon="images/card_wars/heroes/Лихо_одоглазое.jpg")

class Mage(Hero):
    def __init__(self):
        super().__init__(hp=6, damage=1, cost=1, icon="images/card_wars/heroes/Кукурузный_ронин.jpg")

class Archer(Hero):
    def __init__(self):
        super().__init__(hp=0, damage=0, cost=2, icon="images/card_wars/heroes/Кожурыцарь.jpg")

class Archers(Hero):
    def __init__(self):
        super().__init__(hp=7, damage=0, cost=1, icon="images/card_wars/heroes/Царь_полей.jpg")
