# Libraries import
import asyncio
import pygame
import os

# Key Shards Sprite
class key_shard(pygame.sprite.Sprite):
    def __init__(self, lvl, surface):
        super().__init__()
        self.level = lvl - 1
        self.surface = surface
        self.shards = [
            pygame.image.load(os.path.join('GameGraphics', 'KeyShard1.png')),
            pygame.image.load(os.path.join('GameGraphics', 'KeyShard2.png')),
            pygame.image.load(os.path.join('GameGraphics', 'KeyShard3.png'))]
        self.bigWidth, self.bigHeight = 240, 312
        if lvl == 4:
            self.image = pygame.image.load(os.path.join('GameGraphics', 'KeyWhole.png'))
            self.rect = self.image.get_rect()
            self.rect.x = 539
            self.rect.y = 396

    # Re innitialize
    def restart(self):
        self.image = pygame.transform.scale_by(self.shards[self.level], 8)
        self.scaleFactor = 1
        self.rect = self.image.get_rect()
        self.rect.y = 30
        if self.level == 0:
            self.targetx = 780
        elif self.level == 1:
            self.targetx = 836
        else:
            self.targetx = 895
        self.rect.x = self.targetx - 240

    def animation(self):
        self.rect.x += 9
        self.scaleFactor -= 0.03
        width = int(self.bigWidth * self.scaleFactor)
        height = int(self.bigHeight * self.scaleFactor)
        self.image = pygame.transform.scale(self.image, (width, height))
        if self.scaleFactor <= 0.2:
            self.image = self.shards[self.level]

    def win_animation1(self):
        self.rect.y += 6
        self.rect.x -= 4
        pass
    # y = 426 --> 396
    #x =  --> 605

    def win_animation2(self):
        self.rect.x += 5
        self.rect.y -= 9