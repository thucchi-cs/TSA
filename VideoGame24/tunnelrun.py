# Libraries import
import asyncio
import pygame
import os
import random

spikes_images = [
    pygame.image.load(os.path.join('GameGraphics', 'Spikes1TEST.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Spikes2TEST.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Spikes3TEST.png')),
]

class spikes(pygame.sprite.Sprite):
    def __init__(self, counter):
        super().__init__()
        global spikes_images
        self.number = counter
        self.score = 0
        self.space = random.randint(400, 700)
        self.size = random.randint(0, 2)
        if counter >= 1000:
            self.direction = random.choice([1, 1, 1, 1,1 ,1 ,1 ,1, -1])
        else:
            self.direction = 1
        self.image = spikes_images[self.size]
        if self.direction == -1:
            self.image = pygame.transform.rotate(pygame.transform.scale_by(self.image, 1.5), 180)
            self.space //= random.uniform(1, 2)
        self.rect = self.image.get_rect()
        if self.size == 0:
            self.length = 66
        elif self.size == 0:
            self.length = 110
        else:
            self.length = 120
        self.rect.x = 1000
        if self.direction == 1:
            self.rect.y = 355
        else:
            self.rect.y = 140

    def update(self, speed):
        self.rect.x -= speed
        self.scoring()

    def add_new(self):
        if self.rect.x <= 1000 - self.space:
            return True
        return False

    def scoring(self):
        if self.rect.x <= 100 - self.length:
            self.score += 1

class tunnel_exit(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = pygame.image.load(os.path.join('GameGraphics', 'TunnelExitTEST.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 1001
        self.rect.y = 0
        self.surface = surface

    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

