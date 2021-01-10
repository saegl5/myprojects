import pygame # import the Pygame library of functions
import random # import module
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
snow_list = [] # define a list

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own

for i in range(50): # snow flake count
    x = random.randrange(0, 700)
    y = random.randrange(0, 500)
    coordinates = (x, y) # by default, each point is a tuple
    L = list(coordinates) # convert each point to a list
    snow_list.append(L) # create a list of random points

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    screen.fill(BLACK) # clear the screen
    # --- Drawing code
    for i in range(len(snow_list)):
        pygame.draw.circle(screen, LIGHTGRAY, snow_list[i], radius=5)
        snow_list[i][1] += 1 # snowfall speed, increasing y by 1 pixel for each coordinate
        if snow_list[i][1] > 505: # snow flake has moved off the bottom of the screen
            # Reset it just above the top
            y = random.randrange(-50, -5)
            snow_list[i][1] = y
            # Give it a new x position
            x = random.randrange(0, 700)
            snow_list[i][0] = x
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality