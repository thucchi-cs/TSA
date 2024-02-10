# Files import
import asyncio
import pygame, os
import random

# Available images
logs_images = [
    pygame.image.load(os.path.join('GameGraphics', 'LogTEST1.png')),
    pygame.image.load(os.path.join('GameGraphics', 'LogTEST2.png')),
    pygame.image.load(os.path.join('GameGraphics', 'LogTEST3.png'))]

# Lanes of logs
class lanes():
    def __init__(self, number, surface, y):
        global logs_images
        self.surface = surface
        self.number = number    #higher number = more recent on top
        self.speed = random.randint(2, 4)    #random speed of logs
        self.direction = random.choice([1, -1])    #random direction (left or right)
        self.size = random.randint(2, 3)    #random size (medium or large
        self.y = y    #vertical position of lane
        # Set-up by size
        # medium
        if self.size == 2:
            self.space_choices = [3, 80, 80]    #space in between logs
            self.log_image = logs_images[1]    #correct image
            self.length = 156    #correct size
        # large
        else:
            self.space_choices = [3, 80, 80]    #space in between logs
            self.log_image = logs_images[2]    #correct image
            self.length = 234    #correct size
        # Create logs for this lane
        self.logs = pygame.sprite.Group()    #all log sprites of this lane group
        self.logs_number = 0    #number of logs existing
        self.space = random.choice(self.space_choices)    #space in between  is random
        # Generate first few logs
        # going to the left
        if self.direction == -1:
            self.logs.add(self.log(self, 1000))    #add very right log to sprite group
            # create logs until screen is filled
            while self.logs.sprites()[-1].rect.x > 0:
                position = self.logs.sprites()[-1].rect.x - (self.space + self.length)    #spacing logs out
                self.logs.add(self.log(self, position))    #add log
                self.logs_number += 1    #update number of logs
                self.space = random.choice(self.space_choices)    #choose space for next log
            snap_pos = [-20, 58, 136, 214, 292, 370, 448, 526, 604, 682, 760, 838, 916]    #allowed spots for player to snap to
        # going to the right
        else:
            self.logs.add(self.log(self, -self.length))    #add very left log
            # create logs until screen is filled
            while self.logs.sprites()[-1].rect.x < 1000:
                position = self.logs.sprites()[-1].rect.x + (self.space + self.length)    #spacing logs out
                self.logs.add(self.log(self, position))    #add log
                self.logs_number += 1    #update number of logs
                self.space = random.choice(self.space_choices)    #choose spacing for next log
            snap_pos = [936, 858, 780, 702, 624, 546, 468, 390, 312, 234, 156, 78, 0]    #allowed spots for player to snape to
        # Snap points
        self.snap_points = []
        for item in snap_pos:
            self.snap_points.append(self.snaps(self, item))

    # Add logs as needed
    def show(self):
        # don't add if lane no longer on screen
        if self.y >= 600:
            self.logs.empty()
        # if lane is still on screen
        else:
            self.logs.update()    #update all logs' positions
            self.logs.draw(self.surface)
            # Check if more logs are needed
            # going to the left
            if self.direction == -1:
                # if next log is ready to be created
                if self.logs.sprites()[-1].rect.x <= 1000 - (self.space + self.length):
                    self.logs.add(self.log(self, 1000))    #create log
                    self.logs_number += 1    #update number of log
                    self.space = random.choice(self.space_choices)    #choose spacing for next log
                # Create more snap points
                if self.snap_points[-1].x <= 922:
                    self.snap_points.append(self.snaps(self, 1000))
            # going the the right
            else:
                # if next log is ready to be created
                if self.logs.sprites()[-1].rect.x >= self.space:
                    self.logs.add(self.log(self, -self.length))    #create log
                    self.logs_number += 1    # update number of log
                    self.space = random.choice(self.space_choices)    #choose spacing for next log
                # Create more snap points
                if self.snap_points[-1].x >= 0:
                    self.snap_points.append(self.snaps(self, -78))
            # Move snap points along with logs
            for item in self.snap_points:
                item.move()

    # Log sprite
    class log(pygame.sprite.Sprite):
        def __init__(self, attr, x):
            super().__init__()
            self.attr = attr    #inherit attr of lanes
            self.image = self.attr.log_image    #image for sprite
            self.rect = self.image.get_rect()
            self.rect.y = self.attr.y
            self.rect.x = x

        # Log's flow movement with river
        def update(self):
            self.rect.y = self.attr.y
            self.rect.x += self.attr.direction * self.attr.speed

    # Snap points for player
    class snaps():
        def __init__(self, attr, x):
            self.attr = attr   #inherit all attr of lanes
            self.x = x
            self.y = self.attr.y - 95
            self.point = (self.x, self.y)

        # Flow with logs
        def move(self):
            self.x += self.attr.direction * self.attr.speed
            self.y += 4
            self.point = (self.x, self.y)


class sandyLand(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.image = pygame.image.load(os.path.join('GameGraphics', 'LandTEST.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -641
    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))