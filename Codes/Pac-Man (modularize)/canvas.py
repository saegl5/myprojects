"""
Manages display
"""

import pygame, sys

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display

def close(): # user clicked close button
    pygame.quit() # needed if run module through IDLE
    sys.exit() # exit entire process