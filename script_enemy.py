import random
import time
import inspect
import pygame
from enemy_heroes import *


enemy_hero_classes = [cls() for cls in Hero.__subclasses__()]
hero_count = {}

def enemy(info, occupied_positions):
    hero_instances = [hero_class() for hero_class in Hero.__subclasses__()]
    grade = lambda hero: [hero.damage, hero.hp]

    sorted_heroes = sorted(hero_instances, key=grade, reverse=True)
    moves_left = 2

    result = []
    for position_info in info:
        position, _, _ = position_info
        print(position, '->', [i[0] for i in occupied_positions])
        # Проверяем, занято ли текущее поле
        if position not in [i[0] for i in occupied_positions]:
            for hero in sorted_heroes:
                hero_type = type(hero)
                if hero_count.get(hero_type, 0) < 2 and moves_left >= hero.cost:
                    result.append((position, hero, position_info[2]))
                    hero_count[hero_type] = hero_count.get(hero_type, 0) + 1
                    moves_left -= hero.cost
                    break
    print('Враг походил')
    return result
