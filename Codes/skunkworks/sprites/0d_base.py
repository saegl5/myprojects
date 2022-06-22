"""
Base Module
"""

import pygame
import src.canvas as canvas

pygame.display.set_caption("Canvas")

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()