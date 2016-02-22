import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')

mapping = open("/home/student/zainullinr1-master/pacman-master/map","r")
loading = list((mapping.read()).split("\n"))
map = [x.split(" ") for x in loading]

def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))

class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y,type,x-1,y-1)

    def set_coord(self, x, y,type,m,k):
        self.x = x
        self.y = y
        if map[int(x)][int(y)] != ".":
            map[int(x)][int(y)] = type
            map[int(m)][int(k)] = "0"
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        type = "@"
        self.lx = self.x
        self.ly = self.y
        super(Ghost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        self.set_coord(self.x, self.y,type,self.lx,self.ly)


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        type = "*"
        self.lx = self.x
        self.ly = self.y
        super(Pacman, self).game_tick()
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1

            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
            if map[int(self.x)][int(self.y)] == '@':
                print("You looser")

        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
            if map[int(self.x)][int(self.y)] == '@':
                print("You looser")
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
            if map[int(self.x)][int(self.y)] == '@':
                print("You looser")
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
            if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
            if map[int(self.x)][int(self.y)] == '@':
                print("You looser")
        self.set_coord(self.x, self.y,type,self.lx,self.ly)
    def eating(self):
        #if map[self.x][self.y] == '+':
            #pacman.velocity  = 8.0 / 10.0

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0

    def game_tick(self):
        super(walls, self).game_tick()
        self.set_coord(self.x, self.y)

class pechen(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/food.bmp', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0
    def game_tick(self):
        super(pechenky, self).game_tick()
        self.set_coord(self.x, self.y)

def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0


if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16
    num_pechenky = int(random() * 10)
    pechenky = [None for i in range(num_pechenky)]
    screen = pygame.display.get_surface()
    ghost = Ghost(8, 8, tile_size, map_size)
    pacman = Pacman(6, 6, tile_size, map_size)
    walls = [None for i in range(16*16)]
    n = 0
    for k in range(num_pechenky):
        x = int(random()*15)
        y = int(random()*15)
        map[x][y] = '+'
        pechenky[k] = pechen(x, y, tile_size, map_size)
    for m in range(len(map)):
        for k in range(len(map[m])):
            if map[m][k] == '.':
                n += 1
                print(m,k)
                x = Wall(m, k, tile_size, map_size)
                walls[n] = x
    background = pygame.image.load("./resources/background.png")

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick()
        pacman.game_tick()
        draw_background(screen, background)
        pacman.draw(screen)
        ghost.draw(screen)
        for x in walls:
            if x:
                x.draw(screen)
        for y in pechenky:
            y.draw(screen)
        pygame.display.update()