import pygame # import the Pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
offset = 0 # initialize offset earlier, keep starting position at top edge
increment = 64 # initialize increment early

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, example
 
while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # offset = 0 # initialize offset
    # while offset <= 448: # loop until offset = 448 (inclusive)
    #     pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # added one offset to one y-coordinate
    #     offset += 64 # offset = offset + 64, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
    pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # untab
    pygame.draw.ellipse(screen, WHITE, (0, 0+offset, 64, 64), width=1)
    # offset += 64 # untab, if relies on mouse, trackpad or keyboard input becomes game logic
    offset += increment # allow the increment to change
    if 0+offset + 64 == size[1]: # if rectangle at bottom edge
        increment = 0 # stop the rectangle from moving
    # ----------------
    pygame.display.flip() # update the display
    # clock.tick(60) # maximum 60 frames per second
    clock.tick(10) # so can see rectangle moving