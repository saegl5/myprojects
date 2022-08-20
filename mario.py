"""
"Mario" Game
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle
from custom.energy import time_stamp, save_energy
# Other modules to import

pygame.display.set_caption("QUESTABOX's \"Mario\" Game")
# pygame.key.set_repeat(10) # 10 millisecond delay between repeated key presses, smooths out movement, but mario may continually hop
# Other settings

BROWN = pygame.Color("burlywood4") # optional color, ground
WHITE = pygame.Color("white") # mario
width = 48
height = 64
ground_height = 50

ground = Rectangle(canvas.size[0], ground_height)
ground.rect.left = canvas.screen.get_rect().left
ground.rect.bottom = canvas.screen.get_rect().bottom
ground.image.fill(BROWN)
mario = Rectangle(width, height) # see classes.py
mario.rect.x = 50
mario.rect.bottom = ground.rect.top
mario.image.fill(WHITE) # example
grounds = pygame.sprite.Group()
sprites = pygame.sprite.Group() # all sprites
grounds.add(ground)
sprites.add(ground, mario) # displays mario in front of ground (order matters)

speed = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
first = True
# Other variables and constants

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        elif action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RIGHT and mario.rect.bottom > ground.rect.top-50:
                x_inc = speed
            if action.key == pygame.K_LEFT and mario.rect.bottom > ground.rect.top-50:
                x_inc = -speed
            if action.key == pygame.K_SPACE and mario.rect.bottom == ground.rect.top:
                y_inc = -2*speed # y decreases going upward
        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_LEFT and x_inc < 0 and mario.rect.bottom == ground.rect.top:
                x_inc = 0
            if action.key == pygame.K_RIGHT and x_inc > 0 and mario.rect.bottom == ground.rect.top:
                x_inc = 0
        # Other keyboard or mouse/trackpad events

        time_stamp(action)

    mario.rect.x += x_inc

    mario.rect.y += y_inc
    hit_ground = pygame.sprite.spritecollide(mario, grounds, False)
    if hit_ground != []:
        mario.rect.bottom = ground.rect.top
        if first == True:
            x_inc = 0
            first = False
    else: # proceed normally
        y_inc += 0.35 # gravity, place here otherwise increment will keep running
        first = True
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()