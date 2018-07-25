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


class enemy:
    def __init__(self, game, xpos, ypos):
        self.game = game
        self.xpos = xpos
        self.ypos = ypos
        self.model = [0,0,1,0,0,0,0,0,1,0,0,
                      0,0,0,1,0,0,0,1,0,0,0,
                      0,0,1,1,1,1,1,1,1,0,0,
                      0,1,1,0,1,1,1,0,1,1,0,
                      1,1,1,1,1,1,1,1,1,1,1,
                      1,0,1,0,0,0,0,0,1,0,1,
                      1,0,1,0,0,0,0,0,1,0,1,
                      0,0,0,1,1,0,1,1,0,0,0]

    def draw(self):
        start_y = self.ypos
        for row in range(8):
            start_x = self.xpos
            for column in range(11):
                if self.model[11*row+column] == 1:
                    pygame.draw.rect(self.game.screen, (0,255,0), (start_x, start_y, 10, 10))
                start_x += 10
            # go column lower
            start_y += 10



class laser:
    def __init__(self, game, xpos, ypos):
        self.game = game
        self.xpos = xpos
        self.ypos = ypos
        self.height = 40 
        self.width = 5

    def draw(self):
        pygame.draw.rect(self.game.screen, (0,0,255), (self.xpos, self.ypos, self.width, self.height))

    def update(self):
        self.ypos -= 2 


class player:
    def __init__(self, game):
        self.game = game
        self.xpos = 200
        self.ypos = self.game.size[1] - 100 
        self.width = 60
        self.height = 40 
        self.model = [0,0,0,1,0,0,0,
                      0,1,1,1,1,1,0,
                      1,1,1,1,1,1,1]

    def draw(self):
        start_y = self.ypos
        for row in range(3):
            start_x = self.xpos
            for column in range(7):
                if self.model[7*row+column] == 1:
                    pygame.draw.rect(self.game.screen, (0,255,0), (start_x, start_y, 10, 10))
                start_x += 10

            # go column lower
            start_y += 10

    def move_left(self):
        if self.xpos > 0:
            self.xpos -= 1


    def move_right(self):
        if self.xpos + self.width < self.game.size[0]:
            self.xpos += 1


class game:
    def __init__(self):
        pygame.init()
        self.size = width, height = 1000, 800 
        self.screen = pygame.display.set_mode(self.size)
        self.player = player(self)
        self.player_lasers = []
        self.enemies = [enemy(self, 200, 200)]

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.cleanup()
        
    def cleanup(self):
        # check which elements we can remove from memory
        self.player_lasers = list(filter(lambda l: l.ypos > 0, self.player_lasers))


    def check_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_lasers.append(laser(self, self.player.xpos + self.player.width / 2,
                        self.player.ypos - 40))

    def update(self):
        for laser in self.player_lasers:
            laser.update()

    def draw(self):
        self.screen.fill((0,0,0)) # black background
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        for laser in self.player_lasers:
            laser.draw()
        pygame.display.update()



if __name__ == '__main__':
    g = game()
    g.run()
