import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

BLUE = pygame.Color("blue") # example
# can also choose your own color
WHITE = pygame.Color("white")
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
y_increment = 0

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
        # --- Keyboard events
        elif event.type == pygame.KEYDOWN: # "elif" means else if
            if event.key == pygame.K_LEFT: # note "event.key"
                x_increment = -1 # "-1" is optional
            elif event.key == pygame.K_RIGHT:
                x_increment = 1
            elif event.key == pygame.K_UP: # recall that y increases going downward
                y_increment = -1  # note "y_increment," and recall that y increases going downward
            elif event.key == pygame.K_DOWN:
                y_increment = 1
            else:
                None # continue
        elif event.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
        else:
            None # continue
        # -------------------
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    if size[0]/2+x_offset < 0:
        x_offset = -size[0]/2 # prevent center point from passing left edge, solved for x_offset
    elif size[0]/2+x_offset > size[0]:
        x_offset = size[0]-size[0]/2
    else:
        None # continue
    if size[1]/2+y_offset < 0: # note "if"
        y_offset = -size[1]/2 # prevent center point from passing top edge, solved for y_offset
    elif size[1]/2+y_offset > size[1]:
        y_offset = size[1]-size[1]/2
    else:
        None # continue
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=25, width=1)
    # draw_circle(size[0]/2, size[1]/2, 25) # call function and input parameters
    draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 25) # call function, input parameters, and rely on keyboard
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=1, width=1)
    # draw_circle(size[0]/2, size[1]/2, 1)
    draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 1)
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # if run module through IDLE