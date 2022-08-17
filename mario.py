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

WHITE = pygame.Color("white") # optional color
width = 48
height = 64
ground_height = 50
mario = Rectangle(width, height) # see classes.py
mario.rect.x = 50
mario.rect.bottom = canvas.screen.get_rect().bottom - ground_height # could also use rect.y, canvas.size[1] and subtract mario height
mario.image.fill(WHITE) # example
sprites = pygame.sprite.Group()
sprites.add(mario)
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
    y_inc -= 0.15 # gravity
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()