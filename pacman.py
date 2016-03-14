import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')

mapping = open("./map","r")
loading = list((mapping.read()).split("\n"))
map = [x.split(" ") for x in loading]
num_pechen = 0
for i in range(len(map)):
        num_pechen += map[i].count("+")

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
            if type != "." and type != "+" and type != "^":
                map[int(m)][int(k)] = "0"
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self,num):
        self.number = num
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 8.0 / 10.0

    def game_tick(self,num):
        type = "@"
        self.lx = self.x
        self.ly = self.y
        super(Ghost, self).game_tick(num)
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        if map[int(self.x)][int(self.y)] == '*':
            sys.exit(0)
        self.set_coord(self.x, self.y,type,self.lx,self.ly)

class GhostS(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 3.0 / 10.0
    def game_tick(self,num):
        type = "@"
        self.lx = self.x
        self.ly = self.y
        super(GhostS, self).game_tick(num)
        if (max(self.x - pacman.x,pacman.x - self.x)+max(self.y - pacman.y,pacman.y - self.y))<= 8 and self.not_wall(self.x,self.y,pacman.x,pacman.y):
            print("yes")
            if max(self.x - pacman.x,pacman.x - self.x) >= max(self.y - pacman.y,pacman.y - self.y):
                if self.x > pacman.x:
                    self.direction = 3
                else:
                    self.direction = 1
            else:
                if self.y > pacman.y:
                    self.direction = 4
                else:
                    self.direction = 2
        else:
            if self.tick % 20 == 0 or self.direction == 0:
                self.direction = random.randint(1, 4)
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        if map[int(self.x)][int(self.y)] == '*':
            sys.exit(0)
        self.set_coord(self.x, self.y,type,self.lx,self.ly)
    def not_wall(self,x,y,xc,yc):
        if max(x-xc,xc-x) >= max(y-yc,yc-y):
            for i in range(int(min(x,xc)+1),int(max(x,xc))):
                for j in range(int(min(y,yc)),int(max(y,yc)+1)):
                    print(map[i][j])
                    if map[i][j] != ".":
                        break
                else:
                    return False
            else:
                return True
        else:
            for i in range(int(min(y,yc)+1),int(max(y,yc))):
                for j in range(int(min(x,xc)),int(max(x,xc)+1)):
                    print(map[j][i])
                    if map[j][i] != ".":
                        break
                else:
                    return False
            else:
                return True

class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0

    def game_tick(self,num):
        self.type = "*"
        self.lx = self.x
        self.ly = self.y
        super(Pacman, self).game_tick(num)
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1

        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
        if map[int(self.x)][int(self.y)] == '.':
                self.x = self.lx
                self.y = self.ly
        if map[int(self.x)][int(self.y)] == '@':
            sys.exit(0)
        self.set_coord(self.x, self.y,self.type,self.lx,self.ly)

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0

    def game_tick(self):
        self.type = "."
        super(Wall, self).game_tick(num)

class Pechen(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/food.bmp', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0
    def game_tick(self,num):
        self.type = "+"
        self.number = num
        super(Pechen, self).game_tick(num)
        if map[int(self.x)][int(self.y)] == "*":
            self.idie(self.type,self.x,self.y,self.number)
    def idie(self,type,x,y,num):
        map[x][y] = "0"
        pechenky[num] = None

class Pechenextra(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/food.bmp', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 0
    def game_tick(self,num):
        self.type = "+"
        self.number = num
        super(Pechenextra, self).game_tick(num)
        if map[int(self.x)][int(self.y)] == "*":
            self.idie(self.type,self.x,self.y,self.number)
    def idie(self,type,x,y,num):
        map[x][y] = "0"
        pechenky[num] = None
        Pacman.velocity = 0.7

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
    screen = pygame.display.get_surface()
    ghost = Ghost(9, 9, tile_size, map_size)
    ghosts = GhostS(8, 5, tile_size, map_size)
    pacman = Pacman(0, 0, tile_size, map_size)
    Pacman.velocity = 0.4
    pechenky = [None for i in range(10)]
    walls = [None for i in range(16*16)]
    n = 0
    np = 0
    num_pechen = 0
    for m in range(len(map)):
        for k in range(len(map[m])):
            if map[m][k] == '.':
                n += 1
                x = Wall(m, k, tile_size, map_size)
                walls[n] = x
            elif map[m][k] == '+':
                np += 1
                x = Pechen(m,k, tile_size, map_size)
                pechenky[np] = x
            elif map[m][k] == '^':
                np += 1
                x = Pechenextra(m,k, tile_size, map_size)
                pechenky[np] = x
    background = pygame.image.load("./resources/background.png")

    while 1:
        i = len(pechenky) - 1
        while pechenky[i] == None and i >= 0:
            i -= 1
            if pechenky[i] != None:
                break
        else:
            sys.exit(0)
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick(0)
        ghosts.game_tick(0)
        pacman.game_tick(0)
        draw_background(screen, background)
        pacman.draw(screen)
        ghost.draw(screen)
        ghosts.draw(screen)
        for i in range(len(walls)):
            if walls[i]:
                walls[i].draw(screen)
        for i in range(len(pechenky)):
            if pechenky[i]:
                pechenky[i].draw(screen)
                pechenky[i].game_tick(i)
        pygame.display.update()
