import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

LIGHTGRAY = (211, 211, 211) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
BLACK = (0, 0, 0) # example

size = (700, 500) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# offset = 0 # initialize offset earlier
# offset = 100 # start below top edge
y_offset = 100 # start below top edge
x_offset = 0 # keep starting position at left edge
# change = 50 # initialize increment early
y_change = 50 # initialize increment early
x_change = 70 # initialize increment early

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own
 
while not done: # meaning while true, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit While loop on next loop, loop will not run while false
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
    # offset += change # allow the increment to change
    y_offset += y_change # allow the increment to change
    x_offset += x_change # allow the increment to change
    # if 0+offset + 50 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 50 == size[1]: # if rectangle at bottom edge
    if 0+y_offset + 50 == size[1] or 0+y_offset == 100: # if rectangle at bottom or top edge
        # change *= -1 # change = change*-1, that is change the increment's sign
        y_change *= -1 # y_change = y_change*-1, that is change the increment's sign
    # if 0+offset == 0: # if rectangle at top edge
    # if 0+offset == 100: # if rectangle below top edge
    # if 0+y_offset == 100: # if rectangle below top edge
        # change *= -1 # change the increment's sign back
        # y_change *= -1 # change the increment's sign back
    if 0+x_offset + 70 == size[0] or 0+x_offset == 0: # if rectangle below right or left edge
        x_change *= -1 # x_change = x_change*-1, that is change the increment's sign
    # if 0+x_offset == 0: # if rectangle below left edge
    #     x_change *= -1 # change the increment's sign back
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through While loop each second)
    clock.tick(10) # so can see rectangle moving
pygame.quit() # formality