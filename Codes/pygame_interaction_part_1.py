import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

BLUE = pygame.Color("blue") # example
# can also choose your own color
WHITE = pygame.Color("white")
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# offsets are defined by mouse/trackpad position
# no increments are defined

pygame.display.set_caption("QUESTABOX's Cool Game") # title, or choose your own

# --- Functions
def draw_circle(screen, x_offset, y_offset):
    # Draw a circle
    pygame.draw.circle(screen, WHITE, (0+x_offset, 0+y_offset), radius=25, width=1)
    pygame.draw.circle(screen, WHITE, (0+x_offset, 0+y_offset), radius=1, width=1)
# -------------

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    # --- Game logic
    pos = pygame.mouse.get_pos() # for mouse/trackpad, returns tuple (x_offset, y_offset)
    x_offset = pos[0]
    y_offset = pos[1]
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # draw_circle(screen, 10, 10) # numbers are offsets
    draw_circle(screen, x_offset, y_offset) # rely on mouse/trackpad
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality