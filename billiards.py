"""
Billiards Animation
"""

import pygame
import src.canvas as canvas
import src.efficiency as efficiency

ball_picture = pygame.image.load('images/ball_blue_large.png')
background_picture = pygame.image.load('images/background_green.png')
y_offset = 0 # initialize offset, keep starting position at top edge
x_offset = 0 # keep starting position at left edge
y_increment = 8 # initialize increment
x_increment = 10

pygame.display.set_caption("QUESTABOX's Billiards Animation")

while True: # keeps screen open
    for action in pygame.event.get(): # check for user input when open screen
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
        efficiency.snapshot(action)
    # --- Game logic
    y_offset += y_increment
    x_offset += x_increment
    if 0+y_offset + 64 > canvas.size[1]: # if rectangle would breach bottom edge
        y_offset = canvas.size[1] - 64 # prevent rectangle from breaching edge
        y_increment *= -1 # y_increment = y_increment*-1, that is change the increment's sign
    elif 0+y_offset < 0: # else if rectangle would breach top edge
        y_offset = 0
        y_increment *= -1 # change the increment's sign back
    if 0+x_offset + 64 > canvas.size[0]: # if rectangle would breach right edge
        x_offset = canvas.size[0] - 64
        x_increment *= -1
    elif 0+x_offset < 0: # else if rectangle would breach left edge
        x_offset = 0
        x_increment *= -1
    # --------------
    canvas.clean() # redundant
    # --- Drawing code
    for i in range(0, canvas.size[0], 64): # 64 pixels is step size, based on width of background picture
        for j in range(0, canvas.size[1], 64): # again, 64 pixels is step size, but this one is based on height of background picture
            canvas.screen.blit(background_picture, (i, j)) # copy the background picture onto the screen, fills in vertically from left to right
    canvas.screen.blit(ball_picture, (0+x_offset, 0+y_offset)) # copy the foreground picture onto the screen starting at (0+x_offset, 0+y_offset)
    # ball already moved once, but oh well
    # ----------------
    canvas.show()
    efficiency.activate()