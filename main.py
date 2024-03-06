import sys
import pygame

# Инициализация Pygame
pygame.init()

# Установка размеров окна
size = width, height = 1260, 1020
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Карточные войны")
background_image = pygame.image.load("images/card_wars/деревянный_стол_фон.png").convert()
background_image = pygame.transform.scale(background_image, (width, height))


num_rectangles = 4
horizontal_gap = 20
vertical_gap = 20

# Загрузка изображения

# Рассчет ширины и высоты прямоугольников
rect_width = (width - (num_rectangles + 1) * horizontal_gap) // num_rectangles
rect_height = (height - 3 * vertical_gap) // 2 - 160


corn_fields = pygame.image.load("images/card_wars/кукурузные_поля.jpg")
corn_fields = pygame.transform.scale(corn_fields, (rect_width, rect_height))

blue_plain = pygame.image.load("images/card_wars/синяя_равнина.png")
blue_plain = pygame.transform.scale(blue_plain, (rect_width, rect_height))

top_space = vertical_gap
bottom_space = height - (2 * vertical_gap + 2 * rect_height)

additional_rect_width = (width - (num_rectangles + 1) * horizontal_gap) // 6 - 7
additional_rect_height = (height - 5 * vertical_gap) // 3

# Загрузка изображений для дополнительных прямоугольников
additional_image = pygame.image.load("images/card_wars/рубашка_карты.jpg")
additional_image = pygame.transform.scale(additional_image, (additional_rect_width, additional_rect_height))


# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    # Рисуем верхний ряд прямоугольников с верхним изображением
    for i in range(num_rectangles):
        x = horizontal_gap + i * (rect_width + horizontal_gap)
        y = top_space
        screen.blit(corn_fields, (x, y))

    # Рисуем нижний ряд прямоугольников с нижним изображением
    for i in range(num_rectangles):
        x = horizontal_gap + i * (rect_width + horizontal_gap)
        y = height - bottom_space - rect_height
        screen.blit(blue_plain, (x, y))

    for i in range(6):
        x = horizontal_gap + i * (additional_rect_width + horizontal_gap)
        y = height - vertical_gap - additional_rect_height
        screen.blit(additional_image, (x, y))

    pygame.display.flip()

pygame.quit()
sys.exit()