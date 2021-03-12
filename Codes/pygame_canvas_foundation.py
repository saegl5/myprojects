import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example
# can also choose your own color
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size

pygame.event.get() # open window briefly 
screen.fill(BLUE) # clear the screen
pygame.display.flip() # update the screen