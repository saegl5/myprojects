"""
Constructs Sprites
"""

import pygame

BLACK = pygame.Color("black") # useful if run module on macOS

class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    # def __init__(self, COLOR, w, h): # define a constructor, class accepts COLOR, width, and height parameters, must type "__" before and after "init," requires "self"
    # def __init__(self, x, y, w, h): # define a constructor, class accepts width, height, x-coordinate, and y-coordinate parameters, must type "__" before and after "init," requires "self"
    def __init__(self, w, h): # define a constructor, class accepts width, height, x-coordinate, and y-coordinate parameters, must type "__" before and after "init," requires "self"
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (w, h) # define size of image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        # pygame.draw.rect(self.image, COLOR, (0, 0, w, h), width=0) # draw shape on image, draw over entire image with (0, 0, w, h), where (0, 0) is located at image's top-left corner
        # self.image.blit(sprite_picture, (0, 0))
        self.image.set_colorkey(BLACK) # windows only and newer python
        self.rect = self.image.get_rect() # pair image with rectangle object
        # sprite consists of image and rectangle object
        # self.rect.x = x
        # self.rect.y = y
    # def update(self):
        # self.rect.y += 32 # increase sprites' rect.y by 32 pixels
