"""
Constructs Sprites and Moves Aliens
"""

import pygame

BLACK = pygame.Color("black")

class Rectangle(pygame.sprite.Sprite): # Rectangle class of same class as sprites
    def __init__(self, w, h): # constructor, "self" is like an access key, class accepts width and height parameters
        super().__init__() # initialize your sprites
        size = (w, h) # size of sprite's image, local variable
        self.image = pygame.Surface(size) # blank image
        self.image.set_colorkey(BLACK) # removes background, Windows only or newer Python
        self.rect = self.image.get_rect() # pair image with rectangle object
    def update(self, px): # cannot simply name another function/method for group
        self.rect.y += px

"""
Draws Mark
"""

class Draw(pygame.sprite.Sprite):
    def __init__(self, color, w, h):
        super().__init__()
        size = (w, h) # thicker drawing marks
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()