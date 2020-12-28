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
offset = 100 # start below top edge
change = 50 # initialize increment early
# rect_x = 50 # initialize starting x position of the rectangle
# rect_y = 50 # initialize starting y position of the rectangle
# rect_change_x = 1
# rect_change_y = 5 
# # lower number moves rectangle slower, higher moves it faster
# # # negative number changes direction

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own
 
while not done: # meaning while true, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit While loop on next loop, loop will not run while false
    screen.fill(LIGHTGRAY) # clear the screen
    # --- Drawing code
    # offset = 0 # initialize offset
    # while offset <= 400: # loop until offset = 400 (inclusive)
    #     pygame.draw.rect(screen, BLACK, (10, 0+offset, 60, 50), width=0) # added one offset to one y-coordinate
    #     offset += 50 # offset = offset + 50
    pygame.draw.rect(screen, BLACK, (10, 0+offset, 60, 50), width=0) # untab
    # offset += 50 # untab
    offset += change # allow the increment to change
    if 0+offset + 50 == 500: # if rectangle at bottom edge
        change *= -1 # change = change*-1, that is change the increment's sign
    # if 0+offset == 0: # if rectangle at top edge
    if 0+offset == 100: # if rectangle below top edge
        change *= -1 # change the increment's sign back
    # pygame.draw.rect(screen, BLACK, (rect_x, rect_y, 60, 50), width=0)
    # rect_x += rect_change_x
    # rect_y += rect_change_y
    # if rect_y > 450 or rect_y < 0:
    #     rect_change_y = rect_change_y * -1 # bounce off bottom or top edges
    # if rect_x > 640 or rect_x < 0:
    #     rect_change_x = rect_change_x * -1 # bounce off left or right edges
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through While loop each second)
    clock.tick(10) # so can see rectangle moving
pygame.quit() # formality