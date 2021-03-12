import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size

pygame.event.get() # open window briefly 
screen.fill(BLUE) # clear the screen
pygame.display.flip() # update the screen