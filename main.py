import pygame
import sys
import numpy as np
from new import create_board, is_valid_move, drop_piece, winning_move, best_move

pygame.init()

# Constants
WIDTH, HEIGHT = 700, 600
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FONT_SIZE = 36
FONT_COLOR = (0, 0, 0)

# Initialize game variables
board = create_board()
game_over = False
current_player = 1
font = pygame.font.Font(None, FONT_SIZE)

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

def draw_board():
    screen.fill(WHITE)
    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            pygame.draw.rect(screen, (0,0,255), (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, WHITE, (c * SQUARE_SIZE + int(SQUARE_SIZE / 2),
                                              r * SQUARE_SIZE + int(SQUARE_SIZE / 2)), RADIUS)

    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARE_SIZE + int(SQUARE_SIZE / 2),
                                                HEIGHT - r * SQUARE_SIZE - int(SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARE_SIZE + int(SQUARE_SIZE / 2),
                                                   HEIGHT - r * SQUARE_SIZE - int(SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

def display_message(message):
    text = font.render(message, True, FONT_COLOR)
    screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
    pygame.display.update()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and current_player == 1 and not game_over:
            posx = event.pos[0]
            col = posx // SQUARE_SIZE
            if is_valid_move(board, col):
                row = board.shape[0] - 1
                while row >= 0:
                    if board[row][col] == 0:
                        drop_piece(board, col, current_player)
                        draw_board()
                        if winning_move(board, current_player):
                            print(f"Player {current_player} wins!")
                            game_over = True
                            display_message(f"Player {current_player} wins!")
                        current_player = 3 - current_player
                        break
                    row -= 1
                if row < 0:
                    print("Column is full. Choose another column.")

    if current_player == 2 and not game_over:
        # Display "AI is thinking..."
        font = pygame.font.Font(None, 72)
        thinking_text = font.render("AI is thinking...", True, (249, 255, 0))
        text_rect = thinking_text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
        screen.blit(thinking_text, text_rect)
        pygame.display.update() 
        #screen.blit(thinking_text, (10, 10))
        #pygame.display.update()  # Update the display after blitting the text

        col = best_move(board)
        if is_valid_move(board, col):
            row = board.shape[0] - 1
            while row >= 0:
                if board[row][col] == 0:
                    drop_piece(board, col, current_player)
                    draw_board()
                    if winning_move(board, current_player):
                        print(f"AI wins!")
                        game_over = True
                        display_message(f"AI wins!")
                    current_player = 3 - current_player
                    break
                row -= 1

    draw_board()
    pygame.display.update()