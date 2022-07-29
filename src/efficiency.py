"""
Saves energy (optional)
"""

import pygame
import src.canvas as canvas # works, if run from main module

ticks = 0

def snapshot(action): # capture current number of clock ticks
    global ticks
    if action.type == pygame.KEYDOWN or action.type == pygame.MOUSEBUTTONDOWN or action.type == pygame.MOUSEMOTION:
        ticks = pygame.time.get_ticks() # update ticks

def activate(): # if true, reduce frame rate
    if pygame.time.get_ticks() - ticks > 10000:
        canvas.clock.tick(1)