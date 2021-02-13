import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

BLUE = (0, 0, 255) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
WHITE = (255, 255, 255) # example

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
offset = 0 # initialize offset earlier, keep starting position at top edge
increment = 64 # initialize increment early

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own
 
while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the screen
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
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
    clock.tick(10) # so can see rectangle moving
pygame.quit() # formality