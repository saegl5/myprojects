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
# defines offsets in function call
pygame.mouse.set_visible(False) # hide pointer

pygame.display.set_caption("QUESTABOX's Cool Game") # title, or choose your own

# --- Functions
def draw_snowman(screen, x, y):
    # Draw a circle for the head
    pygame.draw.ellipse(screen, LIGHTGRAY, [35 + x, 0 + y, 25, 25])
    # Draw the middle snowman circle
    pygame.draw.ellipse(screen, LIGHTGRAY, [23 + x, 20 + y, 50, 50])
    # Draw the bottom snowman circle
    pygame.draw.ellipse(screen, LIGHTGRAY, [0 + x, 65 + y, 100, 100])
# -------------

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    # --- Game logic
    pos = pygame.mouse.get_pos() # for mouse/trackpad, returns tuple (x, y)
    x = pos[0]
    y = pos[1]
    # --------------
    screen.fill(BLACK) # clear the screen
    # --- Drawing code
    # draw_snowman(screen, 10, 10) # numbers are offsets
    draw_snowman(screen, x, y) # rely on mouse/trackpad
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality