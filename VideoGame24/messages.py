import asyncio
import pygame, os

messageboard = [
    pygame.image.load(os.path.join('GameGraphics', 'IntroText1.png')),
    pygame.image.load(os.path.join('GameGraphics', 'IntroText2.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Level1Text1.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Level1Text2.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Level2Text1.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Level2Text2.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Level3Text1.png')),
    pygame.image.load(os.path.join('GameGraphics', 'Level3Text2.png')),]


class message(pygame.sprite.Sprite):
    def __init__(self, n):
        super().__init__()
        global messageboard
        self.n = n
        self.image = messageboard[n]
        if n != 1:
            self.image = pygame.transform.scale(messageboard[n], (100, 53))
            self.scaleFactor = 0.125
        else:
            self.scaleFactor = 1
        self.rect = self.image.get_rect()
        self.rect.center = (500, 300)
        self.zIn = False
        self.zOut = False
    def zoomIn(self):
        self.scaleFactor += 0.025
        width = int(900 * self.scaleFactor)
        height = int(480 * self.scaleFactor)
        self.image = pygame.transform.scale(messageboard[self.n], (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (500, 300)
        if self.scaleFactor >= 1:
            self.zIn = False
            self.image = messageboard[self.n]
            self.rect.center = (500, 300)
    def zoomOut(self):
        self.scaleFactor -= 0.025
        width = int(900 * self.scaleFactor)
        height = int(480 * self.scaleFactor)
        self.image = pygame.transform.scale(messageboard[self.n], (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (500, 300)


class wantedSign(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('GameGraphics', 'WantedSign.png'))
        self.rect = self.image.get_rect()
        self.rect.x = -411
        self.rect.y = 50
    def slide(self):
        if self.rect.x < 1005:
            self.rect.x += 4

class bigGuards(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('GameGraphics', 'ManyGuardsTEST.png'))
        self.rect = self.image.get_rect()
        self.rect.x = -350
        self.rect.y = 350
    def update(self):
        if self.rect.x < 1007:
            self.rect.x += 7
