import pygame # import the Pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"

pygame.display.set_caption("QUESTABOX's Cool Canvas") # title, example

while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
        # --- Keyboard events
        # -------------------
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second