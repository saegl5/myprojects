"""
Manages frame
"""

import pygame, sys

size = (704, 512) # (width, height) in pixels, example, made size of background picture match (could also do opposite)
screen = pygame.display.set_mode(size) # set up display

def close(): # user clicked close button
    pygame.quit() # needed if run module through IDLE
    sys.exit() # exit entire process