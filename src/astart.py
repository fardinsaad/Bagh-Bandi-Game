import random
from constants import *


class ASTAR:
    # def determine_goat_move(board, tigers, goats, empty_positions):
    #         new_goat_position = random.choice(empty_positions)
    #         return new_goat_position

    def __init__(self, board):
        self.board = board

    #
    # def manhattan_distance(self, start, goal):
    #     return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    #
    # def get_neighbors(self, position):
    #     x, y = position
    #     return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #
    # def is_valid_move(self, move, empty_positions, goats):
    #     if move in empty_positions and move not in goats:
    #         return True
    #     return False
    #
    # def a_star_search(self, start, goal, empty_positions, goats):
    #     frontier = []
    #     heapq.heappush(frontier, (0, start))
    #     came_from = {}
    #     cost_so_far = {start: 0}
    #
    #     while frontier:
    #         current_cost, current_position = heapq.heappop(frontier)
    #
    #         if current_position == goal:
    #             break
    #
    #         for next_position in self.get_neighbors(current_position):
    #             new_cost = cost_so_far[current_position] + 1
    #             if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
    #                 if self.is_valid_move(next_position, empty_positions, goats):
    #                     cost_so_far[next_position] = new_cost
    #                     priority = new_cost + self.manhattan_distance(goal, next_position)
    #                     heapq.heappush(frontier, (priority, next_position))
    #                     came_from[next_position] = current_position
    #
    #     path = []
    #     current = goal
    #     while current != start:
    #         path.append(current)
    #         current = came_from[current]
    #     path.reverse()
    #     return path

    # def determine_goat_move(self, tigers, goats, empty_positions):
    #     print("tigers", tigers, "goats", goats, "empty positions,", empty_positions)
    #     closest_tiger = None
    #     closest_distance = float('inf')
    #     for slot in empty_positions:
    #         for t in tigers:
    #             distance = self.manhattan_distance(goat, t)
    #             if distance < closest_distance:
    #                 closest_distance = distance
    #                 closest_tiger = t
    #     path = self.a_star_search(goats[0], closest_tiger, empty_positions, goats)
    #     if len(path) == 2:
    #         return (goats[0], path[1])
    #     return None
    # def get_legal_moves(self):
    #     """ List all possible legal moves for the goats, considering safety and restricted positions. """
    #     normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    #     diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    #     restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3), (1, 4), (3, 4)}
    #
    #     legal_moves = []
    #     if self.remaining_goat_number > 0:
    #         # Prioritize safe placements before risky ones
    #         safe_empty_positions = [empty for empty in self.empty_positions if not self.is_adjacent_to_tiger(empty)]
    #         risky_empty_positions = [empty for empty in self.empty_positions if self.is_adjacent_to_tiger(empty)]
    #         for empty in safe_empty_positions + risky_empty_positions:
    #             legal_moves.append((None, empty))  # None signifies placement of a new goat
    #
    #     # Movement moves
    #     for goat in self.goats:
    #         allowed_directions = normal_directions if goat in restricted_positions else normal_directions + diagonal_directions
    #         for dx, dy in allowed_directions:
    #             nx, ny = goat[0] + dx, goat[1] + dy
    #             if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in self.tigers and (nx, ny) not in self.goats:
    #                 if not self.is_adjacent_to_tiger((nx, ny)):
    #                     legal_moves.insert(0, (goat, (nx, ny)))  # Prioritize safer moves
    #                 else:
    #                     legal_moves.append((goat, (nx, ny)))  # Add risky moves if necessary
    #     return legal_moves
    def is_adjacent_to_tiger(self, position, tigers):
        """ Check if a position is adjacent to any tiger """
        px, py = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        adjacent_tigers = [(px + dx, py + dy) for dx, dy in directions if (px + dx, py + dy) in tigers]
        return adjacent_tigers

    def is_adjacent_to_empty_space(self, position, empty_positions):
        """ Check if a position is adjacent to any tiger """
        px, py = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        adjacent_empty_space = [(px + dx, py + dy) for dx, dy in directions if (px + dx, py + dy) in empty_positions]
        return adjacent_empty_space

    def determine_goat_move(self, tigers, goats, empty_positions):
        # print("tigers", tigers, "goats", goats, "empty positions,", empty_positions)
        closest_tiger = None
        closest_distance = float('inf')
        normal_directions = [(0, -1), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3), (1, 4),
                                (3, 4)}
        legal_moves = []
        list_of_heuristic = []
        for slot in empty_positions:
            if slot in restricted_positions:
                directions = normal_directions  # Only horizontal and vertical moves
            else:
                directions = normal_directions + diagonal_directions  # All possible moves

            for dx, dy in directions:
                nx, ny = slot[0] + dx, slot[1] + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if (nx, ny) not in tigers and (nx, ny) not in goats:
                        legal_moves.append((slot, (nx, ny)))
                        heuristic = self.calculate_heuristic( slot, (nx, ny), goats, tigers)
                        heuristic.append(heuristic)

        print(legal_moves)
        print(list_of_heuristic)
        return legal_moves

    def calculate_heuristic(self, slot, new_position,  goats, tigers):
        print("Calculate Hhhhhhhhhhhh")
        print(slot, new_position)
        //write some code
        heuristic = 1
        return [heuristic, slot, new_position ]
