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
        self.pixel_size = 5 
        self.width = 11 * self.pixel_size # columns * pixel_size
        self.height = 8 * self.pixel_size # rows * pixel_size
        self.cycle = 0
        self.direction = -1 # -1 == left, 1 == right (todo: enumify?)
        self.model = [0,0,1,0,0,0,0,0,1,0,0,
                      0,0,0,1,0,0,0,1,0,0,0,
                      0,0,1,1,1,1,1,1,1,0,0,
                      0,1,1,0,1,1,1,0,1,1,0,
                      1,1,1,1,1,1,1,1,1,1,1,
                      1,0,1,0,0,0,0,0,1,0,1,
                      1,0,1,0,0,0,0,0,1,0,1,
                      0,0,0,1,1,0,1,1,0,0,0]

        self.model2 = [0,0,1,0,0,0,0,0,1,0,0,
                       1,0,0,1,0,0,0,1,0,0,1,
                       1,0,1,1,1,1,1,1,1,0,1,
                       1,1,1,0,1,1,1,0,1,1,1,
                       0,1,1,1,1,1,1,1,1,1,1,
                       0,0,1,1,1,1,1,1,1,0,0,
                       0,0,1,0,0,0,0,0,1,0,0,
                       0,1,0,0,0,0,0,0,0,1,0]
        self.draw_model = None


    def draw(self):
        start_y = self.ypos

        if self.cycle % 100 == 0:
            self.draw_model = self.model2 if self.draw_model == self.model else self.model

        self.cycle += 1
        for row in range(8):
            start_x = self.xpos
            for column in range(11):
                if self.draw_model[11*row+column] == 1:
                    pygame.draw.rect(self.game.screen, (0,255,0), (start_x, start_y, self.pixel_size,
                        self.pixel_size))
                start_x += self.pixel_size 
            # go column lower
            start_y += self.pixel_size

    def update(self):
        self.xpos += 1 * self.direction

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
        self.enemies = [] 
        self.i = 0

    def run(self):
        # set up the enemies
        for i in range(10):
            self.enemies.append(enemy(self, 80 + i * 80, 50))
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
        self.check_enemy_hits()
        for laser in self.player_lasers:
            laser.update()

        # Check if an enemy hits the left wall
        for enemy in self.enemies:
            enemy.update()
        left_wall_touching = len(list(filter(lambda enemy: enemy.xpos < 0, self.enemies)))
        right_wall_touching = len(list(filter(lambda enemy: enemy.xpos + enemy.width > self.size[0], self.enemies)))
        if left_wall_touching > 0 or right_wall_touching > 0:
            # change the direction and make them descend
            for enemy in self.enemies:
                enemy.ypos += 50
                enemy.direction *= -1

    def check_enemy_hits(self):
        print("checking hits " + str(self.i))
        self.i += 1
        dead_enemies = []
        destroyed_lasers = []
        if len(self.player_lasers) <= 0:
            return
        for enemy in self.enemies:
            for laser in self.player_lasers:
                laser_rect = pygame.Rect((laser.xpos, laser.ypos), (laser.width, laser.height))
                enemy_rect = pygame.Rect((enemy.xpos, enemy.ypos), (enemy.width, enemy.height))
                collision = pygame.Rect.colliderect(laser_rect, enemy_rect)
                if collision == True:
                    dead_enemies.append(enemy)
                    destroyed_lasers.append(laser)
        if len(dead_enemies) > 0:
            self.enemies = list(filter(lambda e: e not in dead_enemies, self.enemies))
            self.player_lasers = list(filter(lambda l: l not in destroyed_lasers,
                self.player_lasers))
        #self.player_lasers = surviving_lasers




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
