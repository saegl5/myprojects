import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
BLUE = (0, 0, 255) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
WHITE = (255, 255, 255) # example

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
snowflakes = [] # define a list

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own

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

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    for center_point in snowflakes: # FOR each item in the list
        pygame.draw.circle(screen, WHITE, center_point, radius=5, width=1)
        pygame.draw.circle(screen, WHITE, center_point, radius=1, width=1)
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality