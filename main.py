import inspect
import sys
import pygame
import random
from heroes import *
from script_enemy import enemy


pygame.init()


size = width, height = 1400, 1020
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Карточные войны")
background_image = pygame.image.load("images/card_wars/деревянный_стол_фон.png").convert()
background_image = pygame.transform.scale(background_image, (width, height))


move_points = 2
count_player_cards = 5
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)


num_rectangles = 4
horizontal_gap = 20
vertical_gap = 20

# Рассчет ширины и высоты прямоугольников
rect_width = (width - (num_rectangles + 1) * horizontal_gap) // num_rectangles - 70
rect_height = (height - 3 * vertical_gap) // 2 - 160

# Загрузка изображений
corn_fields = pygame.image.load("images/card_wars/кукурузные_поля.jpg")
corn_fields = pygame.transform.scale(corn_fields, (rect_width, rect_height))
corn_fields = pygame.transform.rotate(corn_fields, 180)

blue_plain = pygame.image.load("images/card_wars/синяя_равнина.png")
blue_plain = pygame.transform.scale(blue_plain, (rect_width, rect_height))
blue_plain = pygame.transform.rotate(blue_plain, 180)

top_space = vertical_gap
bottom_space = height - (2 * vertical_gap + 2 * rect_height)

player_cards_width = (width - (num_rectangles + 1) * horizontal_gap) // 6
player_cards_height = rect_width

center_offset_x = (rect_width - player_cards_width) // 2
center_offset_y = (rect_height - player_cards_height) // 2


shirt_card = pygame.image.load("images/card_wars/рубашка_карты.jpg")
shirt_card = pygame.transform.scale(shirt_card, (player_cards_width, player_cards_height))
shirt_card_rect = pygame.Rect(width - rect_width, 400, rect_width, rect_height)


button_width = 150
button_height = 40
button_x = width - button_width - 20
button_y = height - button_height - 20
button_color = (0, 128, 0)
end_move_button_color = (255, 255, 255)
button_font = pygame.font.Font(None, 24)
button_text = button_font.render("Завершить ход", True, end_move_button_color)
end_move = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))


count_corn_fields = 4


def is_clicked(rect, pos):
    return rect.collidepoint(pos)


# Создание прямоугольников и их координат
additional_rectangles = []
for i in range(5):
    x = horizontal_gap + i * (player_cards_width + horizontal_gap)
    y = height - vertical_gap - player_cards_height
    rect = pygame.Rect(x, y, player_cards_width, player_cards_height)
    additional_rectangles.append(rect)


selected_rectangle = None
moved_additional_rectangles = {}
occupied_lower_rects = set()


hero_classes = Hero.__subclasses__()

class HeroCard:
    def __init__(self, hero_class):
        self.hero = hero_class()
        self.icon = self.hero.icon



additional_rectangles_info = []

hero_classes_dict = {name: cls for name, cls in globals().items() if inspect.isclass(cls) and issubclass(cls, Hero)}
card_count = {cls: 0 for cls in hero_classes_dict.values()}


def choose_random_card():
    available_cards = [card_class for card_class in hero_classes if card_count[card_class] < 2]
    if not available_cards:
        return None
    random_card_class = random.choice(available_cards)
    card_count[random_card_class] += 1
    return random_card_class


for i, coords in enumerate(additional_rectangles):
    random_hero_class = choose_random_card()
    if not random_hero_class:
        break
    additional_rect = HeroCard(random_hero_class)
    additional_rectangles_info.append(additional_rect)


move_points_text_color = (255, 255, 255)
last_color_change_time = 0
font = pygame.font.Font(None, 36)

player_move = True


cards_on_field = []

def add_card():
    global count_player_cards
    global additional_rectangles

    count_player_cards += 1
    count_cards = len(additional_rectangles)
    additional_rectangles = []
    for i in range(count_cards + 1):
        x = horizontal_gap + i * (player_cards_width + horizontal_gap)
        y = height - vertical_gap - player_cards_height
        rect = pygame.Rect(x, y, player_cards_width, player_cards_height)
        additional_rectangles.append(rect)

    additional_rectangles_info.append(HeroCard(choose_random_card()))



