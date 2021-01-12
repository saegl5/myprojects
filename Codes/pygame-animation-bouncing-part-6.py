import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

LIGHTGRAY = (211, 211, 211) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
BLACK = (0, 0, 0) # example

# size = (700, 500) # (width, height) in pixels
size = (700, 400) # changed height, so rectangle can bounce around more (could also have changed width or rectangle width or height)
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# offset = 0 # initialize offset earlier
y_offset = 50 # initialize offset earlier, keep starting position at top edge, was 0
x_offset = 126 # keep starting position at left edge, was 0, then 70
# increment = 50 # initialize increment early
y_increment = 50 # initialize increment early
x_increment = 126 # initialize increment early, was 70

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own
 
while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    screen.fill(LIGHTGRAY) # clear the screen
    # --- Drawing code
    # offset = 0 # initialize offset
    # while offset <= 450: # loop until offset = 450 (inclusive)
    #     pygame.draw.rect(screen, BLACK, (0, 0+offset, 70, 50), width=0) # added one offset to one y-coordinate
    #     offset += 50 # offset = offset + 50
    # pygame.draw.rect(screen, BLACK, (0, 0+offset, 70, 50), width=0) # untab
    # pygame.draw.rect(screen, BLACK, (0, 0+y_offset, 70, 50), width=0) # untab
    pygame.draw.rect(screen, BLACK, (0+x_offset, 0+y_offset, 70, 50), width=0) # untab
    # offset += 50 # untab
    # offset += increment # allow the increment to change
    y_offset += y_increment # allow the increment to change
    x_offset -= x_increment # allow the increment to change, changed to decrement
    # if 0+offset + 50 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 50 == size[1]: # if rectangle at bottom edge
    if 0+y_offset + 50 == size[1] or 0+y_offset == 0: # if rectangle at bottom or top edge
        # increment *= -1 # increment = increment*-1, that is change the increment's sign
        y_increment *= -1 # y_increment = y_increment*-1, that is change the increment's sign
    # elif 0+offset == 0: # else if rectangle at top edge
    # elif 0+y_offset == 0: # else if rectangle at top edge
        # increment *= -1 # change the increment's sign back
        # y_increment *= -1 # change the increment's sign back
    if 0+x_offset + 70 == size[0] or 0+x_offset == 0: # if rectangle at right or left edge
        x_increment *= -1 # x_increment = x_increment*-1, that is change the increment's sign
    # elif 0+x_offset == 0: # else if rectangle at left edge
    #     x_increment *= -1 # change the increment's sign back
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
    clock.tick(1) # so can see rectangle moving, was 10, then 30
pygame.quit() # formality