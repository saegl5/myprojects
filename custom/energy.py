"""
Save Energy
"""

import pygame
import src.canvas as canvas

ticks = int() # for time stamp

def time_stamp(event):
    global ticks
    if event.type == pygame.MOUSEBUTTONUP or event.type is not pygame.MOUSEMOTION or event.type == pygame.KEYUP:
        ticks = pygame.time.get_ticks() # time stamp

def save_energy():
    if pygame.time.get_ticks() - ticks >= 10000: # inactive for 10 or more seconds
        canvas.clock.tick(1) # minimize frame rate

# keep in mind that time runs separately from frame rate