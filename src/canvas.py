# import in main module

"""
Manages Screen
"""

import pygame, sys

size = (704, 512)
screen = pygame.display.set_mode(size)

def close(): # user clicked close button
    pygame.quit() # needed if run module through IDLE
    sys.exit() # exit entire process


"""
Decorates Screen
"""

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # optional color with which to wipe screen

clock = pygame.time.Clock()

def clean():
    screen.fill(BLUE)
# only one line, but clean() is for what fill() is used

def show():
    pygame.display.flip()
    clock.tick(60)
# show() is for what flip() is used