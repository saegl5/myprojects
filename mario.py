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
YELLOW = pygame.Color("yellow3") # platforms
w = 48
h = 64
ground_height = 50
speed = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
first = True # hopping
halt = True # walking
# Other constants and variables

ground = Rectangle(canvas.size[0], ground_height)
ground.rect.left = canvas.screen.get_rect().left
ground.rect.bottom = canvas.screen.get_rect().bottom
ground.image.fill(BROWN)
mario = Rectangle(w, h) # see classes.py
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
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        elif action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RIGHT:
                x_inc = speed
                halt = False
            if action.key == pygame.K_LEFT:
                x_inc = -speed
                halt = False
            if action.key == pygame.K_SPACE and first == True:
                if mario.rect.bottom == ground.rect.top or mario.rect.bottom == platform.rect.top:
                    y_inc = -2.75*speed # y decreases going upward
                    first = False
        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_SPACE:
                first = True
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                halt = True
        # Other keyboard or mouse/trackpad events

        time_stamp(action)

    mario.rect.x += x_inc
    hit_ground_x = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_x = pygame.sprite.spritecollide(mario, platforms, False)
    # could also check if hit_ground, but this is redundant
    if hit_ground_x != []:
        if x_inc > 0:
            mario.rect.right = ground.rect.left
        elif x_inc < 0:
            mario.rect.left = ground.rect.right
    elif hit_platform_x != []:
        if x_inc > 0:
            mario.rect.right = platform.rect.left
        elif x_inc < 0:
            mario.rect.left = platform.rect.right
    if mario.rect.left < ground.rect.left: # could also use mario.rect.x < 0
        mario.rect.left = ground.rect.left
    elif mario.rect.right >= 500: # don't use canvas.size[0] because won't be able to see ahead of you 
        move_left = mario.rect.right - 500
        ground.rect.x -= move_left
        platform.rect.x -= move_left
        mario.rect.right = 500 # keep mario still, also maintains correct change in movement
    elif mario.rect.left <= 200:
        if ground.rect.x < 0:
            move_right = 200 - mario.rect.left
            ground.rect.x += move_right
            platform.rect.x += move_right
            mario.rect.left = 200

    mario.rect.y += y_inc # mario.rect.y truncates decimal point, but okay, simply causes delay
    hit_ground_y = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_y != []:
        mario.rect.bottom = ground.rect.top
        y_inc = 0 # logical
        if halt == True:
            x_inc = 0
    elif hit_platform_y != []:
        if y_inc >= 0: # location where mario hits platform may be inside it
            mario.rect.bottom = platform.rect.top
            y_inc = 0 # in case mario walks off platform
        elif y_inc < 0: # mario always moving upward from below
            mario.rect.top = platform.rect.bottom # bonks his head on platform
            y_inc = 0 # unsticks mario
        if halt == True:
            x_inc = 0
    else: # cycles, fewer for higher values of gravity
        y_inc += 0.5 # gravity, place here otherwise increment will keep running
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()