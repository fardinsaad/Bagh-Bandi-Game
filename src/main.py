import pygame
import sys
from game import Game
from constants import WINDOW_SIZE

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Bagh Bandi Game')
    game = Game(screen)
    game.run()
    sys.exit()

if __name__ == '__main__':
    main()
