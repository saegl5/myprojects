import pygame, random # import libraries
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example
# can also choose your own color
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
snowflakes = [] # define a list
i = int() # optional, use range() to confine i to 0 or greater

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, size[0]+1) # random number between 0 and, including, size[0]
    y = random.randrange(0, size[1]+1) # random number between 0 and, including, size[1]
    snowflakes.append((x, y)) # create a list of random points

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # for center_point in snowflakes: # FOR each item in the list
    for i in range(0, len(snowflakes)): # FOR each index in the list, could also use range(0, 50)
        # pygame.draw.circle(screen, WHITE, center_point, radius=5, width=1)
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=5, width=1)
        # pygame.draw.circle(screen, WHITE, center_point, radius=1, width=1)
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=1, width=1)
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality