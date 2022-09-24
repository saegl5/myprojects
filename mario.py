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
WHITE = pygame.Color("white") # mario
YELLOW = pygame.Color("yellow") # platform
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
# Other constants and variables

ground = Rectangle(canvas.SIZE[0], GH)
ground.rect.left = canvas.screen.get_rect().left
ground.rect.bottom = canvas.screen.get_rect().bottom
ground.image.fill(BROWN)
mario = Rectangle(W, H) # see classes.py
mario.rect.x = 50
mario.rect.bottom = ground.rect.top
mario.image.fill(WHITE) # example
platform = Rectangle(200, 50)
platform.rect.right = canvas.screen.get_rect().right
platform.rect.y = 300 # low enough for mario to jump over
platform.image.fill(YELLOW)
grounds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
sprites = pygame.sprite.Group() # all sprites
grounds.add(ground)
platforms.add(platform)
sprites.add(ground, platform, mario) # displays mario in front of ground and platform (order matters)
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
    hit_platform_x = pygame.sprite.spritecollide(mario, platforms, False)
    # could also check if hit_ground, but this is redundant
    if hit_platform_x != []:
        if x_inc > 0: # mario moving rightward
            mario.rect.right = platform.rect.left
        else:
            mario.rect.left = platform.rect.right
        if halt == True:
            x_inc = 0
    diff = abs(mario.rect.x - l) # not interested in sign
    if mario.rect.x >= l: # move world leftward
        ground.rect.x -= diff
        platform.rect.x -= diff
        mario.rect.x = l # keep mario still
    elif mario.rect.x < l: # move world back
        if ground.rect.x < 0: # resets initial positions
            if ground.rect.x + diff > 0: # check gap
                gap = ground.rect.x + diff
                ground.rect.x += diff - gap
                platform.rect.x += diff - gap
            else:
                ground.rect.x += diff
                platform.rect.x += diff
            mario.rect.x = l

    mario.rect.y += y_inc # mario.rect.y truncates decimal point, but okay, simply causes delay
    hit_ground = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground != []:
        mario.rect.bottom = ground.rect.top
        y_inc = 0 # logical
        on = True
        if halt == True:
            x_inc = 0
    elif hit_platform_y != []:
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