import asyncio
import pygame, os
import random

logs_images = [
pygame.image.load(os.path.join('GameGraphics', 'LogTEST1.png')),
pygame.image.load(os.path.join('GameGraphics', 'LogTEST2.png')),
pygame.image.load(os.path.join('GameGraphics', 'LogTEST3.png'))]

class lanes(pygame.sprite.Sprite):
    def __init__(self, number, surface, y):
        super().__init__()
        global logs_images
        self.surface = surface
        self.number = number
        self.speed = random.uniform(1, 2.5)
        self.direction = random.choice([1, -1])
        self.size = random.randint(1, 3)
        self.y = y
        if self.size == 1:
            self.space_choices = [17, 17, 78]
            self.log_image = logs_images[0]
        elif self.size == 2:
            self.space_choices = [3, 3, 78]
            self.log_image = logs_images[1]
        else:
            self.space_choices = [3, 3, 78]
            self.log_image = logs_images[2]
        self.logs = pygame.sprite.Group()
        self.logs.add(self.log(self))
        self.logs_number = 0
        self.space = random.choice(self.space_choices)
    def show(self, counter):
            self.logs.update()
            if self.direction == -1:
                if self.logs.sprites()[-1].rect.x <= 1000 - (self.space + self.logs.sprites()[-1].size):
                    self.logs.add(self.log(self))
                    self.logs_number += 1
                    self.space = random.choice(self.space_choices)
            else:
                if self.logs.sprites()[-1].rect.x >= self.space:
                    self.logs.add(self.log(self))
                    self.logs_number += 1
                    self.space = random.choice(self.space_choices)
            self.logs.draw(self.surface)
            #for item in self.logs:
                #item.move()
    class log(pygame.sprite.Sprite):
        def __init__(self, attr):
            super().__init__()
            self.attr = attr
            self.image = self.attr.log_image
            self.rect = self.image.get_rect()
            self.rect.y = self.attr.y
            if self.attr.size == 1:
                self.size = 60
            elif self.attr.size == 2:
                self.size = 156
            else:
                self.size = 234
            if self.attr.direction == -1:
                self.rect.x = 1000
            else:
                self.rect.x = -self.size
        def update(self):
            self.rect.y = self.attr.y
            self.rect.x += self.attr.direction * self.attr.speed
