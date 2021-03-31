import pygame # import the pygame module
import sys # import the sys module

size = (704, 512) # (width, height) in pixels, example
pygame.display.set_mode(size) # set up display

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process