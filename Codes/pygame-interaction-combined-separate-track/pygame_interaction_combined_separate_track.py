import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example
# can also choose your own color
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
click_sound = pygame.mixer.Sound("../pygame-interaction-part-4/click4.ogg") # "Sound" must be capitalized, example
x_offset1 = 0 # reordered, for mouse/trackpad
y_offset1 = 0
x_offset2 = 0 # reordered, for keyboard
y_offset2 = 0
x_increment = 0 # keyboard only
y_increment = 0

pygame.display.set_caption("QUESTABOX's Cool Game") # title, or choose your own

# --- Functions
def draw_circle_mouse_trackpad(screen, color, x_offset1, y_offset1):
    # Draw a circle
    pygame.draw.circle(screen, color, (0+x_offset1, 0+y_offset1), radius=25, width=1)
    pygame.draw.circle(screen, color, (0+x_offset1, 0+y_offset1), radius=1, width=1)
def draw_circle_keyboard(screen, color, x_offset2, y_offset2):
    # Draw a circle
    pygame.draw.circle(screen, color, (0+x_offset2, 0+y_offset2), radius=25, width=1)
    pygame.draw.circle(screen, color, (0+x_offset2, 0+y_offset2), radius=1, width=1)
# -------------

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        # --- Mouse events
        # elif event.type == pygame.MOUSEMOTION:
            # pygame.mouse.set_visible(True)  # show pointer
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pygame.mouse.set_visible(True)  # show pointer
            click_sound.play()
        # --- Keyboard events
        elif event.type == pygame.KEYDOWN:
            # pygame.mouse.set_visible(False)  # hide pointer
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
            else:
                None # continue
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_increment = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_increment = 0
            else:
                None # continue
        else:
            None # continue
    # --- Game logic
    pos = pygame.mouse.get_pos() # for mouse/trackpad, returns tuple (x_offset, y_offset)
    x_offset1 = pos[0]
    y_offset1 = pos[1]
    x_offset2 += x_increment
    y_offset2 += y_increment
    if 0+x_offset1 < 0:
        x_offset1 = 0 # prevent center point from passing left edge
    elif 0+x_offset1 > size[0]-1: # "-1" due to anamoly
        x_offset1 = size[0]-1
    else:
        None # continue
    if 0+y_offset1 < 0:
        y_offset1 = 0 # prevent center point from passing top edge
    elif 0+y_offset1 > size[1]-1:
        y_offset1 = size[1]-1
    else:
        None # continue
    if 0+x_offset2 < 0:
        x_offset2 = 0 # prevent center point from passing left edge
    elif 0+x_offset2 > size[0]-1:
        x_offset2 = size[0]-1
    else:
        None # continue
    if 0+y_offset2 < 0:
        y_offset2 = 0 # prevent center point from passing top edge
    elif 0+y_offset2 > size[1]-1:
        y_offset2 = size[1]-1
    else:
        None # continue
    # pygame.mouse.set_pos(x_offset1, y_offset1) # otherwise, mouse/trackpad will be out of sync with keyboard
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # draw_circle(screen, 10, 10) # numbers are offsets
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        draw_circle_mouse_trackpad(screen, BLACK, x_offset1, y_offset1) # rely on mouse/trackpad
        draw_circle_keyboard(screen, WHITE, x_offset2, y_offset2) # rely on keyboard
    else: # either mouse/trackpad is moving or mouse/trackpad button is clicked
        draw_circle_mouse_trackpad(screen, WHITE, x_offset1, y_offset1) # rely on mouse/trackpad
        draw_circle_keyboard(screen, BLACK, x_offset2, y_offset2) # rely on keyboard
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality