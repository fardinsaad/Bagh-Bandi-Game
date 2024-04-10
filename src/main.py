import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_SIZE = 600
BOARD_SIZE = 5
CELL_SIZE = SCREEN_SIZE // BOARD_SIZE
LINE_COLOR = (0, 0, 0)
GOAT_COLOR = (255, 0, 0)
TIGER_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Bagh Bandi Game')

# Initial game state
goats = []
tigers = [(0, 0), (0, 4), (4, 0), (4, 4)]  # Starting positions for tigers

def draw_board():
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        for y in range(0, SCREEN_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BACKGROUND_COLOR, rect, 0)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

    # Draw goats
    for goat in goats:
        center = (goat[0] * CELL_SIZE + CELL_SIZE // 2, goat[1] * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, GOAT_COLOR, center, CELL_SIZE // 4)

    # Draw tigers
    for tiger in tigers:
        center = (tiger[0] * CELL_SIZE + CELL_SIZE // 2, tiger[1] * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, TIGER_COLOR, center, CELL_SIZE // 4)

def handle_click(pos):
    col = pos[0] // CELL_SIZE
    row = pos[1] // CELL_SIZE
    print(f"Clicked on row {row}, col {col}")

    # Placeholder for more complex logic, like moving pieces or placing goats
    if (row, col) not in goats and (row, col) not in tigers:  # Simple condition to place goats
        goats.append((row, col))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    draw_board()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
