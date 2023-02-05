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
W_mario = 75 # default, used ratio 3:4
W_goomba = 64
H_mario = 100 # default
H_goomba = 56
GH = 50 # ground height
V = 5 # example
x_inc_mario = 0 # short for "increment"
x_inc_goomba = V/5
x_inc_platform = V/5
y_inc_mario = 0.5
first = True # hopping
halt = True # walking
on = True # ground, platform or goomba
l = canvas.SIZE[0]/2 # where world starts moving
mario_frames = pygame.image.load('images/mario_spritesheet.png').convert_alpha()
mario_frames = pygame.transform.scale(mario_frames, (W_mario*9, H_mario*3)) # sprite sheet has 9 columns, 3 rows
goomba_frames = pygame.image.load('images/goomba_spritesheet.png').convert_alpha()
count1 = 0 # mario walk
count2 = 0 # goomba walk
facing_left = False
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.125) # optional
stomp = False
# Other constants and variables

blocks1 = [ (0,                   canvas.SIZE[1]-GH, canvas.SIZE[0], GH), #  x0 = 0,              choose w0,   want C0=100 (gap size)
            (canvas.SIZE[0]+100,  canvas.SIZE[1]-GH, 300,            GH), #  x1 = x0 + w0 + C0,   choose w1,   want C1=100
            (canvas.SIZE[0]+500,  canvas.SIZE[1]-GH, 600,            GH), #  x2 = x1 + w1 + C1,   choose w2,   want C2=400
            (canvas.SIZE[0]+1500, canvas.SIZE[1]-GH, 400,            GH), #  x3 = x2 + w2 + C2,   choose w3,   want C3=100
            (canvas.SIZE[0]+2000, canvas.SIZE[1]-GH, 200,            GH), #  x4 = x3 + w3 + C3,   choose w4,   want C4=75
            (canvas.SIZE[0]+2275, canvas.SIZE[1]-GH, 700,            GH) ] # x5 = x4 + w4 + C4,   choose w5,   want C5=0 (no gap)
            # six blocks, (x, y, w, h) each, additional blocks to right of screen
grounds = pygame.sprite.Group()
for block in blocks1: # each block
    ground = Rectangle(block[2], block[3]) # see classes.py
    ground.rect.x = block[0]
    ground.rect.y = block[1]
    ground.image.fill(BROWN)
    grounds.add(ground)

frame1 = [  (10,         13,         W_mario-17, H_mario-13), 
            (3,          H_mario+12, W_mario-7,  H_mario-12),
            (W_mario+12, H_mario+10, W_mario-23, H_mario-10),
            (W_mario+4,  9,          W_mario-8,  H_mario-9)  ]
# first mario frame is for standing still, second and third for walking, and fourth for jumping
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

blocks2 = [ (400,  300, 200, 50), #  x0 = 400,            choosing y0,   want C0=200 (gap size)
            (800,  250, 200, 50), #  x1 = x0 + w0 + C0,   choosing y1,   want C1=300 gap
            (1300, 100, 200, 50), #  x2 = x1 + w1 + C1,   choosing y2,   want C2=100 gap
            (1600, 100, 200, 50), #  x3 = x2 + w2 + C2,   choosing y3,   want C3=500 gap
            (2300, 300, 200, 50), #  x4 = x3 + w3 + C3,   choosing y4,   want C4=200 gap
            (2700, 150, 200, 50) ] # x5 = x4 + w4 + C4,   choosing y5,   want C5=0 (no gap)
            # six blocks, (x, y, w, h) each
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
sprites.add(walls, grounds, platforms, goombas, mario) # displays mario in front of grounds, platforms, and goomba (order matters)
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
            if event.key == pygame.K_LEFT:
                x_inc_mario = -V
                halt = False
                facing_left = True
            if event.key == pygame.K_SPACE and first == True and on == True:
                y_inc_mario = -2.5*V # y decreases going upward
                first = False
                on = False
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
        if grounds.sprites()[0].rect.x <= left_wall().rect.x: # retains initial positions, ground sprites were not randomly positioned
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
        hit_wall = pygame.sprite.spritecollide(mario, walls, False) # acts as left boundary
        for wall in hit_wall:
            mario.rect.left = wall.rect.right # currently only one wall

    # mario.rect.y += y_inc_mario # mario.rect.y truncates decimal point, but okay, simply causes delay
    mario.rect.y = round(mario.rect.y + y_inc_mario) # remove delay
    hit_ground_y = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    hit_goomba_y = pygame.sprite.spritecollide(mario, goombas, False) # don't want to remove goomba until after showing him squeezed
    if hit_ground_y != []:
        for ground in hit_ground_y:
            mario.rect.bottom = ground.rect.top
        y_inc_mario = 0.5 # logical
        on = True
        if halt == True:
            x_inc_mario = 0
            stand(mario, mario_frames, frame1, W_mario, H_mario, facing_left)
        else:
            count1 += 1 # don't just display first step
            walk(count1, mario, mario_frames, frame1, W_mario, H_mario, facing_left, on)
    elif hit_platform_y != []:
        for platform in hit_platform_y:
            if y_inc_mario < 0: # in jump
                mario.rect.top = platform.rect.bottom # hits his head
            else: # falling or plateaued
                mario.rect.bottom = platform.rect.top
                on = True
        y_inc_mario = 0.5 # unsticks mario from below, and in case mario walks off platform
        if halt == True:
            x_inc_mario = 0
            stand(mario, mario_frames, frame1, W_mario, H_mario, facing_left)
        else:
            count1 += 1 # don't just display first step
            walk(count1, mario, mario_frames, frame1, W_mario, H_mario, facing_left, on)
    elif hit_goomba_y != []:
        goomba.rect.y = canvas.SIZE[1]-GH-H_goomba/2
        goomba.image = pygame.Surface((frame2[2][2], frame2[2][3])).convert_alpha()
        goomba.image.blit(goomba_frames, (0, 0), (frame2[2][0], frame2[2][1], W_goomba, H_goomba/2))
        stomp = True
        count2 = 0 # reset for consistent pause
        y_inc_mario = -1.5*V # short hop
        goombas.remove(goomba) # let goomba rest
        on = True # if want to jump higher
    else: # cycles, fewer for higher values of gravity
        y_inc_mario += 0.5 # gravity, place here otherwise increment will keep running
        on = False
        mario.rect.w = frame1[3][2]
        mario.image = pygame.Surface((frame1[3][2], frame1[3][3])).convert_alpha()
        mario.image.blit(mario_frames, (0, 0), (frame1[3][0], frame1[3][1], W_mario, H_mario))
        mario.image = pygame.transform.flip(mario.image, flip_x=facing_left, flip_y=False)

    count2 += 1
    if stomp == False:
        goomba.rect.x -= x_inc_goomba
        if count2 % 20 == 0:
            goomba.image = pygame.Surface((frame2[1][2], frame2[1][3])).convert_alpha()
            goomba.image.blit(goomba_frames, (0, 0), (frame2[1][0], frame2[1][1], W_goomba, H_goomba))
            # didn't start with first index 0 because first frame is already displayed
        if count2 % 40 == 0:
            goomba.image = pygame.Surface((frame2[0][2], frame2[0][3])).convert_alpha()
            goomba.image.blit(goomba_frames, (0, 0), (frame2[0][0], frame2[0][1], W_goomba, H_goomba))
    else:
        if count2 % 120 == 0: # pause
            sprites.remove(goomba)

    platforms.sprites()[2].rect.x -= x_inc_platform # a start
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()