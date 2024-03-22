import random
import time
import inspect
import pygame
from enemy_heroes import *


enemy_hero_classes = [cls() for cls in Hero.__subclasses__()]
hero_count = {}

def enemy(info, occupied_positions, total_positions=4):
    hero_instances = [hero_class() for hero_class in Hero.__subclasses__()]
    grade = lambda hero: [hero.damage, hero.hp]

    sorted_heroes = sorted(hero_instances, key=grade, reverse=True)
    moves_left = 2

    # Создаем список занятых позиций
    occupied = [pos[2] for pos in occupied_positions]  # Изменено на использование индекса позиции

    result = []
    # Проходим по всем позициям на поле
    for position in range(total_positions):
        # Проверяем, свободна ли текущая позиция
        if position not in occupied:
            for hero in sorted_heroes:
                hero_type = type(hero)
                if hero_count.get(hero_type, 0) < 2 and moves_left >= hero.cost:
                    result.append((position, hero, position))  # Используем position в качестве индекса позиции
                    hero_count[hero_type] = hero_count.get(hero_type, 0) + 1
                    moves_left -= hero.cost
                    occupied.append(position)  # Добавляем позицию в список занятых
                    break
    print('Враг походил')
    return result

