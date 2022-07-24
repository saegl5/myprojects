"""
Constructs Sprites and Moves Aliens
"""

import pygame
# import src.canvas as canvas

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
    def update(self, px): # you cannot simply name another function/method for group
        self.rect.y += px # increase sprites' rect.y by px pixels
        #### if self.rect.y > size[1]: # IF block has left the canvas, then reset block above canvas (assumes player block has not collided with it)
            #### self.reset_position()
    #### def reset_position(self):
        ##### self.rect.y = random.randrange(-50, -20) # -50 is optional
        ##### self.rect.x = random.randrange(0, size[0]-20)
    # def lunge(self): # calling with sprite, not group
    #     if count % 2 == 0: # could also have used timer, using count because did same in pac-man
    #         self.image.blit(invader_picture_alt, (0, 0))
    #     else:
    #         self.image.blit(invader_picture, (0, 0))
    # def retry(self):
    #     self.rect.centerx = canvas.screen.get_rect().centerx # center along bottom of display
    #     self.rect.y = canvas.size[1]-h
    # def return_fire(self, index):
    #     # index = 0 # example, more randomized with random.randrange(0, len(invaders))
    #     self.rect.centerx = invaders.sprites()[index].rect.centerx # align its horizontal center with "invader" sprite's horizontal center
    #     self.rect.top = invaders.sprites()[index].rect.bottom # align its bottom with "invader" sprite's bottom
    #     # self.image = pygame.Surface((10, 20)) # can't do, if want interactions
    #     self.image.fill(RED)
    #     lasers_alt.add(self)
    #     invader_laser_sound.play()