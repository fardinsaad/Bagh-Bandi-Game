import pygame
from constants import *

class Board:
    def __init__(self, screen):
        self.screen = screen

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
