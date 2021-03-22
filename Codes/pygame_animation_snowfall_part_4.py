import pygame, random # import libraries
pygame.init() # initialize any submodules that require it
 
BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
snowflakes = [] # define a list
i = int() # optional, use range() to confine i to 0 or greater

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, example

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, size[0]+1) # random number between 0 and, including, size[0]
    y = random.randrange(0, size[1]+1) # random number between 0 and, including, size[1]
    snowflakes.append((x, y)) # create a list of random points

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # for center_point in snowflakes: # FOR each item in the list
    for i in range(0, len(snowflakes)): # FOR each index in the list, could also use range(0, 50)
        # pygame.draw.circle(screen, WHITE, center_point, radius=5, width=1)
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=5, width=1)
        # pygame.draw.circle(screen, WHITE, center_point, radius=1, width=1)
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=1, width=1)
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
pygame.quit() # needed if run module through IDLE