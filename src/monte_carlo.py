import random
import math
from constants import BOARD_SIZE  # Assuming BOARD_SIZE is defined in constants


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.state = state
        self.untried_moves = state.get_legal_moves()

    def select_child(self):
        """Select a child node with the highest UCB1 value."""
        return max(self.children, key=lambda c: (c.wins / c.visits) + math.sqrt(2 * math.log(self.visits) / c.visits))

    def add_child(self, move, state):
        """Add a new child node for the given move."""
        child = Node(move=move, parent=self, state=state)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        """Update this node - increment the visit count by 1 and increase wins by the result of the play-out."""
        self.visits += 1
        self.wins += result  # Adjust how result affects wins if necessary

    def __repr__(self):
        return f"[M:{self.move} W/V:{self.wins}/{self.visits} U:{len(self.untried_moves)}]"


class MonteCarlo:
    def __init__(self, board, iterations=1000, time_limit=None):
        self.board = board
        self.iterations = iterations
        self.time_limit = time_limit

    def determine_goat_move(self, tigers, goats, empty_positions, remaining_goat_number):
        import time
        start_time = time.time()
        root = Node(state=State(tigers, goats, empty_positions, remaining_goat_number))

        for _ in range(self.iterations):
            node = root
            state = root.state.clone()

            # Selection
            while not node.untried_moves and node.children:
                node = node.select_child()
                state.do_move(node.move)

            # Expansion
            if node.untried_moves:
                m = random.choice(node.untried_moves)
                state.do_move(m)
                node = node.add_child(m, state)

            # Simulation
            while state.get_legal_moves():
                state.do_move(random.choice(state.get_legal_moves()))

            # Backpropagation
            while node:
                result = state.get_result()
                node.update(result)
                node = node.parent

            if self.time_limit and (time.time() - start_time > self.time_limit):
                break

        if not root.children:
            return None  # Handle no valid moves
        return max(root.children, key=lambda c: c.visits).move

class State:
    def __init__(self, tigers, goats, empty_positions, remaining_goat_number):
        self.tigers = tigers
        self.goats = goats
        self.empty_positions = empty_positions
        self.remaining_goat_number = remaining_goat_number

    def get_legal_moves(self):
        """ List all possible legal moves for the goats, considering safety and restricted positions. """
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3), (1, 4), (3, 4)}

        legal_moves = []
        if self.remaining_goat_number > 0:
            # Prioritize safe placements before risky ones
            safe_empty_positions = [empty for empty in self.empty_positions if not self.is_adjacent_to_tiger(empty)]
            risky_empty_positions = [empty for empty in self.empty_positions if self.is_adjacent_to_tiger(empty)]
            for empty in safe_empty_positions + risky_empty_positions:
                legal_moves.append((None, empty))  # None signifies placement of a new goat

        # Movement moves
        for goat in self.goats:
            allowed_directions = normal_directions if goat in restricted_positions else normal_directions + diagonal_directions
            for dx, dy in allowed_directions:
                nx, ny = goat[0] + dx, goat[1] + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in self.tigers and (nx, ny) not in self.goats:
                    if not self.is_adjacent_to_tiger((nx, ny)):
                        legal_moves.insert(0, (goat, (nx, ny)))  # Prioritize safer moves
                    else:
                        legal_moves.append((goat, (nx, ny)))  # Add risky moves if necessary
        return legal_moves

    def do_move(self, move):
        """ Update the state by performing a move """
        goat_position, new_position = move
        if goat_position:
            # Move existing goat
            self.goats.remove(goat_position)
            self.goats.append(new_position)
            self.empty_positions.append(goat_position)
        else:
            # Place new goat
            self.goats.append(new_position)
        self.empty_positions.remove(new_position)

    def is_adjacent_to_tiger(self, position):
        """ Check if a position is adjacent to any tiger """
        px, py = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return any((px + dx, py + dy) in self.tigers for dx, dy in directions)

    def get_result(self):
        """ Evaluate the game state from the goats' perspective, prioritizing safety. """
        # if not self.goats:
        #     return -1  # All goats are captured, tigers win

        score = 0
        for goat in self.goats:
            if self.is_adjacent_to_tiger(goat):
                score -= 10  # Penalize positions where goats are next to tigers

        # Tigers' movement evaluation
        # for tiger in self.tigers:
        #     for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        #         if self.can_move(tiger, direction):
        #             score += 3  # Game continues, evaluate based on tiger mobility

        return score

    def can_move(self, position, direction):
        """ Check if a move is valid given a position and direction, considering board boundaries and other pieces """
        px, py = position
        dx, dy = direction
        nx, ny = px + dx, py + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if (nx, ny) not in self.tigers and (nx, ny) not in self.goats:
                return True
        return False

    def clone(self):
        """ Create a deep copy of the current game state """
        return State(self.tigers.copy(), self.goats.copy(), self.empty_positions.copy(), self.remaining_goat_number)


