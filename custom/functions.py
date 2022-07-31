"""
Connects Marks
"""

from custom.classes import Draw

def fill(previous_x, previous_y, sprite, COLOR, drawn):
    if previous_x != None: # or previous_y != None
        diff_x = sprite.rect.x - previous_x
        diff_y = sprite.rect.y - previous_y
        steps = max(abs(diff_x), abs(diff_y))
        if steps != 0: # cannot divide by zero
            dx = diff_x / steps
            dy = diff_y / steps
            for i in range(int(steps)):
                mark = Draw(COLOR)
                previous_x += dx
                previous_y += dy
                mark.rect.x = previous_x
                mark.rect.y = previous_y
                drawn.add(mark) # preserves marks from being cleared


"""
Swap Positions of Sprites
"""

def swap(sprite1, sprite2):
    x = sprite1.rect.x
    y = sprite1.rect.y
    sprite1.rect.x = sprite2.rect.x
    sprite1.rect.y = sprite2.rect.y
    sprite2.rect.x = x
    sprite2.rect.y = y


"""
Construct Outer Walls
"""

import pygame
import src.canvas as canvas  # works, if run from main module
from custom.classes import Rectangle

def outer_walls():
    sprites = pygame.sprite.Group()

    left_wall = Rectangle(1, canvas.size[1]) # need at least some thickness
    left_wall.rect.x = -1 # moved walls outside screen
    left_wall.rect.y = 0
    sprites.add(left_wall)

    right_wall = Rectangle(1, canvas.size[1])
    right_wall.rect.x = canvas.size[0]
    right_wall.rect.y = 0
    sprites.add(right_wall)

    top_wall = Rectangle(canvas.size[0]-2, 1) # no overlap
    top_wall.rect.x = 1
    top_wall.rect.y = -1
    sprites.add(top_wall)

    bottom_wall = Rectangle(canvas.size[0]-2, 1)
    bottom_wall.rect.x = 1
    bottom_wall.rect.y = canvas.size[1]
    sprites.add(bottom_wall)

    return sprites