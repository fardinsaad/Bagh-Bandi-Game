import pygame
from board import Board
from constants import *
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.goats = []
        self.tigers = [(0, 0), (0, BOARD_SIZE), (BOARD_SIZE, 0), (BOARD_SIZE, BOARD_SIZE)]
        self.board = Board(screen)
        self.selected_tiger = None  # This will store the position of the selected tiger
        self.remaining_goat_number = 16
        self.goats_on_board = 0
        self.number_of_moves = 0
        self.needs_update = True  # Flag to track when the screen needs to be updated

    def place_goat(self):
        empty_positions = [(row, col) for row in range(BOARD_SIZE)
                                       for col in range(BOARD_SIZE)
                                       if (row, col) not in self.goats and (row, col) not in self.tigers]
        if empty_positions:
            new_goat_position = random.choice(empty_positions)
            self.goats.append(new_goat_position)
            self.goats_on_board += 1
            self.needs_update = True  # Set the flag to update the screen

    def is_goat_in_path(self, old_pos, new_pos):
        path = self.calculate_path(old_pos, new_pos)
        for pos in path:
            if pos in self.goats:
                return True, pos
        return False, None

    def calculate_path(self, start, end):
        path = []
        start_row, start_col = start
        end_row, end_col = end
        row_step = (end_row - start_row) // max(abs(end_row - start_row), 1)
        col_step = (end_col - start_col) // max(abs(end_col - start_col), 1)

        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != end:
            path.append((current_row, current_col))
            current_row += row_step
            current_col += col_step

        return path

    def handle_click(self, pos):
        x, y = pos[0] - MARGIN, pos[1] - MARGIN
        col, row = round(x / CELL_SIZE), round(y / CELL_SIZE)
        if 0 <= col <= BOARD_SIZE and 0 <= row <= BOARD_SIZE:
            new_position = (row, col)
            if self.selected_tiger:
                if new_position not in self.goats and new_position not in self.tigers:
                    self.tigers.remove(self.selected_tiger)
                    self.tigers.append(new_position)
                    goats_in_path, goat_pos = self.is_goat_in_path(self.selected_tiger, new_position)
                    print(goat_pos)
                    if goats_in_path:  # If there are goats in the path, remove the first one
                        self.goats.remove(goat_pos)
                        self.goats_on_board -= 1
                        self.remaining_goat_number -=1
                        self.needs_update = True
                    self.selected_tiger = None
                    self.number_of_moves += 1
                    self.needs_update = True  # Update screen to show selected tiger

                    # After moving tiger, place a goat randomly
                    self.place_goat()
            else:
                # Check if a tiger is clicked
                if (row, col) in self.tigers:
                    self.selected_tiger = (row, col)
                    self.needs_update = True

    def run(self):
        running = True
        clock = pygame.time.Clock()  # Create a clock object to manage refresh rate
        self.place_goat()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            if self.needs_update:  # Only draw when needed
                self.screen.fill(BACKGROUND_COLOR)  # Clear the screen
                self.board.draw(self.goats, self.tigers)  # Draw the board and the pieces
                self.board.draw_info(self.goats_on_board, self.remaining_goat_number, self.number_of_moves)
                pygame.display.flip()  # Update the display
                self.needs_update = False  # Reset the update flag

        pygame.quit()

