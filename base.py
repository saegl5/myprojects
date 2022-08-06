"""
Base Module
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle
from custom.energy import time_stamp, save_energy
# Other modules to import

pygame.display.set_caption("Base Module")
pygame.key.set_repeat(10) # 10 millisecond delay between repeated key presses, smooths out movement
# Other settings

WHITE = pygame.Color("white") # optional color
width = 64
height = 64
player = Rectangle(width, height) # see classes.py
player.rect.x = 300
player.rect.y = 200
player.image.fill(WHITE) # example
sprites = pygame.sprite.Group()
sprites.add(player)
speed = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
# Other variables and constants

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
    
        elif action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RIGHT: # comment out any key and increment not needed
                x_inc = speed
            if action.key == pygame.K_UP:
                y_inc = -speed # y decreases going upward
            if action.key == pygame.K_LEFT:
                x_inc = -speed
            if action.key == pygame.K_DOWN:
                y_inc = speed
            if action.key == pygame.K_SPACE:
                y_inc = -speed
        elif action.type == pygame.KEYUP:
            x_inc = 0
            y_inc = 0
        # Other keyboard or mouse/trackpad events
                
        time_stamp(action)

    player.rect.x += x_inc
    player.rect.y += y_inc
    # Other game logic

    canvas.clean()

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()