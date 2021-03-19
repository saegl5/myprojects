import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example
# can also choose your own color
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"

pygame.display.set_caption("QUESTABOX's Cool Canvas") # title, or choose your own

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # if run module through IDLE