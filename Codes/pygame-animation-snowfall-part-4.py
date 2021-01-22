import pygame # import the Pygame library of functions
import random # for random numbers
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
snowflakes = [] # define a list
i = int() # optional, use range() to confine i to 0 or greater

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own

for i in range(0, 50): # FOR fifty snowflakes (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, size[0]+1) # random number between 0 and, including, size[0]
    y = random.randrange(0, size[1]+1) # random number between 0 and, including, size[1]
    snowflakes.append((x, y)) # append center point

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    screen.fill(BLACK) # clear the screen
    # --- Drawing code
    # for center_point in snowflakes: # FOR each item in the list
    for i in range(0, len(snowflakes)): # FOR each index in the list
        # pygame.draw.circle(screen, LIGHTGRAY, center_point, radius=3, width=0)
        pygame.draw.circle(screen, LIGHTGRAY, snowflakes[i], radius=3, width=0)
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality