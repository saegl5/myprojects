import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example, alternative style
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
WHITE = pygame.Color("white")
 
size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
click_sound = pygame.mixer.Sound("../pygame-interaction-part-4/click4.ogg") # "Sound" must be capitalized, example
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
y_increment = 0

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
        # --- Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
        # --- Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # note "event.key"
                x_increment = -7
            elif event.key == pygame.K_RIGHT:
                x_increment = 7
            elif event.key == pygame.K_UP: # recall that y increases going downward
                y_increment = -7 # note "y_increment"
            elif event.key == pygame.K_DOWN:
                y_increment = 7
            elif event.key == pygame.K_RETURN:
                click_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_increment = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_increment = 0
    # --- Game logic
    pos = pygame.mouse.get_pos() # for mouse/trackpad, returns tuple (x_offset, y_offset)
    x_offset = pos[0]
    y_offset = pos[1]
    x_offset += x_increment
    y_offset += y_increment
    if 0+x_offset < 0:
        x_offset = 0 # prevent center point from passing left edge
    elif 0+x_offset > size[0]:
        x_offset = size[0]-1
    if 0+y_offset < 0:
        y_offset = 0 # prevent center point from passing top edge
    elif 0+y_offset > size[1]:
        y_offset = size[1]-1
    pygame.mouse.set_pos(x_offset, y_offset) # otherwise, mouse/trackpad will be out of sync with keyboard
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # draw_circle(screen, 10, 10) # numbers are offsets
    draw_circle(screen, x_offset, y_offset) # rely on either mouse/trackpad or keyboard
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality