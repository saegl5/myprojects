"""
"Mario" Game
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle
from custom.energy import time_stamp, save_energy
# Other modules to import

pygame.display.set_caption("QUESTABOX's \"Mario\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeated key presses, smooths out movement
# Other settings

BROWN = pygame.Color("burlywood4") # optional color, ground
BLACK = pygame.Color("black") # mario
YELLOW = pygame.Color("yellow3") # platforms
W_mario = 75 # default, used ratio 3:4
W_goomba = 64
H_mario = 100 # default
H_goomba = 56
GH = 50 # ground height
V = 5 # example
x_inc_mario = 0 # short for "increment"
x_inc_goomba = V/5
y_inc_mario = 0
first = True # hopping
halt = True # walking
on = True # ground or platform
l = canvas.SIZE[0]/2 # where world starts moving
mario_frames = pygame.image.load('images/mario_spritesheet.png').convert_alpha()
mario_frames = pygame.transform.scale(mario_frames, (W_mario*9, H_mario*3)) # sprite sheet has 9 columns, 3 rows
goomba_frames = pygame.image.load('images/goomba_spritesheet.png').convert_alpha()
count1 = 0 # mario walk
count2 = 0 # goomba walk
facing_left = False
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.125) # optional
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

frame1 = [ (10,           13,           W_mario-17, H_mario-13), 
           (4*W_mario+2,  H_mario+9,    W_mario-10, H_mario-9), 
           (5*W_mario,    H_mario+15,   W_mario,    H_mario-15),
           (3*W_mario+10, 2*H_mario+14, W_mario-12, H_mario-14) ]
# first mario frame is for standing still, second and third for walking/chopping, and fourth for jumping
# will not loop frame list, so to call any parameter use two indices
mario = Rectangle(frame1[0][2], frame1[0][3])
# change W to align mario's right, change H to align mario's bottom
mario.rect.x = 50
mario.rect.y = canvas.SIZE[1]-GH-H_mario
mario.image.blit(mario_frames, (0, 0), (frame1[0][0], frame1[0][1], W_mario, H_mario))
# for (frame[0][0], frame[0][1], W, H), it's x, y, width and height of frame
# change x to align mario's left, change y to align mario's top
# mario.image.set_colorkey(YELLOW) # make background visible temporarily

frame2 = [  (0,          0,          W_goomba, H_goomba),
            (W_goomba,   0,          W_goomba, H_goomba),
            (2*W_goomba, H_goomba/2, W_goomba, H_goomba/2)  ]
goombas = pygame.sprite.Group()
goomba = Rectangle(frame2[0][2], frame2[0][3])
goomba.rect.x = 600 # starts near right edge of screen
goomba.rect.y = canvas.SIZE[1]-GH-H_goomba
goomba.image.blit(goomba_frames, (0, 0), (frame2[0][0], frame2[0][1], W_goomba, H_goomba))
goombas.add(goomba)

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

sprites = pygame.sprite.Group() # all sprites
sprites.add(grounds, platforms, goombas, mario) # displays mario in front of grounds, platforms, and goomba (order matters)
# Other sprites

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            canvas.close()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_inc_mario = V
                halt = False
                facing_left = False
                count1 += 1
                if count1 == 1: # in case there is a quick KEYDOWN and KEYUP event
                    mario.rect.w = frame1[2][2]
                    mario.image = pygame.Surface((frame1[2][2], frame1[1][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[1][0], frame1[1][1], frame1[1][2], H_mario))
                if count1 == 5: # else mario appears to hover
                    mario.rect.w = frame1[2][2]
                    mario.image = pygame.Surface((frame1[2][2], frame1[2][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[2][0], frame1[2][1], W_mario, H_mario))
                if count1 % 10 == 0: # on count of 10
                    mario.rect.w = frame1[2][2]
                    mario.image = pygame.Surface((frame1[2][2], frame1[1][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[1][0], frame1[1][1], frame1[1][2], H_mario))
                if count1 % 20 == 0:
                    mario.rect.w = frame1[2][2]
                    mario.image = pygame.Surface((frame1[2][2], frame1[2][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[2][0], frame1[2][1], W_mario, H_mario))
            if event.key == pygame.K_LEFT:
                x_inc_mario = -V
                halt = False
                facing_left = True
                count1 += 1
                if count1 == 1:
                    mario.image = pygame.Surface((frame1[2][2], frame1[1][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[1][0], frame1[1][1], frame1[1][2], H_mario))
                    mario.image = pygame.transform.flip(mario.image, flip_x=True, flip_y=False)
                if count1 == 5:
                    mario.image = pygame.Surface((frame1[2][2], frame1[2][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[2][0], frame1[2][1], W_mario, H_mario))
                    mario.image = pygame.transform.flip(mario.image, flip_x=True, flip_y=False)
                if count1 % 10 == 0:
                    mario.image = pygame.Surface((frame1[2][2], frame1[1][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[1][0], frame1[1][1], frame1[1][2], H_mario))
                    mario.image = pygame.transform.flip(mario.image, flip_x=True, flip_y=False)
                if count1 % 20 == 0:
                    mario.image = pygame.Surface((frame1[2][2], frame1[2][3])).convert_alpha()
                    mario.image.blit(mario_frames, (0, 0), (frame1[2][0], frame1[2][1], W_mario, H_mario))
                    mario.image = pygame.transform.flip(mario.image, flip_x=True, flip_y=False)
            if event.key == pygame.K_SPACE and first == True and on == True:
                y_inc_mario = -2.5*V # y decreases going upward
                first = False
                on = False
                mario.rect.w = frame1[3][2]
                mario.image = pygame.Surface((frame1[3][2], frame1[3][3])).convert_alpha()
                mario.image.blit(mario_frames, (0, 0), (frame1[3][0], frame1[3][1], W_mario, H_mario))
                mario.image = pygame.transform.flip(mario.image, flip_x=not(facing_left), flip_y=False)
                count1 = 0 # display walking frames evenly
                jump_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                first = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                halt = True
                count1 = 0 # display walking frames evenly
        # Other keyboard or mouse/trackpad events

        time_stamp(event)

    mario.rect.x += x_inc_mario
    hit_ground_x = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_x = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_x != []:
        for ground in hit_ground_x:
            if x_inc_mario > 0: # mario moving rightward
                mario.rect.right = ground.rect.left
            else:
                mario.rect.left = ground.rect.right
    elif hit_platform_x != []:
        for platform in hit_platform_x:
            if x_inc_mario > 0:
                mario.rect.right = platform.rect.left
            else:
                mario.rect.left = platform.rect.right
        if halt == True:
            x_inc_mario = 0
    diff = abs(mario.rect.x - l) # not interested in sign
    if mario.rect.x >= l: # move world leftward
        for ground in grounds:
            ground.rect.x -= diff
        for platform in platforms:
            platform.rect.x -= diff
        goomba.rect.x -= diff
        mario.rect.x = l # keep mario still
    elif mario.rect.x < l: # move world back
        if grounds.sprites()[0].rect.x < 0: # retains initial positions, ground sprites were not randomly positioned
            if grounds.sprites()[0].rect.x + diff > 0: # check gap
                gap = grounds.sprites()[0].rect.x + diff
                for ground in grounds:
                    ground.rect.x += diff - gap
                for platform in platforms:
                    platform.rect.x += diff - gap
                goomba.rect.x += diff - gap
            else:
                for ground in grounds:
                    ground.rect.x += diff
                for platform in platforms:
                    platform.rect.x += diff
                goomba.rect.x += diff
            mario.rect.x = l
        if mario.rect.x < 0: # left boundary
            mario.rect.x = 0

    mario.rect.y += y_inc_mario # mario.rect.y truncates decimal point, but okay, simply causes delay
    hit_ground_y = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    hit_goomba_y = pygame.sprite.spritecollide(mario, goombas, False) # don't want to remove goomba until after showing him squeezed
    if hit_ground_y != []:
        for ground in hit_ground_y:
            mario.rect.bottom = ground.rect.top
        y_inc_mario = 0 # logical
        on = True
        if halt == True:
            x_inc_mario = 0
            mario.image = pygame.Surface((frame1[0][2], frame1[0][3])).convert_alpha()
            mario.image.blit(mario_frames, (0, 0), (frame1[0][0], frame1[0][1], W_mario, H_mario))
            mario.image = pygame.transform.flip(mario.image, flip_x=facing_left, flip_y=False)
    elif hit_platform_y != []:
        for platform in hit_platform_y:
            if y_inc_mario < 0: # in jump
                mario.rect.top = platform.rect.bottom # hits his head
            else: # falling or plateaued
                mario.rect.bottom = platform.rect.top
                on = True
        y_inc_mario = 0 # unsticks mario from below, and in case mario walks off platform
        if halt == True:
            x_inc_mario = 0
            mario.image = pygame.Surface((frame1[0][2], frame1[0][3])).convert_alpha()
            mario.image.blit(mario_frames, (0, 0), (frame1[0][0], frame1[0][1], W_mario, H_mario))
            mario.image = pygame.transform.flip(mario.image, flip_x=facing_left, flip_y=False)
    elif hit_goomba_y != []:
        goomba.rect.y = canvas.SIZE[1]-GH-H_goomba/2 # just me
        goomba.image = pygame.Surface((frame2[2][2], frame2[2][3])).convert_alpha() # just me
        goomba.image.blit(goomba_frames, (0, 0), (frame2[2][0], frame2[2][1], W_goomba, H_goomba/2))
        # goomba.image.set_colorkey(BLACK) # just me
    else: # cycles, fewer for higher values of gravity
        y_inc_mario += 0.5 # gravity, place here otherwise increment will keep running
        on = False

    goomba.rect.x -= x_inc_goomba
    count2 += 1
    if count2 % 20 == 0:
        goomba.rect.y = canvas.SIZE[1]-GH-H_goomba # temporary, just me
        goomba.image = pygame.Surface((frame2[1][2], frame2[1][3])).convert_alpha()
        goomba.image.blit(goomba_frames, (0, 0), (frame2[1][0], frame2[1][1], W_goomba, H_goomba))
         # didn't start with first index 0 because first frame is already displayed
    if count2 % 40 == 0:
        goomba.rect.y = canvas.SIZE[1]-GH-H_goomba # temporary, just me
        goomba.image = pygame.Surface((frame2[0][2], frame2[0][3])).convert_alpha()
        goomba.image.blit(goomba_frames, (0, 0), (frame2[0][0], frame2[0][1], W_goomba, H_goomba))
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()