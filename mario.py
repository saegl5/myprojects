"""
"Mario" Game
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle
from custom.energy import time_stamp, save_energy
from custom.functions import left_wall, walk, stand#, frame
# Other modules to import

pygame.display.set_caption("QUESTABOX's \"Mario\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeated key presses, smooths out movement
# Other settings

BROWN = pygame.Color("burlywood4") # optional color, ground
BLACK = pygame.Color("black") # mario
YELLOW = pygame.Color("yellow3") # platforms
W = 75 # default, used ratio 3:4
H = 100 # default
GH = 50 # ground height
V = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
first = True # hopping
halt = True # walking
on = True # ground or platform
l = canvas.SIZE[0]/2 # where world starts moving
mario_frames = pygame.image.load('images/mario_spritesheet.png').convert()
mario_frames = pygame.transform.scale(mario_frames, (W*9, H*3)) # sprite sheet has 9 columns, 3 rows
count = 0
facing_left = False
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.125) # reduce volume
# Other constants and variables

blocks1 = [ (0,                  canvas.SIZE[1]-GH, canvas.SIZE[0], GH),
            (canvas.SIZE[0]+100, canvas.SIZE[1]-GH, 300,            GH),
            (canvas.SIZE[0]+500, canvas.SIZE[1]-GH, 600,            GH) ]
            # three blocks, (x, y, w, h) each, second and third block to right of screen
            # third ground sprite: x > canvas.SIZE[0]+100+300 = canvas.SIZE[0]+400
grounds = pygame.sprite.Group()
for block in blocks1: # each block
    ground = Rectangle(block[2], block[3]) # see classes.py
    ground.rect.x = block[0]
    ground.rect.y = block[1]
    ground.image.fill(BROWN)
    grounds.add(ground)

frame = [  (10, 13, W-17, H-13), 
           (3, H+12, W-7, H-12),
           (W+12, H+10, W-23, H-10),
           (W+4, 9, W-8, H-9) ]
# first mario frame is for standing still, second and third for walking, and fourth for jumping
# will not loop frame list, so to call any parameter use two indices
mario = Rectangle(frame[0][2], frame[0][3])
# change W to align mario's right, change H to align mario's bottom
mario.rect.x = 50
mario.rect.y = canvas.SIZE[1]-GH-H
mario.image.blit(mario_frames, (0, 0), (frame[0][0], frame[0][1], W, H))
# for (frame[0][0], frame[0][1], W, H), it's x, y, width and height of frame
# change x to align mario's left, change y to align mario's top
mario.image.set_colorkey(BLACK) # make background visible temporarily

blocks2 = [ (400,  300, 200, 50),
            (800,  250, 200, 50),
            (1300, 100, 200, 50) ]
            # three blocks, (x, y, w, h) each
platforms = pygame.sprite.Group()
for block in blocks2:
    platform = Rectangle(block[2], block[3])
    platform.rect.x = block[0] # reverted to x
    platform.rect.y = block[1] # low enough for mario to jump over
    platform.image.fill(YELLOW)
    platforms.add(platform)

walls = pygame.sprite.Group()
walls.add(left_wall()) # outer wall

sprites = pygame.sprite.Group() # all sprites
sprites.add(walls, grounds, platforms, mario) # displays mario in front of grounds and platforms (order matters)
# Other sprites

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            canvas.close()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_inc = V
                halt = False
                count += 1
                facing_left = False
                walk(count, mario, mario_frames, frame, W, H, facing_left)
            if event.key == pygame.K_LEFT:
                x_inc = -V
                halt = False
                count += 1
                facing_left = True
                walk(count, mario, mario_frames, frame, W, H, facing_left)
            if event.key == pygame.K_SPACE and first == True and on == True:
                y_inc = -2.5*V # y decreases going upward
                first = False
                on = False
                mario.image = pygame.Surface((frame[3][2], frame[3][3]))
                mario.image.blit(mario_frames, (0, 0), (frame[3][0], frame[3][1], W, H))
                if facing_left == True:
                    mario.image = pygame.transform.flip(mario.image, flip_x=True, flip_y=False)
                count = 0 # display walking frames evenly
                mario.image.set_colorkey(BLACK)
                jump_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                first = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                halt = True
                count = 0 # display walking frames evenly
                # mario.rect.w = frame[0][2]
                # mario.image = pygame.Surface((frame[0][2], frame[0][3]))
                # mario.image.blit(mario_frames, (0, 0), (frame[0][0], frame[0][1], W, H))
                # if facing_left == True:
                #     mario.image = pygame.transform.flip(mario.image, flip_x=True, flip_y=False)
                # mario.image.set_colorkey(BLACK)
        # Other keyboard or mouse/trackpad events

        time_stamp(event)

    mario.rect.x += x_inc
    hit_ground_x = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_x = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_x != []:
        for ground in hit_ground_x:
            if x_inc > 0: # mario moving rightward
                mario.rect.right = ground.rect.left
            else: # if x_inc < 0: # discovered quirk?
                mario.rect.left = ground.rect.right
    elif hit_platform_x != []: # had tried "if"
        for platform in hit_platform_x:
            if x_inc > 0:
                mario.rect.right = platform.rect.left
            else: # if x_inc < 0: # discovered quirk? plus another when jump at right edge, maybe because dropped at beginning?
                mario.rect.left = platform.rect.right
        if halt == True:
            x_inc = 0
    diff = abs(mario.rect.x - l) # not interested in sign
    if mario.rect.x >= l: # move world leftward
        for ground in grounds:
            ground.rect.x -= diff
        for platform in platforms:
            platform.rect.x -= diff
        mario.rect.x = l # keep mario still
    elif mario.rect.x < l: # move world back
        if grounds.sprites()[0].rect.x <= left_wall().rect.x: # retains initial positions, ground sprites were not randomly positioned
            if grounds.sprites()[0].rect.x + diff > 0: # check gap
                gap = grounds.sprites()[0].rect.x + diff
                for ground in grounds:
                    ground.rect.x += diff - gap
                for platform in platforms:
                    platform.rect.x += diff - gap
            else:
                for ground in grounds:
                    ground.rect.x += diff
                for platform in platforms:
                    platform.rect.x += diff
            mario.rect.x = l
        hit_wall = pygame.sprite.spritecollide(mario, walls, False) # acts as left boundary
        for wall in hit_wall:
            mario.rect.left = wall.rect.right # currently only one wall

    mario.rect.y += y_inc # mario.rect.y truncates decimal point, but okay, simply causes delay
    hit_ground_y = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_y != []:
        for ground in hit_ground_y:
            mario.rect.bottom = ground.rect.top
        y_inc = 0 # logical
        on = True
        if halt == True:
            x_inc = 0
            stand(mario, mario_frames, frame, W, H, facing_left)
    elif hit_platform_y != []:
        for platform in hit_platform_y:
            if y_inc < 0: # in jump
                mario.rect.top = platform.rect.bottom # hits his head
            else: # falling or plateaued
                mario.rect.bottom = platform.rect.top
                on = True
        y_inc = 0 # unsticks mario from below, and in case mario walks off platform
        if halt == True:
            x_inc = 0
            stand(mario, mario_frames, frame, W, H, facing_left)
    else: # cycles, fewer for higher values of gravity
        y_inc += 0.5 # gravity, place here otherwise increment will keep running
        on = False
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()