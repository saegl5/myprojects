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
# WHITE = pygame.Color("white") # mario
YELLOW = pygame.Color("yellow") # platforms
W = 48
H = 64
GH = 50 # ground height
V = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
first = True # hopping
halt = True # walking
on = True # ground or platform
l = canvas.SIZE[0]/2 # where world starts moving
mario_frames = pygame.image.load('images/mario_spritesheet.png').convert()
# Other constants and variables

blocks1 = [ (0,                  canvas.SIZE[1]-GH, canvas.SIZE[0], GH),
            (canvas.SIZE[0]+100, canvas.SIZE[1]-GH, 300,            GH),
            (canvas.SIZE[0]+500, canvas.SIZE[1]-GH, 600,            GH) ]
            # three blocks, (x, y, w, h) each, second and third block to right of screen
            # third ground sprite: x > canvas.SIZE[0]+100+300 = canvas.SIZE[0]+400
grounds = pygame.sprite.Group()
for block in blocks1: # each block
    ground = Rectangle(block[2], block[3])
    ground.rect.x = block[0]
    ground.rect.y = block[1]
    ground.image.fill(BROWN)
    grounds.add(ground)

mario = Rectangle(W, H) # see classes.py
mario.rect.x = 50
mario.rect.y = canvas.SIZE[1]-GH-H
# mario.image.fill(WHITE) # example
mario.image.blit(mario_frames, (0, 0), (0, 0, W, H))
# for (0, 0, W, H), it's x, y, width and height of frame

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
sprites.add(grounds, platforms, mario) # displays mario in front of grounds and platforms (order matters)
# Other sprites

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            canvas.close()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_inc = V
                halt = False
            if event.key == pygame.K_LEFT:
                x_inc = -V
                halt = False
            if event.key == pygame.K_SPACE and first == True and on == True:
                y_inc = -2.5*V # y decreases going upward
                first = False
                on = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                first = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                halt = True
        # Other keyboard or mouse/trackpad events

        time_stamp(event)

    mario.rect.x += x_inc
    hit_ground_x = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_x = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_x != []:
        for ground in hit_ground_x:
            if x_inc > 0: # mario moving rightward
                mario.rect.right = ground.rect.left
            else:
                mario.rect.left = ground.rect.right
    elif hit_platform_x != []:
        for platform in hit_platform_x:
            if x_inc > 0:
                mario.rect.right = platform.rect.left
            else:
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
        if grounds.sprites()[0].rect.x < 0: # retains initial positions, ground sprites were not randomly positioned
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
        if mario.rect.x < 0: # left boundary
            mario.rect.x = 0

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
    else: # cycles, fewer for higher values of gravity
        y_inc += 0.5 # gravity, place here otherwise increment will keep running
        on = False
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()