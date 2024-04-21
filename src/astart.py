import random
class ASTAR:
    def determine_goat_move( board, tigers, goats, empty_positions):
            new_goat_position = random.choice(empty_positions)
            return new_goat_position