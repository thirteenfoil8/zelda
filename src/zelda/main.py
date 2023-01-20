import pygame
import sys
from zelda.config.settings import WINDOW_HEIGHT, WINDOW_WIDTH, FRAMERATE
from zelda.level.level import Level


class Game:
    def __init__(self):
        # setup
		
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Naruto Shippuden Ultimate Ninja Storm 8')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # game logic
            self.display_surface.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()
