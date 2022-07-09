"""
Constructs Sprites and Moves Aliens
"""

import pygame

BLACK = pygame.Color("black")

class Rectangle(pygame.sprite.Sprite): # make class of same class as Sprites
    def __init__(self, W, H): # constructor, "self" is like a key for sprite to access class
        super().__init__() # initialize your sprites, similar to init()
        size = (W, H) # local variable
        self.image = pygame.Surface(size) # blank image
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK) # removes background, needed for newer versions of python
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # drawing on image, not screen
        # self.image.blit(sprite_picture, (0, 0))
        self.rect = self.image.get_rect() # pair image with rectangle object, the rectangle object is your sprite
        # nutshell: drawing shape on an image, and you pair that image with a rectangle object, which is your sprite
    def update(self, px): # cannot give function/method just any name
        # global timer
        # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
        self.rect.y += px # increase sprites' rect.y by 32 pixels