"""
Constructs Sprites
"""

import pygame

BLACK = pygame.Color("black")

class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites
    def __init__(self, width, height): # define a constructor, class accepts width and height parameters
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (width, height) # define size of sprite's image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        self.image.set_colorkey(BLACK) # Windows only and newer python
        self.rect = self.image.get_rect() # pair image with rectangle object, where (rect.x, rect.y) is located at rectangle object's top-left corner