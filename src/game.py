import pygame
from board import Board
from constants import *
import random
from monte_carlo import MonteCarlo
from astart import ASTAR
from bfs import BFS
from dfs import DFS


class Game:
    def __init__(self, screen, algorithm):
        self.screen = screen
        self.algorithm = algorithm
        self.goats = []
        self.tigers = [(0, 0), (0, BOARD_SIZE), (BOARD_SIZE, 0), (BOARD_SIZE, BOARD_SIZE)]
        self.board = Board(screen)
        self.selected_tiger = None  # This will store the position of the selected tiger
        self.remaining_goat_number = 25
        self.goats_on_board = 0
        self.number_of_moves = 0
        self.needs_update = True  # Flag to track when the screen needs to be updated
        self.message = "On-going"
        self.restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3),
                                     (1, 4), (3, 4)}

    def place_goat(self):

        algorithm = self.algorithm

        empty_positions = [(row, col) for row in range(BOARD_SIZE + 1)
                           for col in range(BOARD_SIZE + 1)
                           if (row, col) not in self.goats and (row, col) not in self.tigers]
        new_goat_position = None
        if algorithm == "monte_carlo":
            new_goat_position = MonteCarlo.determine_goat_move(MonteCarlo(board=self.board), self.tigers, self.goats,
                                                               empty_positions, self.remaining_goat_number)
            print(new_goat_position)
        if algorithm == "astar":
            new_goat_position = ASTAR.determine_goat_move(self.tigers, self.goats, empty_positions)
        if algorithm == "bfs":
            new_goat_position = BFS.determine_goat_move(BFS(board=self.board), self.tigers, self.goats, empty_positions,
                                                        self.remaining_goat_number)
        if algorithm == "dfs":
            new_goat_position = DFS.determine_goat_move(DFS(board=self.board), self.tigers, self.goats, empty_positions,
                                                        self.remaining_goat_number)

        if new_goat_position is None:
            print("No valid moves available.")
            return  # Exit the function if no valid move is returned

        if new_goat_position is None:
            print("No valid moves available.")
            return  # Exit the function if no valid move is returned

        if new_goat_position[0] is None:
            self.goats.append(new_goat_position[1])
            self.goats_on_board += 1
        else:
            if new_goat_position[0] in self.goats:
                self.goats[self.goats.index(new_goat_position[0])] = new_goat_position[1]
        self.needs_update = True  # Set the flag to update the screen

    def game_status(self):
        # Checks if all tigers are trapped
        if all(not self.can_move(tiger) for tiger in self.tigers):
            return "Win for Goats"
        # Checks if all goats are captured
        if self.remaining_goat_number <= 5:
            return "Win for Tigers"
        # Checks for stalemate: no valid moves and all goats used
        if self.number_of_moves >= 100:
            return "Stalemate"
        return "On-going"

    def is_free(self, position):
        """ Check if a position is free of both tigers and goats """
        return position not in self.tigers and position not in self.goats

    def is_within_bounds(self, position):
        """ Check if a position is within the board boundaries """
        x, y = position
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def is_occupied_by_goat(self, position):
        """ Check if a position is occupied by a goat """
        return position in self.goats

    def can_move(self, tiger):
        """ Check if a tiger can move or jump to capture a goat, with restrictions on diagonal moves """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cardinal directions
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        all_possible_moves = directions.copy()

        if tiger not in self.restricted_positions:
            all_possible_moves.extend(diagonal_directions)  # Allow diagonal moves only from non-restricted positions

        for d in all_possible_moves:
            normal_move = (tiger[0] + d[0], tiger[1] + d[1])
            jump_move = (tiger[0] + 2 * d[0], tiger[1] + 2 * d[1])
            if self.is_within_bounds(normal_move) and self.is_free(normal_move):
                return True
            if self.is_within_bounds(jump_move) and self.is_occupied_by_goat(normal_move) and self.is_free(jump_move):
                return True

        return False

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
                    self.needs_update = True

                    #  Checking Game Status
                    current_game_status = self.game_status()
                    self.message = current_game_status

                    goats_in_path, goat_pos = self.is_goat_in_path(self.selected_tiger, new_position)
                    print(goat_pos)
                    if goats_in_path:  # If there are goats in the path, remove the first one
                        self.goats.remove(goat_pos)
                        self.goats_on_board -= 1
                        self.remaining_goat_number -= 1
                        self.needs_update = True
                    self.selected_tiger = None
                    self.number_of_moves += 1
                    # Update screen to show selected tiger
                    self.needs_update = True
                    print("```Tiger Moved``````````")
                    # After moving tiger, place a goat randomly
                    self.place_goat()
                    self.needs_update = True
            else:
                # Check if a tiger is clicked
                if (row, col) in self.tigers:
                    print("```Tiger Clicked`````````````")
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

            # Check game status
            if self.message != "On-going":
                self.message = f"Game over: {self.message}"  # Update message based on game status
                print("Inside status loop")
            #self.needs_update = True
            if self.needs_update:  # Only draw when needed
                self.screen.fill(BACKGROUND_COLOR)  # Clear the screen
                self.board.draw(self.goats, self.tigers)  # Draw the board and the pieces
                self.board.draw_info(self.goats_on_board, self.remaining_goat_number, self.number_of_moves,
                                     self.message)
                pygame.display.flip()  # Update the display
                self.needs_update = False  # Reset the update flag

        pygame.quit()
