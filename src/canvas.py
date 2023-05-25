# import in main module

"""
Manages Screen
"""

import pygame, sys

SIZE = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(SIZE, flags=pygame.SCALED, vsync=1) # set up screen

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
fps = 120 # 120 frames per second (max), higher fixes jitter

def clean(): # wipe the screen
    screen.fill(BLUE)
# only one line, but clean() is for what fill() is used

def show(): # showcase your work
    pygame.display.flip() # literally, update the screen
    clock.tick(fps)
# show() is for what flip() is used