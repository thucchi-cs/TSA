# Libraries import
import asyncio
import pygame
import os
import sys, random, time

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load(os.path.join('Music', 'Piece 2 New.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Screen set-up
WIDTH, HEIGHT = 1000, 600
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Name of Game")
BACKGROUND = [
    pygame.image.load(os.path.join('GameGraphics', 'Water.jpg')),
    pygame.image.load(os.path.join('GameGraphics', 'TunnelTEST.png')),
    pygame.image.load(os.path.join('GameGraphics', 'HallwayTEST.png')),
    pygame.image.load(os.path.join('GameGraphics', 'IntroBackground.png')),
    pygame.image.load(os.path.join('GameGraphics', 'ForestRunningPath.png')),
    pygame.image.load(os.path.join('GameGraphics', 'ShoreLine.png')),
    pygame.image.load(os.path.join('GameGraphics', 'TunnelEntrance.png')),
    pygame.image.load(os.path.join('GameGraphics', 'HallwayEntrance.png')),
    pygame.image.load(os.path.join('GameGraphics', 'BigGateClosed.png')),
    pygame.image.load(os.path.join('GameGraphics', 'BigGateOpen.png'))]
# Background key:
# [0] Water lvl 1
# [1] Tunnel lvl 2
# [2] Hallway lvl 3
# [3] Intro background w/ houses
# [4] Forest w/ trees
# [5] Shore of river
# [6] Tunnel Entrance
# [7] Hallway Entrance
# [8] Big Gate Closed
# [9] Big Gate Open

# Files import
from crossyriver import*
from player import*
from keys import*
from tunnelrun import*
from hallway import*
from messages import*
import music

async def main():
    # Goldilocks (player)
    player_sprite = pygame.sprite.Group()
    goldilocks = player(SURFACE)
    player_sprite.add(goldilocks)

    # Key Shards
    keys = pygame.sprite.Group()
    k1 = key_shard(1, SURFACE)
    k2 = key_shard(2, SURFACE)
    k3 = key_shard(3, SURFACE)
    kw = key_shard(4, SURFACE)

    # levels
    run = True
    intro = True
    quit = False

    # FPS
    clock = pygame.time.Clock()
    FPS = 40
    counter = 0

    song = 0

    # main loop
    while True and not quit:

        counter = 0
        wanted = False
        explain = False
        after = False
        signN = 0
        intro_sprites = pygame.sprite.Group()
        sign1 = message(0)
        sign2 = message(1)
        poster = wantedSign()
        runningGuards = bigGuards()
        intro_sprites.add(poster)
        intro_sprites.add(runningGuards)

        while intro:
            clock.tick(FPS)
            counter += 1

            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    intro = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        intro = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign1.zIn = False
                        signN += 1
                        if signN == 1:
                            intro_sprites.add(sign2)
                            sign1.zOut = True
                        else:
                            sign2.zOut = True

            SURFACE.blit(BACKGROUND[3], (0, 0))

            runningGuards.update()
            if runningGuards.rect.x >= 430 and not wanted and not explain and not after:
                wanted = True
            if wanted:
                poster.slide()
                if poster.rect.x >= 1000:
                    explain = True
                    wanted = False
                    BACKGROUND[3] = pygame.transform.flip(BACKGROUND[3], True, False)
                    counter = 1
            if explain:
                if counter == 20:
                    intro_sprites.add(sign1)
                    sign1.zIn = True
                if sign1.zIn:
                    sign1.zoomIn()
                if sign1.zOut:
                    if sign1.scaleFactor > 0.05:
                        sign1.zoomOut()
                    else:
                        intro_sprites.remove(sign1)
                        sign1.zOut = False
                if sign2.zOut:
                    if sign2.scaleFactor > 0.05:
                        sign2.zoomOut()
                    else:
                        intro_sprites.remove(sign2)
                        sign2.zOut = False
                        explain = False
                        after = True
                player_sprite.draw(SURFACE)
            if after:
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                player_sprite.draw(SURFACE)
                if goldilocks.rect.x > 990:
                    intro = False
                    break

            intro_sprites.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        if quit:
            pass
            #break

        beforelvl1 = True
        counter = 0
        explain = False
        signN = 2
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        sign3 = message(2)
        goldilocks.rect.x = 0
        goldilocks.rect.y = 350

        while beforelvl1:
            clock.tick(FPS)
            counter += 1

            SURFACE.blit(BACKGROUND[5], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    beforelvl1 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        beforelvl1 = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign3.zIn = False
                        signN += 1
                        sign3.zOut = True

            if not explain:
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 580:
                    explain = True
                    intro_sprites.add(sign3)
                    sign3.zIn = True
            else:
                if sign3.zIn:
                    sign3.zoomIn()
                if sign3.zOut:
                    if sign3.scaleFactor > 0.05:
                        goldilocks.rect.x = -100
                        sign3.zoomOut()
                    else:
                        beforelvl1 = False
                        break
            player_sprite.draw(SURFACE)
            intro_sprites.draw(SURFACE)


            pygame.display.flip()
            await asyncio.sleep(0)

        if quit:
            pass
            #break

        #pygame.mixer.music.stop()  # 3000 milliseconds (3 seconds) fade-out

        # Load and play the second music track
        # pause = music.music_level()

        # Init lvl 1
        # Variables
        lvl1 = True
        lvl1_win = False
        lvl1_lose = False
        score = 0
        score_font = pygame.font.Font(None, 120)
        freeze = False
        lose_process = False
        key_collected = False
        counter = 0

        # Objects
        lane = []
        logs_y = [555, 470, 385, 300, 215, 130, 45, -40]
        for i in range(len(logs_y)):
            lane.append(lanes(i, SURFACE, logs_y[i]))
        lane_number = len(lane) - 1
        goldilocks.lvl1__init__(lane)

        # Winning land
        land = sandyLand(SURFACE)
        win_counter = 0

        # Lvl1 loop
        while lvl1 and not lvl1_win:
            # FPS
            clock.tick(FPS)
            counter += 1

            score_display = score_font.render(str(score), True, (255, 250, 250))

            song = music.switch(song)

            # Check for win-lose status
            if lvl1_win:
                lvl1 = False
                break
            elif lvl1_lose:
                # Reset game
                pygame.mixer.music.set_volume(0.5)
                if score >= 50:
                    keys.remove(k1)
                score = 0
                counter = 1
                lose_process = False
                for item in lane:
                    for sprite in item.logs:
                        sprite.kill()
                        item.logs.remove(sprite)
                lane.clear()
                for i in range(len(logs_y)):
                    lane.append(lanes(i, SURFACE, logs_y[i]))
                lane_number = len(lane) - 1
                goldilocks.lvl1__init__(lane)
                land.rect.y = -641
                freeze = False
                lvl1_lose = False
                key_collected = False

            # Check if first key shard is collected
            if score == 50 and not key_collected:
                key_collected = True
                keys.add(k1)
                k1.restart()
                music.key.play()

            # Get keys pressed
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    quit = True
                    lvl1 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        lvl1 = False
                        break

                    # Player bounce
                    else:
                        goldilocks.beforemove1(event)
                # Move player
                if event.type == pygame.KEYUP:
                    score = goldilocks.move1(lane, score, counter)

            # Movements
            if not freeze:
                # Blit background
                SURFACE.blit(BACKGROUND[0], (0, 0))

                # Move lanes down when still in screen
                for item in lane:
                    if item.y < 610:
                        item.y += 4
                    else:
                        if len(item.logs) > 0:
                            for sprite in item.logs:
                                sprite.kill()
                                item.logs.remove(sprite)

                # Show land when win game
                if counter >= 1082:
                    land.rect.y += 4
                # Move logs horizontally
                for item in lane:
                    if item.y < 601:
                        item.show()
                # Add lanes at the top
                if counter % 21 == 0:
                    if counter < 1082:
                        lane_number += 1
                        lane.append(lanes(lane_number, SURFACE, -40))

                # Move goldilocks
                goldilocks.rect.y += 4
                if goldilocks.lane < len(lane):
                    goldilocks.flow1(lane[goldilocks.lane])

                # Check for lose
                if goldilocks.lose:
                    lose_process = True
                    freeze = True
                    start_freeze = 0

                # Draw everything else on screen
                land.draw()
                SURFACE.blit(score_display, (40, 10))
                player_sprite.draw(SURFACE)

            # If/when lose
            if lose_process:
                pygame.mixer.music.set_volume(0.2)
                if start_freeze == 0:
                    music.water.play()
                    music.lose.play()
                start_freeze += 1
                if start_freeze % 80 == 0:
                    lvl1_lose = True

            # Key shard animation
            if key_collected and k1.scaleFactor > 0.2:
                k1.animation()
            keys.draw(SURFACE)

            # Ending level when win
            if counter >= 1082 and goldilocks.lane >= len(lane):
                win_counter += 1
                if win_counter >= 30:
                    lvl1_win = True
                    break

            pygame.display.flip()
            await asyncio.sleep(0)

        # Outside lvl 1 loop
        # Inside main game loop
        if lvl1_win:
            print("YOU WIN!")
            for item in lane:
                for sprite in item.logs:
                    sprite.kill()
                    item.logs.remove(sprite)
            lane.clear()
            del lane

        if k1 not in keys:
            keys.add(k1)
            k1.restart()
            while k1.scaleFactor > 0.2:
                k1.animation()

        #if quit:
        #break

        goldilocks.imagesNormal = [pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_front.png')), pygame.image.load(os.path.join('GameGraphics','Goldilocks_back.png')), pygame.image.load(os.path.join('GameGraphics', 'Goldilocks_left.png')), pygame.image.load(os.path.join('GameGraphics','Goldilocks_right.png'))]

        afterlvl1 = True
        counter = 0
        explain = True
        signN = 3
        BACKGROUND[5] = pygame.transform.flip(BACKGROUND[5], True, False)
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        sign4 = message(3)
        intro_sprites.add(sign4)
        sign4.zIn = True
        goldilocks.image = goldilocks.imagesNormal[0]

        music.win.play()

        while afterlvl1:
            clock.tick(FPS)
            counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    afterlvl1 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        afterlvl1 = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign4.zIn = False
                        signN += 1
                        sign4.zOut = True
                        goldilocks.rect.y = 350
                        goldilocks.rect.x = 550
                        # music.music_transition(pause)

            if sign4.zIn:
                sign4.zoomIn()
            if sign4.zOut:
                SURFACE.blit(BACKGROUND[5], (0, 0))
                if sign4.scaleFactor > 0.05:
                    sign4.zoomOut()
                else:
                    sign4.zOut = False
                    explain = False
                    intro_sprites.remove(sign4)
                    sign4.kill()
                player_sprite.draw(SURFACE)

            if not explain:
                SURFACE.blit(BACKGROUND[5], (0, 0))
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 990:
                    afterlvl1 = False
                    break
                player_sprite.draw(SURFACE)

            keys.draw(SURFACE)
            intro_sprites.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        beforelvl2 = True
        counter = 0
        explain = False
        signN = 4
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        sign5 = message(4)
        goldilocks.rect.x = 0

        while beforelvl2:
            clock.tick(FPS)
            counter += 1

            SURFACE.blit(BACKGROUND[6], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    beforelvl2 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        beforelvl2 = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign5.zIn = False
                        signN += 1
                        sign5.zOut = True

            if not explain:
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 500:
                    explain = True
                    intro_sprites.add(sign5)
                    sign5.zIn = True
            else:
                if sign5.zIn:
                    sign5.zoomIn()
                if sign5.zOut:
                    if sign5.scaleFactor > 0.05:
                        goldilocks.rect.x = -100
                        sign5.zoomOut()
                    else:
                        beforelvl2 = False
                        break
            player_sprite.draw(SURFACE)
            keys.draw(SURFACE)
            intro_sprites.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        # Load and play the second music track
        # pause = music.music_level()

        # Init level 2
        # Variables
        lvl2 = True
        lvl2_win = False
        lvl2_lose = False
        score = 0
        speed = 10
        counter = 0
        freeze = False
        lose_process = False
        key_collected = False
        win_counter = 0

        # Sprites
        goldilocks.lvl2__init__()
        all_spikes = pygame.sprite.Group()
        all_spikes.add(spikes(2))
        way_out = tunnel_exit(SURFACE)

        music.lose.set_volume(0.8)

        # Level 2 loop
        while lvl2 and not lvl2_win:
            # FPS
            clock.tick(FPS)
            counter += 1

            # Sccore display
            score_display = score_font.render(str(score), True, (255, 250, 250))

            # Check for win - lose status
            if lvl2_win:
                lvl2 = False
                break
            elif lvl2_lose:
                # Reset everything
                pygame.mixer.music.set_volume(0.5)
                if score >= 40:
                    keys.remove(k2)
                score = 0
                speed = 10
                counter = 0
                freeze = False
                lose_process = False
                key_collected = False
                goldilocks.lvl2__init__()
                for sprite in all_spikes:
                    sprite.kill()
                all_spikes.empty()
                all_spikes.add(spikes(0))
                lvl2_lose = False

            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    lvl2 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        lvl2 = False
                        break

            # Get key pressed for control functions
            key_pressed = pygame.key.get_pressed()
            # Jump
            if key_pressed[pygame.K_SPACE] or key_pressed[pygame.K_UP]:
                goldilocks.jumping = True

            # Movements
            if not freeze:
                # Background and score display
                SURFACE.blit(BACKGROUND[1], (0, 0))
                SURFACE.blit(score_display, (30, 40))

                # Add new spikes
                if counter < 2400:
                    if all_spikes.sprites()[-1].add_new():
                        all_spikes.add(spikes(counter))

                # Remove unused sprites
                for sprite in all_spikes:
                    if sprite.rect.x < -2 - sprite.length:
                        all_spikes.remove(sprite)
                        sprite.kill()

                # Move spikes
                all_spikes.update(speed)

                # Update speed
                if counter % 1000 == 0:
                    speed += 1

                # Check for spikes passing player
                try:
                    # Check for collisons
                    freeze = goldilocks.check_collision2(all_spikes.sprites()[0])

                    # Update score
                    if all_spikes.sprites()[0].score == 1:
                        score += 1
                except:
                    pass

                # Running animation
                if way_out.rect.x > 250:
                    goldilocks.run2(counter)

                # Exit approaching player
                if counter >= 2500 and way_out.rect.x > 250:
                    way_out.rect.x -= 7

                # if lose
                if freeze:
                    lose_process = True
                    start_freeze = 0

                # Draw all sprites
                way_out.draw()
                player_sprite.draw(SURFACE)
                all_spikes.draw(SURFACE)

            # Collect key shard
            if score == 40 and not key_collected:
                key_collected = True
                keys.add(k2)
                k2.restart()
                music.key.play()

            # Key animation
            if key_collected and k2.scaleFactor > 0.2:
                k2.animation()
            keys.draw(SURFACE)

            # Freeze when lose
            if lose_process:
                pygame.mixer.music.set_volume(0.2)
                if start_freeze == 0:
                    music.lose.play()
                start_freeze += 1
                if start_freeze % 60 == 0:
                    lvl2_lose = True

            # When win
            if way_out.rect.x <= 250:
                win_counter += 1
                if win_counter % 60 == 0:
                    lvl2 = False
                    break

            pygame.display.flip()
            await asyncio.sleep(0)

        if lvl2_win:
            print("YOU WIN AGAIN!")

        #if quit:
        #break

        if k2 not in keys:
            keys.add(k2)
            k2.restart()
            while k2.scaleFactor > 0.2:
                k2.animation()

        afterlvl2 = True
        counter = 0
        explain = True
        signN = 5
        BACKGROUND[6] = pygame.transform.flip(BACKGROUND[6], True, False)
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        sign6 = message(5)
        intro_sprites.add(sign6)
        sign6.zIn = True
        goldilocks.image = goldilocks.imagesNormal[0]

        music.win.play()

        while afterlvl2:
            clock.tick(FPS)
            counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    afterlvl2 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        afterlvl2 = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign6.zIn = False
                        signN += 1
                        sign6.zOut = True
                        goldilocks.rect.y = 350
                        goldilocks.rect.x = 500
                        # music.music_transition(pause)

            if sign6.zIn:
                sign6.zoomIn()
            if sign6.zOut:
                SURFACE.blit(BACKGROUND[6], (0, 0))
                if sign6.scaleFactor > 0.05:
                    sign6.zoomOut()
                else:
                    sign6.zOut = False
                    explain = False
                    intro_sprites.remove(sign6)
                    sign6.kill()
                player_sprite.draw(SURFACE)

            if not explain:
                SURFACE.blit(BACKGROUND[6], (0, 0))
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 990:
                    afterlvl6 = False
                    break
                player_sprite.draw(SURFACE)
            keys.draw(SURFACE)
            intro_sprites.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        beforelvl3 = True
        counter = 0
        explain = False
        signN = 6
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        sign7 = message(6)
        goldilocks.rect.x = 0

        while beforelvl3:
            clock.tick(FPS)
            counter += 1

            SURFACE.blit(BACKGROUND[7], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    beforelvl3 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        beforelvl3 = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign7.zIn = False
                        signN += 1
                        sign7.zOut = True

            if not explain:
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 500:
                    explain = True
                    intro_sprites.add(sign7)
                    sign7.zIn = True
            else:
                if sign7.zIn:
                    sign7.zoomIn()
                if sign7.zOut:
                    if sign7.scaleFactor > 0.05:
                        goldilocks.rect.x = -100
                        sign7.zoomOut()
                    else:
                        beforelvl3 = False
                        break
            player_sprite.draw(SURFACE)
            keys.draw(SURFACE)
            intro_sprites.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        # Load and play the second music track
        # pause = music.music_level()

        # Init level 3
        # Variables
        lvl3 = True
        lvl3_win = False
        lvl3_lose = False
        score = 0
        speed = 3
        counter = 0
        start_freeze = 0
        freeze = False
        lose_process = False
        key_collected = False
        win_counter = 0
        # Sprites
        goldilocks.lvl3__init__()
        marking = pygame.sprite.Group()
        marking.add(marks(0, 900))
        marking.add(marks(1, 200))
        guards = pygame.sprite.Group()
        guards.add(guard())
        exitway = door(SURFACE)

        # Level 3 loop
        while lvl3 and not lvl3_win:
            # FPS
            clock.tick(FPS)
            counter += 1

            # Score display
            score_display = score_font.render(str(score), True, (255, 250, 250))

            # Check for win-lose status
            if lvl3_win:
                lvl3 = False
                break
            if lvl3_lose:
                pygame.mixer.music.set_volume(0.5)
                if counter >= 2560:
                    goldilocks.borderright = 930
                    exitway.rect.x = 1001
                    keys.remove(k3)
                    key_collected = False
                    win_counter = 0
                score = 0
                speed = 2
                counter = 0
                start_freeze = 0
                freeze = False
                lose_process = False
                key_collected = False
                win_counter = 0
                # Sprites
                goldilocks.lvl3__init__()
                marking = pygame.sprite.Group()
                marking.add(marks(0, 900))
                marking.add(marks(1, 200))
                guards = pygame.sprite.Group()
                guards.add(guard())
                lvl3_lose = False

            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    lvl3 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        lvl3 = False
                        break
                    # Goldilocks flipping
                    if event.key != pygame.K_LEFT:
                        goldilocks.left = False
                    if event.key == pygame.K_w:
                        counter = 2460
                        print(counter)

            # Movements
            if not freeze:
                # Draw background
                SURFACE.blit(BACKGROUND[2], (0, 0))
                #SURFACE.blit(score_display, (40, 20))

                # Move sprites
                key = pygame.key.get_pressed()
                goldilocks.move3(key, counter, speed)
                marking.update(speed)
                guards.update()

                # Check for collisions
                if len(guards) != 0:
                    freeze = goldilocks.check_collision3(guards.sprites()[-1])
                    if freeze:
                        start_freeze = 0
                        lose_process = True

                # Add guards
                if counter < 2500 and guards.sprites()[-1].rect.x < 0:
                    guards.add(guard())

                # Remove off-screen guards
                for sprite in guards:
                    if sprite.rect.x < -sprite.length:
                        sprite.kill()
                        guards.remove(sprite)

                # Draw all sprites
                marking.draw(SURFACE)
                guards.draw(SURFACE)
                player_sprite.draw(SURFACE)
                if counter % 40 == 0:
                    score += 1

            if lose_process:
                pygame.mixer.music.set_volume(0.2)
                if start_freeze == 0:
                    music.lose.play()
                start_freeze += 1
                if start_freeze % 60 == 0:
                    lvl3_lose = True

            if counter == 2700:
                goldilocks.borderright = 430
                if goldilocks.rect.x > 450:
                    goldilocks.rect.x = 400
                key_collected = True
                keys.add(k3)
                k3.restart()
                music.key.play()

            if key_collected:
                if exitway.rect.x > 500:
                    exitway.update(speed)
                else:
                    win_counter += 1
                    speed = 0
                    if win_counter % 60 == 0:
                        lvl3_win = True
                        lvl3 = False
                        break
                if k3.scaleFactor > 0.2:
                    k3.animation()
            exitway.draw()
            keys.draw(SURFACE)



            pygame.display.flip()
            await asyncio.sleep(0)

        if k3 not in keys:
            keys.add(k3)
            k3.restart()
            while k3.scaleFactor > 0.2:
                k3.animation()

        # music.music_transition(pause)

        afterlvl3 = True
        counter = 0
        explain = True
        signN = 7
        BACKGROUND[7] = pygame.transform.flip(BACKGROUND[7], True, False)
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        sign8 = message(7)
        intro_sprites.add(sign8)
        sign8.zIn = True
        goldilocks.image = goldilocks.imagesNormal[0]
        goldilocks.resize3()
        goldilocks.rect.y = 350
        goldilocks.rect.x = 500

        music.win.play()

        while afterlvl3:
            clock.tick(FPS)
            counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    afterlvl3 = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        afterlvl3 = False
                        break
                    if event.key == pygame.K_SPACE and explain:
                        sign8.zIn = False
                        signN += 1
                        sign8.zOut = True


            if sign8.zIn:
                sign8.zoomIn()
            if sign8.zOut:
                if sign8.scaleFactor > 0.05:
                    sign8.zoomOut()
                else:
                    sign8.zOut = False
                    explain = False
                    intro_sprites.remove(sign8)
                    sign8.kill()
                player_sprite.draw(SURFACE)

            if not explain:
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 990:
                    afterlvl3 = False
                    break
            SURFACE.blit(BACKGROUND[7], (0, 0))
            player_sprite.draw(SURFACE)
            keys.draw(SURFACE)
            intro_sprites.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        ending = True
        counter = 0
        waitCount = 0
        win = False
        win_animation = False
        animate1 = False
        animate2 = False
        key_whole = None
        signN = 8
        for sprite in intro_sprites:
            intro_sprites.remove(sprite)
            sprite.kill()
        goldilocks.rect.x = 0

        while ending:
            clock.tick(FPS)
            counter += 1

            if not win:
                SURFACE.blit(BACKGROUND[8], (0, 0))
            else:
                SURFACE.blit(BACKGROUND[9], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    ending = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit = True
                        ending = False
                        break

            if not win_animation and not win:
                key = pygame.key.get_pressed()
                goldilocks.move0(key)
                if goldilocks.rect.x >= 450:
                    goldilocks.image = goldilocks.imageStill
                    win_animation = True
                    animate1 = True
            elif win_animation:
                if animate1:
                    if k1.rect.y <= 390:
                        k1.win_animation1()
                        k2.win_animation1()
                        k3.win_animation1()
                    else:
                        animate1 = False
                        keys.remove(k1, k2, k3)
                        keys.add(kw)
                        animate2 = True
                        counter = 1
                if animate2:
                    if counter > 30:
                        if kw.rect.x < 585:
                            kw.win_animation2()
                        else:
                            waitCount += 1
                            if waitCount == 20:
                                win_animation = False
                                win = True
                                music.success.play()
            else:
                counter = goldilocks.celebration(counter)
            keys.draw(SURFACE)
            player_sprite.draw(SURFACE)

            pygame.display.flip()
            await asyncio.sleep(0)

        if quit:
            break

asyncio.run(main())
