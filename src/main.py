import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the game
MARGIN = 50  # Width of the margin around the board
SCREEN_SIZE = 600
BOARD_SIZE = 4
CELL_SIZE = SCREEN_SIZE // BOARD_SIZE
LINE_COLOR = (0, 0, 0)
GOAT_COLOR = (255, 0, 0)  # Red
TIGER_COLOR = (0, 128, 0)  # Dark Green
BACKGROUND_COLOR = (255, 255, 255)  # White

# Adjust the screen size for the margin
WINDOW_SIZE = (SCREEN_SIZE + 2 * MARGIN, SCREEN_SIZE + 2 * MARGIN)

# Set up the display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Bagh Bandi Game')

# Initial game state
goats = []
# Adjust the tigers' starting positions to be at the corners of the grid
tigers = [(0, 0), (0, 4), (4, 0), (4, 4)]



def draw_board():
    screen.fill(BACKGROUND_COLOR)

    # Draw the vertical and horizontal lines
    for i in range(BOARD_SIZE + 1):
        start_pos = (i * CELL_SIZE + MARGIN, MARGIN)
        end_pos = (i * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN)
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 1)
        start_pos = (MARGIN, i * CELL_SIZE + MARGIN)
        end_pos = (SCREEN_SIZE + MARGIN, i * CELL_SIZE + MARGIN)
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 1)

    # Draw the diagonal lines
    pygame.draw.line(screen, LINE_COLOR, (MARGIN, MARGIN), (SCREEN_SIZE + MARGIN, SCREEN_SIZE + MARGIN), 1)
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_SIZE + MARGIN, MARGIN), (MARGIN, SCREEN_SIZE + MARGIN), 1)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, MARGIN), (MARGIN, 2 * CELL_SIZE + MARGIN), 1)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, MARGIN), (SCREEN_SIZE + MARGIN, 2 * CELL_SIZE + MARGIN), 1)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN), (MARGIN, 2 * CELL_SIZE + MARGIN), 1)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN), (SCREEN_SIZE + MARGIN, 2 * CELL_SIZE + MARGIN), 1)

    # Draw goats and tigers at the intersections
    for goat in goats:
        center = ((goat[1] * CELL_SIZE) + MARGIN, (goat[0] * CELL_SIZE) + MARGIN)
        pygame.draw.circle(screen, GOAT_COLOR, center, CELL_SIZE // 8)

    for tiger in tigers:
        center = ((tiger[1] * CELL_SIZE) + MARGIN, (tiger[0] * CELL_SIZE) + MARGIN)
        pygame.draw.circle(screen, TIGER_COLOR, center, CELL_SIZE // 8)


def handle_click(pos):
    # Calculate the nearest intersection point
    x = pos[0] - MARGIN  # Adjusted for margin
    y = pos[1] - MARGIN  # Adjusted for margin
    col = round(x / CELL_SIZE)
    row = round(y / CELL_SIZE)

    # Calculate the exact position of the intersection
    exact_x = col * CELL_SIZE + MARGIN
    exact_y = row * CELL_SIZE + MARGIN

    # Check if the click was close enough to the intersection
    if abs(x - col * CELL_SIZE) < CELL_SIZE // 4 and abs(y - row * CELL_SIZE) < CELL_SIZE // 4:
        print(f"Clicked near intersection at row {row}, col {col}")

        # Check if the position is within the bounds of the board
        if 0 <= col <= BOARD_SIZE and 0 <= row <= BOARD_SIZE:
            # Check if the intersection is not already occupied
            intersection = (row, col)
            if intersection not in goats and intersection not in [(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)]:
                goats.append(intersection)
                print(goats)


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
