"""
Billiards Animation
"""

import pygame # import the pygame module
import src.canvas as canvas
import src.efficiency as efficiency

# WHITE = pygame.Color("white") # example, redundant

ball_picture = pygame.image.load('images/ball_blue_large.png') # foreground picture from https://kenney.nl/assets/rolling-ball-assets, see License.txt; the ball is a circle, but the picture of it is a rectangle
background_picture = pygame.image.load('images/background_green.png') # background picture from https://kenney.nl/assets/rolling-ball-assets, see License.txt
# offset = 0 # initialize offset earlier
y_offset = 0 # <- STEP 2b, initialize offset earlier, keep starting position at top edge, was 0, then 50, then 64
x_offset = 0 # <- STEP 2 (horizontal movement), keep starting position at left edge, was 0, then 70, then 90, then 100
# increment = 64 # initialize increment early
y_increment = 8 # <- STEP 4, initialize increment early, was 50, then 64
x_increment = 10 # <- STEP 4, initialize increment early, was 64, then 70, then 126 and 128 as decrement

pygame.display.set_caption("QUESTABOX's Billiards Animation") # title, example

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
        efficiency.snapshot(action)
    # --- Game logic
    # --------------
    canvas.clean() # redundant
    # --- Drawing code
    for i in range(0, canvas.size[0], 64): # 64 pixels is step size, based on width of background picture
        for j in range(0, canvas.size[1], 64): # again, 64 pixels is step size, but this one is based on height of background picture
            canvas.screen.blit(background_picture, (i, j)) # copy the background picture onto the screen, fills in vertically from left to right
    # offset = 0 # <- STEP 2a, initialize offset
    # while offset <= 448: # <- STEP 0, loop until offset = 448 (inclusive)
    #     pygame.draw.rect(canvas.screen, WHITE, (0, 0+offset, 64, 64), width=1) # added one offset to one y-coordinate
    #     offset += 64 # offset = offset+64, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
    # pygame.draw.rect(canvas.screen, WHITE, (0, 0+offset, 64, 64), width=1) # untab
    # pygame.draw.rect(canvas.screen, WHITE, (0, 0+y_offset, 64, 64), width=1) # untab
    # pygame.draw.rect(canvas.screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1) # untab <- "offset" is STEP 1 (could also offset x-coordinate), "offset" became "y_offset"
    # pygame.draw.ellipse(screen, WHITE, (0, 0+offset, 64, 64), width=1)
    # pygame.draw.ellipse(canvas.screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1)
    canvas.screen.blit(ball_picture, (0+x_offset, 0+y_offset)) # copy the foreground picture onto the screen starting at (0+x_offset, 0+y_offset)
    # offset += 64 # untab, if relies on mouse, trackpad or keyboard input becomes game logic
    # offset += increment # allow the increment to change
    y_offset += y_increment # untab, "increment" is STEP 3, "increment" became "y_increment", allow the increment to change
    x_offset += x_increment # <- STEP 3, allow the increment to change, had changed to decrement
    # if 0+offset + 64 == canvas.size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == canvas.size[1]: # <- STEP 5a, if rectangle at bottom edge
    if 0+y_offset + 64 > canvas.size[1]: # if rectangle would otherwise breach bottom edge
        # increment = 0 # stop the rectangle from moving
        # increment *= -1 # increment = increment*-1, that is change the increment's sign
        y_offset = canvas.size[1] - 64 # prevent rectangle from breaching edge
        y_increment *= -1 # y_increment = y_increment*-1, that is change the increment's sign
    # elif 0+offset == 0: # else if rectangle at top edge
    # elif 0+y_offset == 0: # <- STEP 5b, else if rectangle at top edge
    elif 0+y_offset < 0: # else if rectangle would otherwise breach top edge
        # increment *= -1 # change the increment's sign back
        y_offset = 0 # prevent rectangle from breaching edge
        y_increment *= -1 # change the increment's sign back
    # if 0+y_offset + 64 == size[1] or 0+y_offset == 0: # <- STEP 5a-b, if rectangle at bottom or top edge
    # if 0+x_offset + 64 == size[0]: # <- STEP 5a, if rectangle at right edge    
    if 0+x_offset + 64 > canvas.size[0]: # if rectangle would otherwise breach right edge
        x_offset = canvas.size[0] - 64 # prevent rectangle from breaching edge
        x_increment *= -1 # x_increment = x_increment*-1, that is change the increment's sign
    # elif 0+x_offset == 0: # <- STEP 5b, else if rectangle at left edge
    elif 0+x_offset < 0: # else if rectangle would otherwise breach left edge
        x_offset = 0 # prevent rectangle from breaching edge
        x_increment *= -1 # change the increment's sign back
    # if 0+x_offset + 64 == size[0] or 0+x_offset == 0: # <- STEP 5a-b, if rectangle at right or left edge
    # if 0+x_offset + 64 >= size[0] or 0+x_offset <= 0: # if rectangle at right or left edge
        # x_decrement *= -1 # x_increment = x_increment*-1, that is change the increment's sign, changed to decrement
    # ----------------
    canvas.show()
    efficiency.activate()