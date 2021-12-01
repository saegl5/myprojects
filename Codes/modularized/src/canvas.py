"""
Decorates frame
"""

import pygame
import src.frame as frame

pygame.init()

BLUE = pygame.Color("blue")

screen = pygame.display.set_mode(frame.size)
clock = pygame.time.Clock()

def clean(): # wipe the frame
    screen.fill(BLUE)

def show(): # showcase your work
    pygame.display.flip()
    clock.tick(60)