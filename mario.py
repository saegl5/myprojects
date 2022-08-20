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

WHITE = pygame.Color("white") # optional color, mario
BROWN = pygame.Color("burlywood4") # ground
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
sprites.add(ground, mario)

speed = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
# Other variables and constants

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        elif action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RIGHT:
                x_inc = speed
            if action.key == pygame.K_LEFT:
                x_inc = -speed
            if action.key == pygame.K_SPACE:
                y_inc = -speed # y decreases going upward
        elif action.type == pygame.KEYUP:
            x_inc = 0
            y_inc = 0 # keep?
        # Other keyboard or mouse/trackpad events

        time_stamp(action)

    mario.rect.x += x_inc
    mario.rect.y += y_inc
    hit_ground = pygame.sprite.spritecollide(mario, grounds, False)
    if hit_ground != []:
        mario.rect.bottom = ground.rect.top
    else:
        y_inc += 0.15 # gravity, place here otherwise increment will keep running
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()