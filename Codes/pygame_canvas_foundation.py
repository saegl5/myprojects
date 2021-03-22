import pygame # import the Pygame module
pygame.init() # initialize any submodules that require it

size = (704, 512) # (width, height) in pixels, example
pygame.display.set_mode(size) # set up display

pygame.event.get() # open display
pygame.display.flip() # update the display

pygame.quit() # needed if run module through IDLE