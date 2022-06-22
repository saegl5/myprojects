# import in base.py

"""
Manages Screen
"""

import pygame, sys

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up screen

# function
def close(): # user clicked close button
    pygame.quit() # needed if run module through IDLE
    sys.exit() # exit entire process

# functions can also be placed in a separate module



"""
Decorates Screen
"""

pygame.init() # initialize any submodules (e.g., font and mixer) that require it

BLUE = pygame.Color("blue") # optional color with which to wipe screen

clock = pygame.time.Clock()

def clean(): # wipe the screen
    screen.fill(BLUE)
# only one line, but clean() is for what fill() is used

def show(): # showcase your work
    pygame.display.flip() # literally, update the screen
    clock.tick(60) # maximum 60 frames per second
# show() is for what flip() is used