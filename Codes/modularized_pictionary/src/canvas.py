"""
Manages frame
"""

import pygame, sys

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display

def close(): # user clicked close button
    pygame.quit() # needed if run module through IDLE
    sys.exit() # exit entire process    



"""
Decorates frame
"""

pygame.init()

BLUE = pygame.Color("blue")

clock = pygame.time.Clock()

def clean(): # wipe the frame
    screen.fill(BLUE)

def show(): # showcase your work
    pygame.display.flip()
    clock.tick(60)