## space invaders!

## steps to make the game:
# 0. get Pygame running
# 2. implement logic to render drawings
# 3. implement logic to move them (player)
# 4. implement enemy movement
# 5. implement enemy AI (attacking player)

import sys
import pygame
from enum import Enum

class Colour(Enum):
    WHITE = (255,255,255)
    BLACK = (0,0,0)



class player:
    def __init__(self, game):
        self.game = game
        self.xpos = 200
        self.ypos = 200
        self.width = 60
        self.height = 40 
        self.model = [0,0,0,1,0,0,0,
                      0,0,1,1,1,0,0,
                      1,1,1,1,1,1,1]

    def draw(self):
        start_y = self.ypos
        for row in range(3):
            start_x = self.xpos
            for column in range(7):
                if self.model[7*row+column] == 1:
                    pygame.draw.rect(self.game.screen, (255,255,255), (start_x, start_y, 10, 10))
                start_x += 10

            # go column lower
            start_y += 10


class game:
    def __init__(self):
        pygame.init()
        size = width, height = 600, 800
        self.screen = pygame.display.set_mode(size)
        self.player = player(self)

    def run(self):
        while True:
            self.check_events()
            self.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def draw(self):
        self.screen.fill((0,0,0)) # black background
        self.player.draw()
        pygame.display.update()



if __name__ == '__main__':
    g = game()
    g.run()
