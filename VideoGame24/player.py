# Libraries import
import asyncio
import pygame, os

# Extra graphics
panic = pygame.image.load(os.path.join('GameGraphics', 'panicTEST.png'))

# Goldilocks sprite
class player(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.imageStill = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_right.png'))
        self.imagesRunning = [pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_running1TEST.png')), pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_running2TEST.png'))]
        self.imageCelebrate = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_Celebrate2.png'))
        self.image = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_front.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400
        self.speed = 5
        self.steps = 0
        self.run = False
        self.gravity = 1
        self.jump_height = 17
        self.velocity = self.jump_height
        self.jumping = False
    def move0(self, key):
        if key[pygame.K_RIGHT] and self.rect.x < 1000:
            self.rect.x += self.speed
            self.run = True
        else:
            self.run = False

        if self.steps >= 12:
            self.steps = 0

        if self.run:
            self.image = self.imagesRunning[self.steps // 6]
            self.steps += 1
        else:
            self.image = self.imageStill
            self.steps = 0
    def celebration(self, counter):
        self.image = self.imageCelebrate
        if self.jumping:
            self.rect.y -= self.velocity
            self.velocity -= self.gravity
            if self.velocity < (-self.jump_height):
                self.velocity = self.jump_height
                self.jumping = False
                return 1
        else:
            if counter % 20 == 0:
                self.jumping = True
        return counter

    # Set-up for level 1 (Crossy Road)
    def lvl1__init__(self, lane):
        self.negatives = 0    #keep track when moving down from current score
        self.width = 73
        self.height = 123
        #costumes/images
        self.imagesNormal = [pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_front.png')), pygame.image.load(os.path.join('GameGraphics','Goldilocks_back.png')), pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_left.png')), pygame.image.load(os.path.join('GameGraphics','Goldilocks_right.png'))]
        for i in range(len(self.imagesNormal)):
            self.imagesNormal[i] = pygame.transform.scale(self.imagesNormal[i], (73, 123))
        self.imageLose = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_lose.png'))
        self.jumpsize = 10    #how much player squish down when a key is held down
        self.imagesJump = [None] * len(self.imagesNormal)
        for i in range(len(self.imagesNormal)):    #make normal images squish down before jumps
            self.imagesJump[i] = pygame.transform.scale(self.imagesNormal[i], (self.width, self.height - self.jumpsize))
        self.image = self.imagesNormal[0]    #current image
        self.rect = self.image.get_rect()    #sprite rect
        self.rect.x = 470
        self.rect.y = 200
        self.lane = 3    #current lane player is on
        self.moveUP, self.moveDOWN, self.moveLEFT, self.moveRIGHT = False, False, False, False
        self.lose = False
        #snap to closest spot
        self.snap1(lane)
        # Make sure player start on a log
        self.detect_logs(lane)  #check position
        if self.lose:    #if not on a log
            self.rect.y -= 54    #reverse what detect_logs() have set
            # move to a log
            self.moveLEFT = True
            self.move1(lane, 0, 0)
            self.lose = False
            self.image = self.imagesNormal[0]

    # Squish down before a jump
    def beforemove1(self,event):
        # Get key then changes costumes
        if event.key == pygame.K_UP:
            self.moveUP = True
            self.image = self.imagesJump[1]
        elif event.key == pygame.K_DOWN:
            self.moveDOWN = True
            self.image = self.imagesJump[0]
        elif event.key == pygame.K_LEFT:
            self.moveLEFT = True
            self.image = self.imagesJump[2]
        elif event.key == pygame.K_RIGHT:
            self.moveRIGHT = True
            self.image = self.imagesJump[3]
        self.rect.y += self.jumpsize #move down bc height is shorter

    # Move when key is pressed then released
    def move1(self, lane, score, counter):
        # Cannot go pass the borders
        borderL = 50
        borderR = 900
        borderT = 20
        borderB = 400
        # Movement limits
        movex = 78
        movey = 85
        # Check if requested movement is allowed
        # move up
        if self.moveUP and self.rect.y > borderT:
            self.rect.y -= movey
            self.image = self.imagesNormal[1]    #update current image to back
            self.lane += 1    #update current lane player is on
            #update score
            if self.negatives > 0:
                self.negatives -= 1
            else:
                score += 1
        # move down
        elif self.moveDOWN and self.rect.y < borderB:
            self.rect.y += movey
            self.image = self.imagesNormal[0]    #update current image to front
            self.lane -= 1    #update current lane player is on
            #update score
            self.negatives += 1
        # move left
        elif self.moveLEFT and self.rect.x > borderL:
            self.rect.x -= movex
            self.image = self.imagesNormal[2]    #update current image to facing left
        # move right
        elif self.moveRIGHT and self.rect.x < borderR:
            self.rect.x += movex
            self.image = self.imagesNormal[3]    #update current image to facing right
        # Reset
        self.moveUP, self.moveDOWN, self.moveLEFT, self.moveRIGHT = False, False, False, False
        self.rect.y -= self.jumpsize    #move back up bc size is now big again
        if self.lane < len(lane):
            # Snap to correct and allowed spot
            self.snap1(lane)
            self.detect_logs(lane)
        # Update score
        return score

    # Moving along the current lane the player is on
    def flow1(self, lane):
        self.rect.x += lane.direction * lane.speed    #move with speed and direction of lane

        # Check if player goes over the edge
        # right edge
        if self.rect.x > 990:
            self.current = pygame.transform.rotate(self.imageLose, 60)    #lose image
            self.surface.blit(self.current, (920, self.rect.y))
            panic_temp = pygame.transform.rotate(panic, 90)
            self.surface.blit(panic_temp, (730, self.rect.y - 50))    #exclamation marks
            self.lose = True    #update lose status
        # left edge
        elif self.rect.x < -65:
            self.current = pygame.transform.rotate(self.imageLose, 300)    #lose image
            self.surface.blit(self.current, (-15, self.rect.y))
            panic_temp = pygame.transform.rotate(panic, 270)
            self.surface.blit(panic_temp, (100, self.rect.y - 50))    #exclamation marks
            self.lose = True    #update lose status
        #bottom edge
        if self.rect.y > 590:
            self.current = self.imageLose    #lose image
            self.surface.blit(self.current, (self.rect.x, 533))
            self.surface.blit(panic, (self.rect.x - 50, 390))    #exclamation marks
            self.lose = True    #update lose statues

    #Snap to right spots
    def snap1(self, lane):
        min_distance = float('inf')
        closest_point = None
        # Check for closest available spots
        for item in lane[self.lane].snap_points:
            distance = pygame.math.Vector2(item.point[0] - self.rect.x, item.point[1] - self.rect.y).length()
            if distance < min_distance:
                min_distance = distance
                closest_point = item.point
        # Snap to point
        if closest_point:
            self.rect.x, self.rect.y = closest_point

    # Check if player is on a log or in the water
    def detect_logs(self, lane):
        self.lose = True
        for sprite in lane[self.lane].logs:
            if pygame.sprite.collide_mask(sprite, self):
                self.lose = False
                break
        if self.lose:
            self.image = self.imageLose
            self.rect.y += 56


    # Level 2
    def lvl2__init__(self):
        self.imagesRunning = [pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_running1TEST.png')), pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_running2TEST.png'))]
        self.imageJump2 = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_runningJumpTEST.png'))
        self.imageLose = pygame.image.load(os.path.join('GameGraphics', 'panicTESTsmall.png'))
        self.image = self.imagesRunning[0]
        self.imageCurrentIndex = 0
        self.imageNextIndex = 1
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 323

        self.jumping = False
        self.gravity = 1
        self.jump_height = 17
        self.velocity = self.jump_height

    def run2(self, counter):
        if self.jumping:
            self.image = self.imageJump2
            self.jump2()
        else:
            if counter % 6 == 0:
                self.imageCurrentIndex += self.imageNextIndex
                self.image = self.imagesRunning[self.imageCurrentIndex]
                self.imageNextIndex *= -1
    def jump2(self):
        self.rect.y -= self.velocity
        self.velocity -= self.gravity
        if self.velocity < (-self.jump_height):
            self.velocity = self.jump_height
            self.image = self.imagesRunning[0]
            self.imageCurrentIndex = 0
            self.imageNextIndex = 1
            self.jumping = False

    def check_collision2(self, spike):
        if pygame.sprite.collide_mask(self, spike):
            self.surface.blit(self.imageLose, (self.rect.x, self.rect.y + 76))
            self.surface.blit(self.imageLose, (self.rect.x + 75, self.rect.y))
            return True
        return False


    def lvl3__init__(self):
        self.imageStill = pygame.transform.scale(pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_right.png')), (67, 114))
        self.imageFreeze = pygame.transform.scale(pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_runningFreeze.png')), (67, 114))
        for i in range(len(self.imagesRunning)):
            self.imagesRunning[i] = pygame.transform.scale(self.imagesRunning[i], (67, 114))
        self.image = self.imageStill
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 300
        self.speed = 7
        self.steps = 0
        self.runx = False
        self.runy = False
        self.left = False
        self.borderright = 930

    def move3(self, key, counter, speed):
        if key[pygame.K_RIGHT] and self.rect.x < self.borderright:
            self.rect.x += self.speed
            self.runx = True
        elif key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.left = True
            self.runx = True
        else:
            self.runx = False
            self.left = False
        if key[pygame.K_UP] and self.rect.y > 115:
            self.rect.y -= self.speed
            self.runy = True
        elif key[pygame.K_DOWN] and self.rect.y < 434:
            self.rect.y += self.speed
            self.runy = True
        else:
            self.runy = False
        self.animation3(speed)

    def animation3(self, speed):
        if self.steps >= 10:
            self.steps = 0
        if self.runx or self.runy:
            if self.left:
                self.image = pygame.transform.flip(self.imagesRunning[self.steps//5], True, False)
            else:
                self.image = self.imagesRunning[self.steps//5]
            self.steps += 1
        else:
            self.image = self.imageStill
            self.rect.x -= speed

    def check_collision3(self, guard):
        if pygame.sprite.collide_mask(self, guard):
            self.image = self.imageFreeze
            self.surface.blit(self.imageLose, (self.rect.x, self.rect.y + 76))
            self.surface.blit(self.imageLose, (self.rect.x + 75, self.rect.y))
            return True
        return False

    def resize3(self):
        self.imageStill = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_right.png'))
        self.imageFreeze = pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_runningFreeze.png'))
        self.imagesRunning = [pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_running1TEST.png')),
                              pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_running2TEST.png'))]
