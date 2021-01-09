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
offset = 0 # initialize offset earlier, keep starting position at top edge
increment = 50 # initialize increment early

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
    pygame.draw.rect(screen, BLACK, (0, 0+offset, 70, 50), width=0) # untab
    # offset += 50 # untab
    offset += increment # allow the increment to change
    if 0+offset + 50 == size[1]: # if rectangle at bottom edge
        increment *= -1 # increment = increment*-1, that is change the increment's sign
    if 0+offset == 0: # if rectangle at top edge
        increment *= -1 # change the increment's sign back
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through While loop each second)
    clock.tick(10) # so can see rectangle moving
pygame.quit() # formality