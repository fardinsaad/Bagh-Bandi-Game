import pygame
from board import Board
from constants import *

class Game:
    def __init__(self, screen):
        self.goats = []
        self.tigers = [(0, 0), (0, BOARD_SIZE), (BOARD_SIZE, 0), (BOARD_SIZE, BOARD_SIZE)]
        self.board = Board(screen)

    def handle_click(self, pos):
        x, y = pos[0] - MARGIN, pos[1] - MARGIN
        col, row = round(x / CELL_SIZE), round(y / CELL_SIZE)
        if abs(x - col * CELL_SIZE) < CELL_SIZE // 4 and abs(y - row * CELL_SIZE) < CELL_SIZE // 4:
            if 0 <= col <= BOARD_SIZE and 0 <= row <= BOARD_SIZE:
                if (row, col) not in self.goats and (row, col) not in self.tigers:
                    self.goats.append((row, col))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.board.draw(self.goats, self.tigers)
        pygame.quit()
