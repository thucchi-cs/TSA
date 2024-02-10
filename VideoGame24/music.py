import asyncio
import pygame
import os

water = pygame.mixer.Sound(os.path.join('Music', 'Splash.wav'))
water.set_volume(3)
key = pygame.mixer.Sound(os.path.join('Music', 'Collected.wav'))
key.set_volume(3)
lose = pygame.mixer.Sound(os.path.join('Music', 'Lose2.wav'))
lose.set_volume(0.3)
win = pygame.mixer.Sound(os.path.join('Music', 'Win.wav'))

success = pygame.mixer.Sound(os.path.join('Music', 'Yay.wav'))
celebrate = pygame.mixer.Sound(os.path.join('Music', 'Celebrate.wav'))
celebrate.set_volume(1.7)

def music_level():
    pause = pygame.mixer.music.get_pos() // 1000
    print(pause)
    pygame.mixer.music.load(os.path.join('Music', 'Piece 2.mp3'))
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1, fade_ms=3000)
    return pause

def music_transition(pause):
    pygame.mixer.music.load(os.path.join('Music', 'GARREG.mp3'))
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
    print(pygame.mixer.music.get_pos())
    pygame.mixer.music.set_pos(pause)
    print(pause)
    print(pygame.mixer.music.get_pos())

def switch(current):
    pass
    # songs = ['GARREG.mp3', 'Piece 2.mp3']
    # if not pygame.mixer.music.get_busy():
    #     if current == 0:
    #         current = 1
    #     else:
    #         current = 0
    #     pygame.mixer.music.load(os.path.join('Music', songs[current]))
    #     pygame.mixer.music.set_volume(0.7)
    #     pygame.mixer.music.play(loops = 0)
    # return current