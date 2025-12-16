import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
# beige = red, black= white

LIGHT_SQUARE = (245, 245, 220)
DARK_SQUARE = (101, 67, 33)

PLAYER_1_BEIGE = (0, 0, 0)
PLAYER_2_BLACK = (222, 184, 135)
BEIGE = (238, 238, 210)

BLUE = (135, 206, 250)

CROWN = pygame.transform.scale(pygame.image.load('checkers\crown.png'), (44, 25))