import pygame

pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

CARD_SIZE = pygame.Vector2(162, 250)

SPACE_BETWEEN = 45
SPACE_BETWEEN2 = 20
MID_X = SCREEN_WIDTH // 2
MID_Y = SCREEN_HEIGHT // 2
CARD_Y = 530
SELECTED_CARD_Y = 40

MID_Y2 = 300

FONT_TITLE = pygame.font.Font('assets/fonts/SEVESBRG.TTF', 150)
FONT_60 = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 60)
FONT_50 = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 50)
FONT_40 = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 40)
FONT_30 = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 30)
FONT_25 = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 25)
FONT_20 = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 20)

SENSIBLITE_SOURIS = 30