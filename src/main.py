import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_SIZE = 600
BOARD_SIZE = 4
CELL_SIZE = SCREEN_SIZE // BOARD_SIZE
LINE_COLOR = (0, 0, 0)
GOAT_COLOR = (255, 0, 0)  # Red
TIGER_COLOR = (0, 128, 0)  # Dark Green
BACKGROUND_COLOR = (255, 255, 255)  # White

# Set up the display
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Bagh Bandi Game')

# Initial game state
goats = []
tigers = [(0, 0), (0, 4), (4, 0), (4, 4)]  # Starting positions for tigers


def draw_board():
    screen.fill(BACKGROUND_COLOR)

    # Draw the vertical and horizontal lines
    for i in range(BOARD_SIZE):
        start_pos = (i * CELL_SIZE, 0)
        end_pos = (i * CELL_SIZE, SCREEN_SIZE)
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 1)

        start_pos = (0, i * CELL_SIZE)
        end_pos = (SCREEN_SIZE, i * CELL_SIZE)
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 1)


    pygame.draw.line(screen, LINE_COLOR, (0, 0), (4* CELL_SIZE , SCREEN_SIZE), 1)
    pygame.draw.line(screen, LINE_COLOR, (4* CELL_SIZE, 0), (0 , SCREEN_SIZE), 1)

    pygame.draw.line(screen, LINE_COLOR, (2* CELL_SIZE, 0), (0 , 2* CELL_SIZE), 1)
    pygame.draw.line(screen, LINE_COLOR, (2* CELL_SIZE, 0), (4* CELL_SIZE , 2* CELL_SIZE), 1)


    pygame.draw.line(screen, LINE_COLOR, (2* CELL_SIZE, 4* CELL_SIZE), (0 , 2* CELL_SIZE), 1)
    pygame.draw.line(screen, LINE_COLOR, (2* CELL_SIZE, 4* CELL_SIZE), (4* CELL_SIZE , 2* CELL_SIZE), 1)







    # Draw goats
    for goat in goats:
        center = (goat[1] * CELL_SIZE, goat[0] * CELL_SIZE)
        pygame.draw.circle(screen, GOAT_COLOR, center, CELL_SIZE // 8)

    # Draw tigers
    for tiger in tigers:
        center = (tiger[1] * CELL_SIZE, tiger[0] * CELL_SIZE)
        pygame.draw.circle(screen, TIGER_COLOR, center, CELL_SIZE // 8)


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
