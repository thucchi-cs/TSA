import asyncio
import pygame, os
import random

images = [pygame.image.load(os.path.join('GameGraphics', 'Guard1TEST.png')),
          pygame.image.load(os.path.join('GameGraphics', 'Guard2TEST.png')),
          pygame.image.load(os.path.join('GameGraphics', 'Guard3TEST.png'))]

class guard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global images
        size = random.randint(0, 2)
        self.image = images[size]
        self.rect = self.image.get_rect()
        if size == 0:
            self.length = 34
        elif size == 1:
            self.length = 81
        else:
            self.length = 131

        self.xspeed = random.randint(6, 10)
        self.yspeed = random.randint(3, 12)
        self.rect.x = 1000
        self.rect.y = random.randint(115, 430)
        self.upperlimit = 115
        self.lowerlimit = 430
        if self.rect.y > 333:
            self.direction = 1
        else:
            self.direction = -1

    def update(self):
        self.rect.x -= self.xspeed
        if (self.direction == 1 and self.rect.y >= self.upperlimit + self.yspeed) or (self.direction == -1 and self.rect.y <= self.lowerlimit - self.yspeed):
            self.rect.y -= self.direction * self.yspeed
        else:
            self.xspeed = random.randint(6, 10)
            self.yspeed = random.randint(3, 12)
            self.direction *= -1

class door(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.image = pygame.image.load(os.path.join('GameGraphics', 'HallwayExitTEST.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 1001
        self.rect.y = 0
    def update(self, speed):
        self.rect.x -= speed
    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

class marks(pygame.sprite.Sprite):
    def __init__(self, n, x):
        super().__init__()
        self.images = [
            pygame.image.load(os.path.join('GameGraphics', 'MarksTEST.png')),
            pygame.image.load(os.path.join('GameGraphics', 'Marks2TEST.png'))]
        self.image = self.images[n]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
    def update(self, speed):
        if self.rect.x >= -613:
            self.rect.x -= speed
        else:
            self.rect.x = 1000