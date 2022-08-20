"""
Constructs Sprites and Moves Aliens
"""

import pygame
import src.canvas as canvas

BLACK = pygame.Color("black")

class Rectangle(pygame.sprite.Sprite): # Rectangle class of same class as sprites
    def __init__(self, w, h): # constructor, "self" is like an access key, class accepts width and height parameters
        super().__init__() # initialize your sprites
        size = (w, h) # size of sprite's image, local variable
        self.image = pygame.Surface(size) # blank image
        self.image.fill(BLACK) # useful if run module on macOS
        self.image.set_colorkey(BLACK) # removes background, Windows only and newer Python
        self.rect = self.image.get_rect() # pair image with rectangle object

        # List of sprites we can bump against
        # self.level = None

    def update(self, px): # cannot simply name another function/method for group
        self.rect.y += px  
    
        # if self.y_inc == 0:
        #     self.y_inc = 1
        # else:
        #     self.y_inc += .35

        # and self.y_inc >= 0:????
     
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        # self.rect.y += 2 /* probably there is simpler way */
        # platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # self.rect.y -= 2 /* this all could be used to show spring effect */
 
        # If it is ok to jump, set our speed upwards
        # if len(platform_hit_list) > 0 or self.rect.bottom >= canvas.size[1]:


"""
Draws Mark
"""

class Draw(pygame.sprite.Sprite):
    def __init__(self, COLOR):
        super().__init__()
        size = (2, 2) # thicker drawing marks
        self.image = pygame.Surface(size)
        self.image.fill(COLOR)
        self.rect = self.image.get_rect()