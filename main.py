import sys
import pygame
import random
from heroes import Hero, Warrior, Mage, Archer


pygame.init()


size = width, height = 1260, 1020
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Карточные войны")
background_image = pygame.image.load("images/card_wars/деревянный_стол_фон.png").convert()
background_image = pygame.transform.scale(background_image, (width, height))

num_rectangles = 4
horizontal_gap = 20
vertical_gap = 20

# Рассчет ширины и высоты прямоугольников
rect_width = (width - (num_rectangles + 1) * horizontal_gap) // num_rectangles
rect_height = (height - 3 * vertical_gap) // 2 - 160

# Загрузка изображений
corn_fields = pygame.image.load("images/card_wars/кукурузные_поля.jpg")
corn_fields = pygame.transform.scale(corn_fields, (rect_width, rect_height))

blue_plain = pygame.image.load("images/card_wars/синяя_равнина.png")
blue_plain = pygame.transform.scale(blue_plain, (rect_width, rect_height))

top_space = vertical_gap
bottom_space = height - (2 * vertical_gap + 2 * rect_height)

additional_rect_width = (width - (num_rectangles + 1) * horizontal_gap) // 6 - 7
additional_rect_height = rect_width - 50

center_offset_x = (rect_width - additional_rect_width) // 2
center_offset_y = (rect_height - additional_rect_height) // 2

def is_clicked(rect, pos):
    return rect.collidepoint(pos)

# Создание прямоугольников и их координат
additional_rectangles = []
for i in range(6):
    x = horizontal_gap + i * (additional_rect_width + horizontal_gap)
    y = height - vertical_gap - additional_rect_height
    rect = pygame.Rect(x, y, additional_rect_width, additional_rect_height)
    additional_rectangles.append(rect)


selected_rectangle = None
moved_additional_rectangles = {}
occupied_lower_rects = set()


hero_classes = Hero.__subclasses__()

class HeroCard:
    def __init__(self, hero_class, x, y):
        self.hero = hero_class()
        self.icon = self.hero.icon
        self.rect = pygame.Rect(x, y, additional_rect_width, additional_rect_height)


initial_additional_rect_coordinates = [(rect.x, rect.y) for rect in additional_rectangles]
additional_rectangles_info = []
for i, coords in enumerate(initial_additional_rect_coordinates):
    random_hero_class = random.choice(hero_classes)
    additional_rect = HeroCard(random_hero_class, coords[0], coords[1])
    additional_rectangles_info.append(additional_rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Проверяем, был ли клик на одном из дополнительных прямоугольников
            for i, rect in enumerate(additional_rectangles):
                if is_clicked(rect, pos):
                    # Добавляем проверку, чтобы позволить сменить выбор, если другой дополнительный прямоугольник не был перемещен
                    if i not in moved_additional_rectangles or (selected_rectangle is not None and i == selected_rectangle):
                        selected_rectangle = i
                        print(f"Дополнительный прямоугольник {i + 1} выбран.")
                        break

            # Проверяем, был ли клик на одном из нижних прямоугольников для перемещения выбранного дополнительного прямоугольника
            if selected_rectangle is not None:
                for i in range(num_rectangles):
                    x = horizontal_gap + i * (rect_width + horizontal_gap)
                    y = height - bottom_space - rect_height
                    rect = pygame.Rect(x, y, rect_width, rect_height)
                    if is_clicked(rect, pos) and i not in occupied_lower_rects:
                        # Расчет новых координат для центрирования дополнительного прямоугольника внутри нижнего
                        new_x = x + center_offset_x
                        new_y = y + center_offset_y
                        moved_additional_rectangles[selected_rectangle] = (new_x, new_y)
                        occupied_lower_rects.add(i)
                        print(
                            f"Дополнительный прямоугольник {selected_rectangle + 1} перемещен в центр прямоугольника {i + 1}.")
                        selected_rectangle = None  # Сбрасываем выбор после перемещения
                        break

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))


    for i in range(num_rectangles):
        x = horizontal_gap + i * (rect_width + horizontal_gap)
        y = top_space
        screen.blit(corn_fields, (x, y))

    for i in range(num_rectangles):
        x = horizontal_gap + i * (rect_width + horizontal_gap)
        y = height - bottom_space - rect_height
        screen.blit(blue_plain, (x, y))

    for i, rect in enumerate(additional_rectangles):
        if i in moved_additional_rectangles:
            card = pygame.image.load(additional_rectangles_info[i].icon)
            card = pygame.transform.scale(card, (additional_rect_width, additional_rect_height))
            screen.blit(card, moved_additional_rectangles[i])
        else:
            card = pygame.image.load(additional_rectangles_info[i].icon)
            card = pygame.transform.scale(card, (additional_rect_width, additional_rect_height))
            screen.blit(card, rect)
            if selected_rectangle == i:
                pygame.draw.rect(screen, (167, 252, 0), rect, 3)

    pygame.display.flip()

pygame.quit()
sys.exit()
