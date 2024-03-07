class Hero:
    def __init__(self, hp, damage, icon):
        self.hp = hp
        self.damage = damage
        self.icon = icon

class Warrior(Hero):
    def __init__(self):
        super().__init__(hp=100, damage=15, icon="images/card_wars/деревянный_стол_фон.png")

class Mage(Hero):
    def __init__(self):
        super().__init__(hp=80, damage=25, icon="images/card_wars/рубашка_карты.jpg")

class Archer(Hero):
    def __init__(self):
        super().__init__(hp=90, damage=20, icon="images/card_wars/синяя_равнина.png")
