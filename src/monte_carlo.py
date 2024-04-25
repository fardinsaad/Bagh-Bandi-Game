import random
from constants import *
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
        """ Select a child node with the highest UCB1 value """
        import math
        return max(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))

    def add_child(self, move, state):
        """ Add a new child node for the given move """
        child = Node(move=move, parent=self, state=state)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        """ Update this node - increment the visit count by 1 and increase wins by the result of the play-out """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return f"[M:{self.move} W/V:{self.wins}/{self.visits} U:{self.untried_moves}]"


class MonteCarlo:
    def __init__(self, board, iterations=1000, time_limit=None):
        self.board = board
        self.board_size = 4
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

            # Expansion        print(move)

            if node.untried_moves:
                m = random.choice(node.untried_moves)
                state.do_move(m)
                node = node.add_child(m, state)

            # Simulation
            while state.get_legal_moves():
                state.do_move(random.choice(state.get_legal_moves()))

            # Backpropagation
            while node:
                node.update(state.get_result())
                node = node.parent

            if self.time_limit and (time.time() - start_time > self.time_limit):
                break

        # Handle the case where there are no children (e.g., no valid moves were added)
        if not root.children:
            # Return a special value or handle it based on your game logic
            return None
        return max(root.children, key=lambda c: c.visits).move


class State:
    def __init__(self, tigers, goats, empty_positions, remaining_goat_number):
        self.tigers = tigers
        self.goats = goats
        self.empty_positions = empty_positions
        self.remaining_goat_number = remaining_goat_number

    def get_legal_moves(self):
        """ List all possible legal moves for the goats """
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        restricted_positions = {(1, 1), (1, 3), (3, 1), (3, 3), (1,4), (1,0), (3,0), (3,4), (0,1), (0,3), (2,1), (2,3), (4,1), (4,3)}

        legal_moves = []
        if self.remaining_goat_number > 0:
            # If fewer than 16 goats, any empty position can be a new goat placement
            for empty in self.empty_positions:
                legal_moves.append((None, empty))  # None signifies no goat is moving, it's a placement

            for goat in self.goats:
                if goat in restricted_positions:
                    directions = normal_directions  # Only horizontal and vertical moves
                else:
                    directions = normal_directions + diagonal_directions  # All possible moves

                for dx, dy in directions:
                    nx, ny = goat[0] + dx, goat[1] + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if (nx, ny) not in self.tigers and (nx, ny) not in self.goats:
                            legal_moves.append((goat, (nx, ny)))
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
    def get_result(self):
        """ Determine the result of a game from the goats' perspective """
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        restricted_positions = {(1, 1), (1, 3), (3, 1), (3, 3), (1, 4), (1, 0), (3, 0), (3, 4), (0, 1), (0, 3), (2, 1),
                                (2, 3), (4, 1), (4, 3)}

        if not self.goats:
            return -1  # All goats are captured, tigers win

        # Check if tigers have any valid moves

        for tiger in self.tigers:
            if tiger in restricted_positions:
                directions = normal_directions  # Only horizontal and vertical moves
            else:
                directions = normal_directions + diagonal_directions  # All possible moves

            for dx, dy in directions:
                # Check simple move
                adj_x, adj_y = tiger[0] + dx, tiger[1] + dy
                if 0 <= adj_x <= BOARD_SIZE and 0 <= adj_y <= BOARD_SIZE:
                    if (adj_x, adj_y) not in self.tigers and (adj_x, adj_y) not in self.goats:
                        return 0  # Tigers can still move, game continues

                # Check jump move
                jump_x, jump_y = tiger[0] + 2 * dx, tiger[1] + 2 * dy
                if 0 <= jump_x <= BOARD_SIZE and 0 <= jump_y <= BOARD_SIZE:
                    if (adj_x, adj_y) in self.goats and (jump_x, jump_y) not in self.tigers and (jump_x, jump_y) not in self.goats:
                        return -0.5  # Tigers can still jump/capture, game continues

        return 1  # No valid moves for tigers, goats win

    def clone(self):
        """ Return a deep copy of the current game state """
        return State(self.tigers.copy(), self.goats.copy(), self.empty_positions.copy(), self.remaining_goat_number)

