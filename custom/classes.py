"""
Constructs Sprites and Moves Aliens
"""

import pygame
move_x = 0
move_y = 0

class Rectangle(pygame.sprite.Sprite): # Rectangle class of same class as sprites
    def __init__(self, w, h): # constructor, "self" is like an access key, class accepts width and height parameters, __ is pronounced "dunder"
        super().__init__() # initialize your sprites
        size = (w, h) # size of sprite's image, local variable
        self.image = pygame.Surface(size, pygame.SRCALPHA) # blank transparent image
        self.rect = self.image.get_rect() # pair image with rectangle object
    def update(self, x_inc, y_inc, limit): # cannot simply name another function/method for group
        if limit == None:
            self.rect.y += y_inc
        elif x_inc != 0:
            global move_x
            if move_x < limit:
                self.rect.x -= x_inc # recall space invaders return fire
                move_x += abs(x_inc)
            else:
                x_inc *= -1 # recall pac-man ghosts
                move_x = 0 # reset
            return x_inc, limit
        else:
            global move_y
            if move_y < limit:
                self.rect.y += y_inc
                move_y += abs(y_inc)
            else:
                y_inc *= -1
                move_y = 0
            return y_inc, limit

"""
Draws Mark
"""

class Draw(pygame.sprite.Sprite):
    def __init__(self, color, w, h):
        super().__init__()
        size = (w, h) # thicker drawing marks
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
