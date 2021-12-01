"""
Pictionary
"""

import pygame

class Draw(pygame.sprite.Sprite):
    def __init__(self, COLOR):
        super().__init__()
        size = (2, 2) # thicker drawing marks
        self.image = pygame.Surface(size)
        self.image.fill(COLOR)
        self.rect = self.image.get_rect()