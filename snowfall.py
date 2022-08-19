"""
Snowfall Animation
"""

import pygame, random
import src.canvas as canvas
from custom.energy import time_stamp, save_energy

WHITE = pygame.Color("white") # example

background_picture = pygame.image.load('images/north_pole.jpeg')
background_picture = pygame.transform.scale(background_picture, canvas.size)
snowflakes = [] # empty list
y_increment = 1 # initialize increment
r = 4 # circle radius

pygame.display.set_caption("QUESTABOX's Snowfall Animation")

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, canvas.size[0]+1) # random number between 0 and, including, size[0]
    y = random.randrange(0, canvas.size[1]+1) # random number between 0 and, including, size[1]
    snowflakes.append((x, y)) # populate the list with random center points
    snowflakes[i] = list(snowflakes[i]) # each center point is a tuple, but tuples are immutable, so convert them to a list

while True: # keeps screen open
    for action in pygame.event.get(): # check for user input when open screen
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
        time_stamp(action)
    # --- Game logic
    for i in range(0, len(snowflakes)): # FOR each index in the list
        snowflakes[i][1] += y_increment # increase y by 1 pixel for each point
        if snowflakes[i][1] > canvas.size[1]+r: # IF snowflake has left the screen
            # Recreate it above the screen
            snowflakes[i][1] = random.randrange(-50, -r) # -50 is optional
            # More randomness
            snowflakes[i][0] = random.randrange(0, canvas.size[0]+1)
    # --------------
    canvas.clean() # redundant
    # --- Drawing code
    canvas.screen.blit(background_picture, (0, 0)) # copy the background picture onto the screen starting at top-left corner
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=r, width=0) # snowflakes already moved once, but oh well
    # ----------------
    canvas.show()
    save_energy()