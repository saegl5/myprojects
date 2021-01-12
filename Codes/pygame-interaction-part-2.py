import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
LIGHTGRAY = (211, 211, 211) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
BLACK = (0, 0, 0)
 
size = (700, 500) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
y_increment = 0

pygame.display.set_caption("QUESTABOX's Cool Game") # title, or choose your own

# --- Functions
def draw_snowman(screen, x_offset, y_offset):
    # Draw a circle for the head
    pygame.draw.ellipse(screen, LIGHTGRAY, [35+x_offset, 0+y_offset, 25, 25])
    # Draw the middle snowman circle
    pygame.draw.ellipse(screen, LIGHTGRAY, [23+x_offset, 20+y_offset, 50, 50])
    # Draw the bottom snowman circle
    pygame.draw.ellipse(screen, LIGHTGRAY, [0+x_offset, 65+y_offset, 100, 100])
# -------------

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        # --- Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # note "event.key"
                x_increment = -5
            elif event.key == pygame.K_RIGHT:
                x_increment = 5
            elif event.key == pygame.K_UP: # recall that y increases going downward
                y_increment = -5 # note "y_increment"
            elif event.key == pygame.K_DOWN:
                y_increment = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_increment = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_increment = 0
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    if 0+x_offset < 0:
        x_offset = 0 # prevent shape from passing left edge, based on bottom snowman circle
    elif 0+x_offset + 100 > size[0]:
        x_offset = size[0] - 100 # from x_offset + 100 = size[0], solved for x_offset
    if 0+y_offset < 0:
        y_offset = 0 # prevent shape from passing top edge, based on circle for the head
    elif 0+y_offset + 165 > size[1]:
        y_offset = size[1] - 165 # based on circle for the head, middle snowman circle, and bottom snowman circle, subtracted overlap
    # --------------
    screen.fill(BLACK) # clear the screen
    # --- Drawing code
    # draw_snowman(screen, 10, 10) # numbers are offsets
    draw_snowman(screen, x_offset, y_offset) # rely on keyboard
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality