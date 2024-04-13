import pygame
from constants import *
import pygame.font
class Board:
    def __init__(self, screen):
        self.screen = screen

    def draw_info(self, goats_on_board, remaining_goat_number, number_of_moves):
        # Position the text at the bottom of the board
        info_y_position = SCREEN_SIZE  - 500  # Adjust this as necessary
        self.draw_text(f"Remaining Goats: {remaining_goat_number}", (MARGIN-50, info_y_position))
        self.draw_text(f"Goats on Board: {goats_on_board}", (MARGIN + 200, info_y_position))
        self.draw_text(f"Moves: {number_of_moves}", (MARGIN + 450, info_y_position))

    def draw_text(self, text, position, font_size=30, color=(61, 52, 235)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)
    def draw_lines(self):
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE + MARGIN, MARGIN),
                             (i * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN), 1)
            pygame.draw.line(self.screen, LINE_COLOR, (MARGIN, i * CELL_SIZE + MARGIN),
                             (SCREEN_SIZE + MARGIN, i * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (MARGIN, MARGIN),
                         (SCREEN_SIZE + MARGIN, SCREEN_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (SCREEN_SIZE + MARGIN, MARGIN),
                         (MARGIN, SCREEN_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, MARGIN),
                         (MARGIN, 2 * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, MARGIN),
                         (SCREEN_SIZE + MARGIN, 2 * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN),
                         (MARGIN, 2 * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN),
                         (SCREEN_SIZE + MARGIN, 2 * CELL_SIZE + MARGIN), 1)

    def draw_pieces(self, goats, tigers):
        for goat in goats:
            center = ((goat[1] * CELL_SIZE) + MARGIN, (goat[0] * CELL_SIZE) + MARGIN)
            pygame.draw.circle(self.screen, GOAT_COLOR, center, CELL_SIZE // 8)

        for tiger in tigers:
            center = ((tiger[1] * CELL_SIZE) + MARGIN, (tiger[0] * CELL_SIZE) + MARGIN)
            pygame.draw.circle(self.screen, TIGER_COLOR, center, CELL_SIZE // 8)

    def draw(self, goats, tigers):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_lines()
        self.draw_pieces(goats, tigers)
        pygame.display.flip()
