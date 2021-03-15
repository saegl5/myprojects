import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

BLUE = pygame.Color("blue") # example
# can also choose your own color
WHITE = pygame.Color("white")
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# offsets are specified by mouse/trackpad position
# no increments are initialized or specified

pygame.display.set_caption("QUESTABOX's Cool Game") # title, or choose your own

# --- Functions
# def draw_circle(COLOR, x, y, radius, width):
#     pygame.draw.circle(screen, COLOR, (x, y), radius, width)
def draw_circle(x, y, radius):
    # Draw a circle
    pygame.draw.circle(screen, WHITE, (x, y), radius, width=1)
# -------------

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        else:
            None # continue
    # --- Game logic
    pos = pygame.mouse.get_pos() # position of mouse/trackpad, returns tuple (x, y)
    # x_offset = pos[0]
    x_offset = pos[0]-size[0]/2 # align mouse pointer with circles' center point
    # y_offset = pos[1]
    y_offset = pos[1]-size[1]/2
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=25, width=1)
    # draw_circle(size[0]/2, size[1]/2, 25) # call function and input parameters
    draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 25) # call function, input parameters, and rely on mouse/trackpad
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=1, width=1)
    # draw_circle(size[0]/2, size[1]/2, 1)
    draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 1)
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality