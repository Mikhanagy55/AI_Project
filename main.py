import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, PLAYER_1_BEIGE, PLAYER_2_BLACK
from checkers.game import Game
from checkers.ai import Checkers

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        # Let AI play as PLAYER_2_BLACK
        if game.turn == PLAYER_2_BLACK:
            best_board = Checkers.get_best_move(game.board, depth=3, mandatory_jumping=True, maximizing_player=False)
            if best_board:
                game.ai_move(best_board)
            else:
                # No available moves; treat as loss for AI
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()