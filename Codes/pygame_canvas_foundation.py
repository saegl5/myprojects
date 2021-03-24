import pygame, sys # import the Pygame and sys modules

size = (704, 512) # (width, height) in pixels, example
pygame.display.set_mode(size) # set up display

while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
        else:
            None # continue