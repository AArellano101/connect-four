import pygame
import time
import connect_four_ai as c4
import numpy as np
pygame.font.init()

WIDTH, HEIGHT = 500, 450
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Four In A Row")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SMALLFONT = pygame.font.SysFont('comicsans', 40)
LARGEFONT = pygame.font.SysFont('comicsans', 70)


PLAYER_HEIGHT, PLAYER_WIDTH = 50, 50
BUTTON_HEIGHT, BUTTON_WIDTH = 150, 50
TILE_SIZE = 50
MARGIN_X, MARGIN_Y = 100, 150
ROW_COUNT = 6
COLUMN_COUNT = 7
COLUMNS = []
for col in range(COLUMN_COUNT + 1):
    COLUMNS.append(0.75* MARGIN_X + TILE_SIZE * col)
DEPTH = 5

Y = 1
R = 2
E = 0
    
def draw_gameboard(board, script, winner):
    board = np.flip(board, 0)
    WINDOW.fill(BLACK)
    for row in range(ROW_COUNT):
        for tile in range(COLUMN_COUNT):
            circleDims = (MARGIN_X + tile * TILE_SIZE, MARGIN_Y + row * TILE_SIZE)
            if not board[row][tile]:
                pygame.draw.circle(WINDOW, WHITE, circleDims, TILE_SIZE/2)
            elif board[row][tile] == Y:
                pygame.draw.circle(WINDOW, YELLOW, circleDims, TILE_SIZE/2)
            elif board[row][tile] == R:
                pygame.draw.circle(WINDOW, RED, circleDims, TILE_SIZE/2)
                
    if script:
        if winner == Y:
            text = LARGEFONT.render(script, True, YELLOW)
        elif winner == R:
            text = LARGEFONT.render(script, True, RED)
        else:
            text = SMALLFONT.render(script, True, WHITE)
            
        textRect = text.get_rect()
        textRect.center = ((WIDTH / 2), 50)
        WINDOW.blit(text, textRect)
    
    #print(board)
    pygame.display.update()
   
    
    return False
    
def write_info(script):
    text = LARGEFONT.render(script, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((WIDTH / 2), 50)
    WINDOW.blit(text, textRect)
    pygame.display.update()

def clicked_column(x_pos):
     for col in range(COLUMN_COUNT):
         if x_pos > COLUMNS[col] and x_pos < COLUMNS[col + 1]:
             return col
     return None

 
def main():
    run = True
    text = "Your Turn"
    current_player = Y
    board = c4.initial_state()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        draw_gameboard(board, text, c4.winner(board))
        if current_player == Y:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                mouse = pygame.mouse.get_pos()[0]
                column = clicked_column(mouse)
                board = c4.result(board, column, Y)
                time.sleep(0.2)
                current_player = R
                text = "AIs Turn (Red)"
                
                if c4.winner(board) == 1:
                    current_player = None
                    text = "You Won!"
        elif current_player == R:
            column = c4.minimax(board, DEPTH, True)[0]
            board = c4.result(board, column, R)
            time.sleep(0.2)
            current_player = Y
            text = "Your Turn (Yellow)"
            
            if c4.winner(board) == 2:
                current_player = None
                text = "Red Won!"
                
    pygame.quit()       

    
if __name__ == "__main__":
    main()
    