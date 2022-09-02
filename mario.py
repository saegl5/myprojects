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
on = True # ground or platform
# Other constants and variables

# grounds = pygame.sprite.Group()
# blocks = [ (canvas.size[0], ground_height, 0, canvas.size[1]-ground_height),
#             (300, ground_height, canvas.size[0]+100, canvas.size[1]-ground_height),
#             (500, ground_height, canvas.size[0]+500, canvas.size[1]-ground_height)
#           ]
# for block in blocks:
    # ground = Rectangle(block[0], block[1])
    # ground.rect.x = block[2]
    # ground.rect.y = block[3]
    # ground.image.fill(BROWN)
    # grounds.add(ground)
ground = Rectangle(canvas.size[0], ground_height)
ground.rect.x = 0
ground.rect.y = canvas.size[1]-ground_height
ground.image.fill(BROWN)
mario = Rectangle(w, h) # see classes.py
mario.rect.x = 50
mario.rect.bottom = canvas.size[1]-ground_height
mario.image.fill(WHITE) # example

blocks = [  (200, 50, 400, 300),
            (200, 50, 800, 250),
            (200, 50, 1300, 100),
            (200, 50, 1700, 400)
         ] # four blocks, (w, h, x, y) each, can also vary width and height, third is too hard to reach but make part for lesson
platforms = pygame.sprite.Group()
for block in blocks: # each block
    platform = Rectangle(block[0], block[1])
    platform.rect.x = block[2] # reverted to x
    platform.rect.y = block[3] # low enough for mario to jump over, reverted to y 
    platform.image.fill(YELLOW)
    platforms.add(platform)

grounds = pygame.sprite.Group()
sprites = pygame.sprite.Group() # all sprites
grounds.add(ground)
sprites.add(grounds, platforms, mario) # displays mario in front of grounds and platforms (order matters)
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
            if action.key == pygame.K_SPACE and first == True and on == True:
                y_inc = -2.5*speed # y decreases going upward
                first = False
                on = False
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
        for platform in hit_platform_x:
            if x_inc > 0:
                mario.rect.right = platform.rect.left
            elif x_inc < 0:
                mario.rect.left = platform.rect.right
    if mario.rect.left < ground.rect.left: # could also use mario.rect.x < 0
        mario.rect.left = ground.rect.left
    elif mario.rect.right >= 500: # don't use canvas.size[0] because won't be able to see ahead of you 
        move_left = mario.rect.right - 500
        ground.rect.x -= move_left
        for platform in platforms:
            platform.rect.x -= move_left
        mario.rect.right = 500 # keep mario still, also maintains correct change in movement
    elif mario.rect.left <= 200:
        if ground.rect.x < 0:
            move_right = 200 - mario.rect.left
            ground.rect.x += move_right
            for platform in platforms:
                platform.rect.x += move_right
            mario.rect.left = 200

    mario.rect.y += y_inc # mario.rect.y truncates decimal point, but okay, simply causes delay
    hit_ground_y = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_y != []:
        mario.rect.bottom = ground.rect.top
        y_inc = 0 # logical
        on = True
        if halt == True:
            x_inc = 0
    elif hit_platform_y != []:
        for platform in hit_platform_y:
            if y_inc >= 0: # location where mario hits platform may be inside it
                mario.rect.bottom = platform.rect.top
                y_inc = 0 # in case mario walks off platform
                on = True
            elif y_inc < 0: # mario always moving upward from below
                mario.rect.top = platform.rect.bottom # bonks his head on platform
                y_inc = 0 # unsticks mario
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