def draw_fields():
    for i in range(num_rectangles):
        x = horizontal_gap + i * (rect_width + horizontal_gap)
        y = top_space
        screen.blit(blue_plain, (x, y))

    for i in range(num_rectangles):
        x = horizontal_gap + i * (rect_width + horizontal_gap)
        y = height - bottom_space - rect_height
        screen.blit(corn_fields, (x, y))


def draw_widgets():
    global move_points_text_color

    move_points_text = font.render(f"Move Points: {move_points}", True, move_points_text_color)
    move_points_text_rect = move_points_text.get_rect()
    move_points_text_rect.topright = (width - 10, 10)
    screen.blit(move_points_text, move_points_text_rect)

    move_text = font.render(f"Move: {'you' if player_move else 'enemy'}", True, text_color)
    move_text_rect = move_text.get_rect()
    move_text_rect.topright = (width - 10, 30)
    screen.blit(move_text, move_text_rect)

    screen.blit(shirt_card, (width - rect_width, 400))

    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    screen.blit(button_text, end_move)

    if current_time - last_color_change_time > 500:
        move_points_text_color = (255, 255, 255)


def draw_cards():
    c = 0
    for i, _ in enumerate(additional_rectangles):
        if i not in moved_additional_rectangles:
            card = pygame.transform.scale(additional_rectangles_info[i].icon, (player_cards_width, player_cards_height))
            # Рисуем урон и ХП на карте
            draw_text_on_card(card, additional_rectangles_info[i].hero.damage, (8, card.get_height() - 28))
            draw_text_on_card(card, additional_rectangles_info[i].hero.hp, (card.get_width() - 25, card.get_height() - 25))
            x = horizontal_gap + c * (player_cards_width + horizontal_gap)
            y = height - vertical_gap - player_cards_height
            rect = pygame.Rect(x, y, player_cards_width, player_cards_height)
            additional_rectangles[i] = rect
            screen.blit(card, rect)
            c += 1
            if selected_rectangle == i:
                pygame.draw.rect(screen, (167, 252, 0), rect, 3)


def draw_cards_on_fields():
    for i, info, _ in cards_on_field:
        card = pygame.transform.scale(info.hero.icon, (player_cards_width, player_cards_height))
        # Рисуем урон и ХП на карте
        draw_text_on_card(card, info.hero.damage, (8, card.get_height() - 28))
        draw_text_on_card(card, info.hero.hp, (card.get_width() - 25, card.get_height() - 25))
        screen.blit(card, i)


def draw_text_on_card(image, text, position, font_size=36, text_color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(str(text), True, text_color)
    image.blit(text_surface, position)


running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            mouse_x, mouse_y = event.pos

            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                player_move = False

            if player_move:
                if shirt_card_rect.collidepoint(event.pos) and count_player_cards < 5:
                    if move_points >= 1:
                        move_points -= 1
                        add_card()
                        print("Вы взяли карту")

                    else:
                        move_points_text_color = (255, 0, 0)
                        last_color_change_time = current_time
                else:
                    print(count_player_cards)


                # Проверяем, был ли клик на одном из дополнительных прямоугольников
                for i, rect in enumerate(additional_rectangles):
                    if is_clicked(rect, pos):
                        # Добавляем проверку, чтобы позволить сменить выбор, если другой дополнительный прямоугольник не был перемещен
                        if i not in moved_additional_rectangles or (
                                selected_rectangle is not None and i == selected_rectangle):
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
                            if selected_rectangle is not None:
                                card_info = additional_rectangles_info[selected_rectangle]
                                card_cost = card_info.hero.cost
                                if move_points >= card_cost:
                                    new_x = x + center_offset_x
                                    new_y = y + center_offset_y
                                    moved_additional_rectangles[selected_rectangle] = (new_x, new_y)
                                    occupied_lower_rects.add(i)
                                    move_points -= card_cost
                                    cards_on_field.append(((new_x, new_y), card_info, i))
                                    count_player_cards -= 1

                                    print(
                                        f"Дополнительный прямоугольник {selected_rectangle + 1} перемещен в центр прямоугольника {i + 1}.")
                                else:
                                    move_points_text_color = (255, 0, 0)
                                    last_color_change_time = current_time
                                selected_rectangle = None
                            break
            else:
                print(enemy(cards_on_field))
                player_move = True
                move_points = 2

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    draw_widgets()
    draw_fields()
    draw_cards()
    draw_cards_on_fields()

    pygame.display.flip()

pygame.quit()
sys.exit()
