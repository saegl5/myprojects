"""
"Mario" Game
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle
from custom.energy import time_stamp, save_energy
# Other modules to import

pygame.display.set_caption("QUESTABOX's \"Mario\" Game")
# pygame.key.set_repeat(10) # 10 millisecond delay between repeated key presses, smooths out movement, but mario may continually hop
# Other settings

BROWN = pygame.Color("burlywood4") # optional color, ground
WHITE = pygame.Color("white") # mario
# CYAN = pygame.Color("cyan") # platforms
width = 48
height = 64
ground_height = 50

ground = Rectangle(canvas.size[0], ground_height)
ground.rect.left = canvas.screen.get_rect().left # could also use rect.x = 0
ground.rect.bottom = canvas.screen.get_rect().bottom # could also use rect.y = canvas.size[1]
ground.image.fill(BROWN)
mario = Rectangle(width, height) # see classes.py
mario.rect.x = 50
mario.rect.bottom = ground.rect.top # could also use rect.y and subtract mario height
mario.image.fill(WHITE) # example
grounds = pygame.sprite.Group()
sprites = pygame.sprite.Group()
grounds.add(ground)
sprites.add(ground, mario) # order matters

speed = 5 # example
x_inc = 0 # short for "increment"
y_inc = 0
# Other variables and constants

# class Platform(pygame.sprite.Sprite):
#     """ Platform the user can jump on """
 
#     def __init__(self, width, height):
#         """ Platform constructor. Assumes constructed with user passing in
#             an array of 5 numbers like what's defined at the top of this
#             code. """
#         super().__init__()
 
#         self.image = pygame.Surface([width, height])
#         self.image.fill(CYAN)
 
#         self.rect = self.image.get_rect()
 
 
# class Level(object):
#     """ This is a generic super-class used to define a level.
#         Create a child class for each level with level-specific
#         info. """
 
#     def __init__(self, mario):
#         """ Constructor. Pass in a handle to mario. Needed for when moving platforms
#             collide with mario. """
#         self.platform_list = pygame.sprite.Group()
#         self.enemy_list = pygame.sprite.Group()
#         self.mario = mario
         
#         # Background image
#         self.background = None
 
#     # Update everythign on this level
#     def update(self):
#         """ Update everything in this level."""
#         self.platform_list.update()
#         self.enemy_list.update()
 
#     def draw(self, screen):
#         """ Draw everything on this level. """
 
#         canvas.clean()
 
#         # Draw all the sprite lists that we have
#         self.platform_list.draw(canvas.screen)
#         self.enemy_list.draw(canvas.screen)
 
 
# # Create platforms for the level
# class Level_01(Level):
#     """ Definition for level 1. """
 
#     def __init__(self, mario):
#         """ Create level 1. """
 
#         # Call the parent constructor
#         Level.__init__(self, mario)
 
#         # Array with width, height, x, and y of platform
#         level = [[210, 70, 500, 500],
#                  [210, 70, 200, 400],
#                  [210, 70, 600, 300],
#                  ]
 
#         # Go through the array above and add platforms
#         for platform in level:
#             block = Platform(platform[0], platform[1])
#             block.rect.x = platform[2]
#             block.rect.y = platform[3]
#             block.mario = self.mario
#             self.platform_list.add(block)

# # Create all the levels
# level_list = []
# level_list.append( Level_01(mario) )

# # Set the current level
# current_level_no = 0
# current_level = level_list[current_level_no]

# mario.level = current_level

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        elif action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RIGHT:
                x_inc = speed
            if action.key == pygame.K_LEFT:
                x_inc = -speed
            if action.key == pygame.K_SPACE and mario.rect.bottom == ground.rect.top:
                y_inc = -2*speed # y decreases going upward
        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_LEFT and x_inc < 0:
                x_inc = 0
            if action.key == pygame.K_RIGHT and x_inc > 0:
                x_inc = 0
        # Other keyboard or mouse/trackpad events

        time_stamp(action)

    mario.rect.x += x_inc
    # block_hit_list = pygame.sprite.spritecollide(mario, mario.level.platform_list, False)
    # for block in block_hit_list:
    #     # If we are moving right,
    #     # set our right side to the left side of the item we hit
    #     if x_inc > 0:
    #         mario.rect.right = block.rect.left
    #     elif x_inc < 0:
    #         # Otherwise if we are moving left, do the opposite.
    #         mario.rect.left = block.rect.right

    mario.rect.y += y_inc
    hit_ground = pygame.sprite.spritecollide(mario, grounds, False)
    if hit_ground != []:
        mario.rect.bottom = ground.rect.top
    else: # proceed normally
        y_inc += 0.35 # gravity, place here otherwise increment will keep running



    # mario.rect.y += y_inc # could increase precision, as did for fast pac-man because part of mario (if moving quickly) will dip below screen or platform
    # block_hit_list = pygame.sprite.spritecollide(mario, mario.level.platform_list, False)
    # for block in block_hit_list:

    #     # Reset our position based on the top/bottom of the object.
    #     if y_inc > 0:
    #         mario.rect.bottom = block.rect.top
    #     elif y_inc < 0:
    #         mario.rect.top = block.rect.bottom

    #     # Stop our vertical movement
    #     y_inc = 0

    # Update items in the level
    # current_level.update()

    # If mario gets near the right side, shift the world left (-x)
    # if mario.rect.right > canvas.size[0]:
        # mario.rect.right = canvas.size[0]

    # If mario gets near the left side, shift the world right (+x)
    # if mario.rect.left < 0:
        # mario.rect.left = 0
    # Other game logic

    canvas.clean()

    # current_level.draw(canvas.screen)
    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()