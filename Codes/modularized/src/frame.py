"""
Opens frame
"""

import pygame
import sys

size = (704, 512)
pygame.display.set_mode(size)

def open(action): # keep open unless action taken
    if action.type == pygame.QUIT:
        pygame.quit()
        sys.exit()