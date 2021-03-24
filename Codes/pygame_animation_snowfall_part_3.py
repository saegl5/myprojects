import pygame, sys # import the Pygame and sys modules
pygame.init() # initialize any submodules that require it
 
BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
snowflakes = [] # define a list

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, example

snowflakes.append((10, 10)) # append center point, could also extend this and rest
snowflakes.append((500, 10))
snowflakes.append((100, 100))
snowflakes.append((380, 100))
snowflakes.append((5, 250))
snowflakes.append((300, 250))
snowflakes.append((500, 250))
snowflakes.append((10, 400))
snowflakes.append((200, 400))
snowflakes.append((500, 400))

while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    for center_point in snowflakes: # FOR each item in the list
        pygame.draw.circle(screen, WHITE, center_point, radius=5, width=1)
        pygame.draw.circle(screen, WHITE, center_point, radius=1, width=1)
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
pygame.quit() # needed if run module through IDLE