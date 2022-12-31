"""
Snowfall Animation
"""

import pygame
import src.canvas as canvas
from custom.energy import time_stamp, save_energy

pygame.display.set_caption("QUESTABOX's Snowfall Animation")

WHITE = pygame.Color("white") # example
Y_INC = 1 # initialize increment
R = 4 # circle radius
background_picture = pygame.image.load('images/north_pole.jpeg').convert_alpha()
background_picture = pygame.transform.scale(background_picture, canvas.SIZE)
background_music = pygame.mixer.Sound('sounds/concerto.ogg')
snowflakes = [] # empty list

snowflakes.append((0, 0)) # populate the list with center points, (x, y)
snowflakes.append((100, 200))
snowflakes.append((400, 100))
snowflakes.append((canvas.SIZE[0], canvas.SIZE[1])) # (704, 512)
snowflakes.append((100, 400))
snowflakes.append((300, 10))
snowflakes.append((500, 300))
snowflakes.append((600, 0))
snowflakes.append((605, 120))
snowflakes.append((352, 256))

for i in range(0, len(snowflakes)): # FOR all indices (i.e., each index between 0 and, but not including, len(snowflakes))
    snowflakes[i] = list(snowflakes[i]) # each center point is a tuple, but tuples are immutable, so convert them to a list

background_music.play()

while True: # keeps screen open
    for event in pygame.event.get(): # check for user input when open screen
        if event.type == pygame.QUIT: # user clicked close button
            canvas.close()
        time_stamp(event)
    # --- Game logic
    for i in range(0, len(snowflakes)): # FOR each index in the list
        snowflakes[i][1] += Y_INC # increase y by 1 pixel for each point
        if snowflakes[i][1] > canvas.SIZE[1]+R: # IF snowflake has left the screen
            # Recreate it above the screen
            snowflakes[i][1] = -R
    # --------------
    canvas.clean() # redundant
    # --- Drawing code
    canvas.screen.blit(background_picture, (0, 0)) # copy the background picture onto the screen starting at top-left corner
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=R, width=0) # snowflakes already moved once, but oh well
    # ----------------
    canvas.show()
    save_energy()