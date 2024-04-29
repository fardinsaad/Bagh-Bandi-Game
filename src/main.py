import pygame
import sys
from game import Game
from constants import WINDOW_SIZE


def main():
    algorithm = sys.argv[1].lower()
    print(algorithm)
    if algorithm not in ["random", "bfs", "dfs", "monte_carlo", "astar"]:
        sys.exit("Invalid Algorithm specified, Valid Options: random, bfs, dfs, astar, monte_carlo")
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Bagh Bandi Game')
    game = Game(screen, algorithm)
    game.run()
    sys.exit()


if __name__ == '__main__':
    main()
