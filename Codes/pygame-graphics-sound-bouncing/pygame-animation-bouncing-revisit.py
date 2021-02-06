import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

# BLUE = (0, 0, 255) # example, redundant
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
# WHITE = (255, 255, 255) # example, redundant

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
foreground_image = pygame.image.load("ball_blue_large.png") # foreground image from https://kenney.nl/assets/rolling-ball-assets, see License.txt; the ball is a circle, but the image of it is a rectangle
background_image = pygame.image.load("background_green.png") # background image from https://kenney.nl/assets/rolling-ball-assets, see License.txt
# offset = 0 # initialize offset earlier
y_offset = 64 # initialize offset earlier, keep starting position at top edge, was 0, then 50
x_offset = 64 # keep starting position at left edge, was 0, then 70, then 90
# increment = 64 # initialize increment early
y_increment = 64 # initialize increment early, was 50
x_increment = 64 # initialize increment early, was 70, then 126

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    # screen.fill(BLUE) # clear the screen, redundant
    for i in range(0, size[0], 64): # 64 pixels is step size, based on width of background image
        for j in range(0, size[1], 64): # again, 64 pixels is step size, but this one is based on height of background image
            screen.blit(background_image, (i, j)) # copy the background image onto the screen, fills in vertically from left to right
    # --- Drawing code
    # offset = 0 # initialize offset
    # while offset <= 448: # loop until offset = 448 (inclusive)
    #     pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # added one offset to one y-coordinate
    #     offset += 64 # offset = offset + 64
    # pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # untab
    # pygame.draw.rect(screen, WHITE, (0, 0+y_offset, 64, 64), width=1) # untab
    # pygame.draw.rect(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1) # untab
    # pygame.draw.ellipse(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1)
    screen.blit(foreground_image, (0+x_offset, 0+y_offset)) # copy the foreground image onto the screen starting at (0+x_offset, 0+y_offset)
    # offset += 64 # untab
    # offset += increment # allow the increment to change
    y_offset += y_increment # allow the increment to change
    x_offset -= x_increment # allow the increment to change, changed to decrement
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
    if 0+x_offset + 64 == size[0] or 0+x_offset == 0: # if rectangle at right or left edge
        x_increment *= -1 # x_increment = x_increment*-1, that is change the increment's sign
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
    clock.tick(10) # so can see rectangle moving, was 10, then 30
pygame.quit() # formality