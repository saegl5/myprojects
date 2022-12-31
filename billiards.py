"""
Billiards Animation
"""

import pygame
import src.canvas as canvas
from custom.energy import time_stamp, save_energy

pygame.display.set_caption("QUESTABOX's Billiards Animation")

ball_picture = pygame.image.load('images/ball_blue_large.png').convert_alpha()
background_picture = pygame.image.load('images/background_green.png').convert_alpha() # could also simply use convert()
sound = pygame.mixer.Sound('sounds/bump.ogg')
sound.set_volume(0.125)
y = 0 # initialize position
x = 0
y_inc = 20 # initialize increment
x_inc = 20

while True: # keeps screen open
    for event in pygame.event.get(): # check for user input when open screen
        if event.type == pygame.QUIT: # user clicked close button
            canvas.close()
        time_stamp(event)
    # --- Game logic
    y += y_inc
    x += x_inc
    if y + 64 > canvas.SIZE[1]: # if rectangle would breach bottom edge
        y = canvas.SIZE[1] - 64 # prevent rectangle from breaching edge
        y_inc *= -1 # y_inc = y_inc*-1, that is change the increment's sign
        sound.play()
    elif y < 0: # else if rectangle would breach top edge
        y = 0
        y_inc *= -1 # change the increment's sign back
        sound.play()
    if x + 64 > canvas.SIZE[0]: # if rectangle would breach right edge
        x = canvas.SIZE[0] - 64
        x_inc *= -1
        sound.play()
    elif x < 0: # else if rectangle would breach left edge
        x = 0
        x_inc *= -1
        sound.play()
    if round(y_inc, 3) < 0:
        y_inc += 0.1 # friction
    elif round(y_inc, 3) > 0:
        y_inc -= 0.1 # friction
    else:
        y_inc = 0 # rounding and making zero, so ball doesn't roll in reverse
    if round(x_inc, 3) < 0:
        x_inc += 0.1 # friction
    elif round(x_inc, 3) > 0:
        x_inc -= 0.1 # friction
    else:
        x_inc = 0 # rounding and making zero, so ball doesn't roll in reverse
    # --------------
    canvas.clean() # redundant
    # --- Drawing code
    for i in range(0, canvas.SIZE[0], 64): # 64 pixels is step size, based on width of background picture
        for j in range(0, canvas.SIZE[1], 64): # again, 64 pixels is step size, but this one is based on height of background picture
            canvas.screen.blit(background_picture, (i, j)) # copy the background picture onto the screen, fills in vertically from left to right
    canvas.screen.blit(ball_picture, (x, y)) # copy the foreground picture onto the screen at (x, y)
    # ball already moved once, but oh well
    # ----------------
    canvas.show()
    save_energy()