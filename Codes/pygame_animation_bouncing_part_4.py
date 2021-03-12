import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

BLUE = pygame.Color("blue") # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# offset = 0 # initialize offset earlier
y_offset = 0 # initialize offset earlier, keep starting position at top edge
x_offset = 0 # keep starting position at left edge
# increment = 64 # initialize increment early
y_increment = 64 # initialize increment early
x_increment = 64 # initialize increment early

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
    # pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # untab
    # pygame.draw.rect(screen, WHITE, (0, 0+y_offset, 64, 64), width=1) # untab
    pygame.draw.rect(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1) # untab
    pygame.draw.ellipse(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1)
    # offset += 64 # untab, if relies on mouse, trackpad or keyboard input becomes game logic
    # offset += increment # allow the increment to change
    y_offset += y_increment # allow the increment to change
    x_offset += x_increment # allow the increment to change
    # if 0+offset + 64 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == size[1]: # if rectangle at bottom edge
        # increment *= -1 # increment = increment*-1, that is change the increment's sign
        # y_increment *= -1 # y_increment = y_increment*-1, that is change the increment's sign
    # elif 0+offset == 0: # else if rectangle at top edge
    # elif 0+y_offset == 0: # else if rectangle at top edge
        # increment *= -1 # change the increment's sign back
        # y_increment *= -1 # change the increment's sign back
    if 0 + y_offset + 64 == size[1] or 0 + y_offset == 0:  # if rectangle at bottom or top edge
        y_increment *= -1  # y_increment = y_increment*-1, that is change the increment's sign
    # if 0+x_offset + 64 == size[0]: # if rectangle at right edge
        # x_increment *= -1 # x_increment = x_increment*-1, that is change the increment's sign
    # elif 0+x_offset == 0: # else if rectangle at left edge
        # x_increment *= -1 # change the increment's sign back
    if 0+x_offset + 64 == size[0] or 0+x_offset == 0: # if rectangle at right or left edge
        x_increment *= -1 # x_increment = x_increment*-1, that is change the increment's sign
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
    clock.tick(10) # so can see rectangle moving
pygame.quit() # formality