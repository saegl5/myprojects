"""
Saves energy (optional)
"""

import pygame
import src.canvas as canvas # works, if run from main module

ticks = int()

def snapshot(action): # capture current number of clock ticks
    global ticks
    if action.type == {pygame.KEYUP, pygame.MOUSEBUTTONUP} or action.type is not pygame.MOUSEMOTION:
        ticks = pygame.time.get_ticks()

def activate(): # if true, reduce frame rate
    if pygame.time.get_ticks() - ticks > 10000:
        canvas.clock.tick(1)