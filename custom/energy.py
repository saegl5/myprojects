"""
Save Energy
"""

import pygame
import src.canvas as canvas

ticks = int() # for time stamp

def time_stamp(action):
    global ticks
    if action.type == pygame.MOUSEBUTTONUP or action.type is not pygame.MOUSEMOTION or action.type == pygame.KEYUP:
        ticks = pygame.time.get_ticks() # time stamp

def save_energy():
    if pygame.time.get_ticks() - ticks >= 10000: # inactive for 10 or more seconds
        canvas.clock.tick(1) # minimize frame rate

# keep in mind that time runs separately from frame rate