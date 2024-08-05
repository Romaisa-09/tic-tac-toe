import pygame
import sys
import time
import tictactoe as ttt

pygame.init()
screen = pygame.display.set_mode((600, 400))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load Fonts
font_paths = {
    "medium": ("OpenSans-Regular.ttf", 28),
    "large": ("OpenSans-Regular.ttf", 40),
    "move": ("OpenSans-Regular.ttf", 60)
}
fonts = {key: pygame.font.Font(path, size) for key, (path, size) in font_paths.items()}

user = None
board = ttt.initial_state()
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    if user is None:
        title = fonts["large"].render("Play Tic-Tac-Toe", True, WHITE)
        screen.blit(title, title.get_rect(center=(300, 50)))

        play_x_button = pygame.Rect(75, 200, 150, 50)
        play_o_button = pygame.Rect(375, 200, 150, 50)

        pygame.draw.rect(screen, WHITE, play_x_button)
        pygame.draw.rect(screen, WHITE, play_o_button)

        screen.blit(fonts["medium"].render("Play as X", True, BLACK), play_x_button.move(25, 10))
        screen.blit(fonts["medium"].render("Play as O", True, BLACK), play_o_button.move(25, 10))

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if play_x_button.collidepoint(mouse_pos):
                time.sleep(0.2)
                user = ttt.X
            elif play_o_button.collidepoint(mouse_pos):
                time.sleep(0.2)
                user = ttt.O
    else:
        tile_size = 80
        tile_origin = (300 - 1.5 * tile_size, 200 - 1.5 * tile_size)
        tiles = [[pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size) for j in range(3)] for i in range(3)]

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                pygame.draw.rect(screen, WHITE, tiles[i][j], 3)
                if cell != ttt.EMPTY:
                    screen.blit(fonts["move"].render(cell, True, WHITE), tiles[i][j].move(15, 5))

        if ttt.terminal(board):
            title = fonts["large"].render(f"Game Over: {'Tie' if ttt.winner(board) is None else f'{ttt.winner(board)} wins'}", True, WHITE)
        elif user == ttt.player(board):
            title = fonts["large"].render(f"Play as {user}", True, WHITE)
        else:
            title = fonts["large"].render("Computer thinking...", True, WHITE)
        
        screen.blit(title, title.get_rect(center=(300, 30)))

        if user != ttt.player(board) and not ttt.terminal(board):
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        if pygame.mouse.get_pressed()[0] and user == ttt.player(board) and not ttt.terminal(board):
            mouse_pos = pygame.mouse.get_pos()
            for i, row in enumerate(tiles):
                for j, tile in enumerate(row):
                    if board[i][j] == ttt.EMPTY and tile.collidepoint(mouse_pos):
                        board = ttt.result(board, (i, j))

        if ttt.terminal(board):
            again_button = pygame.Rect(200, 335, 200, 50)
            pygame.draw.rect(screen, WHITE, again_button)
            screen.blit(fonts["medium"].render("Play Again", True, BLACK), again_button.move(50, 10))
            if pygame.mouse.get_pressed()[0] and again_button.collidepoint(pygame.mouse.get_pos()):
                time.sleep(0.2)
                user = None
                board = ttt.initial_state()
                ai_turn = False

    pygame.display.flip()
