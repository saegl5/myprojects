import pygame # import the pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
# offset = 0 # initialize offset earlier
y_offset = 64 # initialize offset earlier, keep starting position at top edge, was 0
x_offset = 100 # keep starting position at left edge, was 0, then 70
# increment = 64 # initialize increment early
y_increment = 64 # initialize increment early
x_decrement = 128 # initialize increment early, was 70, changed to decrement

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, example
 
while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # offset = 0 # initialize offset
    # while offset <= 448: # loop until offset = 448 (inclusive)
    #     pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # added one offset to one y-coordinate
    #     offset += 64 # offset = offset+64, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
    # pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # untab
    # pygame.draw.rect(screen, WHITE, (0, 0+y_offset, 64, 64), width=1) # untab
    pygame.draw.rect(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1) # untab
    pygame.draw.ellipse(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1)
    # offset += 64 # untab, if relies on mouse, trackpad or keyboard input becomes game logic
    # offset += increment # allow the increment to change
    y_offset += y_increment # allow the increment to change
    x_offset -= x_decrement # allow the increment to change, changed to decrement
    # if 0+offset + 64 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == size[1]: # if rectangle at bottom edge
        # increment *= -1 # increment = increment*-1, that is change the increment's sign
        # y_increment *= -1 # y_increment = y_increment*-1, that is change the increment's sign
    # elif 0+offset == 0: # else if rectangle at top edge
    # elif 0+y_offset == 0: # else if rectangle at top edge
        # increment *= -1 # change the increment's sign back
        # y_increment *= -1 # change the increment's sign back
    if 0+y_offset + 64 == size[1] or 0+y_offset == 0: # if rectangle at bottom or top edge
        y_increment *= -1 # y_increment = y_increment*-1, that is change the increment's sign
    # if 0+x_offset + 64 == size[0]: # if rectangle at right edge
        # x_increment *= -1 # x_increment = x_increment*-1, that is change the increment's sign
    # elif 0+x_offset == 0: # else if rectangle at left edge
    #     x_increment *= -1 # change the increment's sign back
    if 0+x_offset + 64 >= size[0] or 0+x_offset <= 0: # if rectangle at right or left edge
        x_decrement *= -1 # x_increment = x_increment*-1, that is change the increment's sign, changed to decrement
    # ----------------
    pygame.display.flip() # update the display
    # clock.tick(60) # maximum 60 frames per second
    clock.tick(1) # so can see rectangle moving, was 10, then 30