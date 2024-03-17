import random
import time
import inspect
import pygame
from enemy_heroes import *


enemy_hero_classes = Hero.__subclasses__()
hero_classes_dict = {name: cls for name, cls in globals().items() if inspect.isclass(cls) and issubclass(cls, Hero)}
card_count = {cls: 0 for cls in hero_classes_dict.values()}


def choose_random_card():
    available_cards = [card_class for card_class in enemy_hero_classes if card_count[card_class] < 2]
    if not available_cards:
        return None
    random_card_class = random.choice(available_cards)
    card_count[random_card_class] += 1
    return random_card_class()

def enemy(info):
    enemy_list = []
    move_points = 2

    heroes_on_fields = [i[2] for i in info]
    while move_points:
        enemy = choose_random_card()
        if heroes_on_fields:
            field = heroes_on_fields.pop(random.randint(0, len(heroes_on_fields)-1))
        else:
            field = random.choice([0, 1, 2, 3])
        if move_points - enemy.cost >= 0:
            move_points -= enemy.cost
            enemy_list.append((enemy, field))

    print('Враг походил')
    return enemy_list