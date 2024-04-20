import pygame as pg
import sys
import numpy as np

# Dimensions de la fenêtre et des cases
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700  # Ajuster la hauteur pour inclure la zone de message
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Dimensions de la zone de message
MESSAGE_AREA_HEIGHT = 100
MESSAGE_AREA_COLOR = (200, 200, 200)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Exemple de grille Sudoku (0 représente une case vide)
EXAMPLE_BOARD = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

class SudokuGame:
    def __init__(self):
        self.grid = EXAMPLE_BOARD.copy()
        self.selected = None
        self.error_message = ""  # Initialiser le message d'erreur comme une chaîne vide
    def draw(self, screen):
        screen.fill(WHITE)
        # Dessiner la zone de jeu
        self.draw_board(screen)
        # Dessiner la zone de message
        self.draw_message_area(screen)
    def draw_board(self, screen):
        for i in range(GRID_SIZE + 1):
            thickness = 4 if i % 3 == 0 else 1
            pg.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), thickness)
            pg.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT - CELL_SIZE), thickness)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                if value != 0:
                    self.draw_number(screen, value, (j, i))
        if self.selected:
            pg.draw.rect(screen, BLUE, (self.selected[0] * CELL_SIZE, self.selected[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    def draw_message_area(self, screen):
        pg.draw.rect(screen, MESSAGE_AREA_COLOR, (0, SCREEN_HEIGHT - MESSAGE_AREA_HEIGHT, SCREEN_WIDTH, MESSAGE_AREA_HEIGHT))
        font = pg.font.Font(None, 25)
        text = font.render(self.error_message, True, BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - MESSAGE_AREA_HEIGHT // 2))
        screen.blit(text, text_rect)
    def draw_number(self, screen, value, pos):
        font = pg.font.Font(None, 40)
        text = font.render(str(value), True, BLACK)
        text_rect = text.get_rect(center=(pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2))
        screen.blit(text, text_rect)
    def is_valid_move(self, value, pos):
        row, col = pos
        if value == 0:
            return True
        # Check row
        if value in self.grid[row, :]:
            return False
        # Check column
        if value in self.grid[:, col]:
            return False
        # Check 3x3 grid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        if value in self.grid[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True
    def input_number(self, number):
        if self.selected:
            col, row = self.selected
            if self.is_valid_move(number, (row, col)):
                self.grid[row][col] = number
                self.error_message = ""  
            else:
                self.error_message = "Mouvement invalide"
    def click(self, pos):
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT - MESSAGE_AREA_HEIGHT:
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            self.selected = (col, row)
        else:
            self.selected = None
def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("ARIJ Game")
    sudoku_game = SudokuGame()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                sudoku_game.click(pos)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    sudoku_game.input_number(1)
                elif event.key == pg.K_2:
                    sudoku_game.input_number(2)
                elif event.key == pg.K_3:
                    sudoku_game.input_number(3)
                elif event.key == pg.K_4:
                    sudoku_game.input_number(4)
                elif event.key == pg.K_5:
                    sudoku_game.input_number(5)
                elif event.key == pg.K_6:
                    sudoku_game.input_number(6)
                elif event.key == pg.K_7:
                    sudoku_game.input_number(7)
                elif event.key == pg.K_8:
                    sudoku_game.input_number(8)
                elif event.key == pg.K_9:
                    sudoku_game.input_number(9)
                elif event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                    sudoku_game.input_number(0)
        screen.fill(WHITE)
        sudoku_game.draw(screen)
        pg.display.flip()
    pg.quit()
    sys.exit()
if __name__ == "__main__":
    main()