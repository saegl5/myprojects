"""
Construct Outer Walls
"""

import src.canvas as canvas  # works, if run from main module
from custom.classes import Rectangle

def left_wall():
    wall = Rectangle(1, canvas.SIZE[1]) # need at least some thickness
    wall.rect.x = -1 # moved walls outside screen
    wall.rect.y = 0
    return wall

def right_wall():
    wall = Rectangle(1, canvas.SIZE[1])
    wall.rect.x = canvas.SIZE[0]
    wall.rect.y = 0
    return wall

def top_wall():
    wall = Rectangle(canvas.SIZE[0]-2, 1) # no overlap
    wall.rect.x = 1
    wall.rect.y = -1
    return wall

def bottom_wall():
    wall = Rectangle(canvas.SIZE[0]-2, 1)
    wall.rect.x = 1
    wall.rect.y = canvas.SIZE[1]
    return wall