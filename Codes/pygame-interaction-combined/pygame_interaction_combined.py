import pygame # import the Pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
y_increment = 0
click_sound = pygame.mixer.Sound("click4.ogg") # "Sound" must be capitalized, example

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example

# --- Functions
# def draw_circle(COLOR, x, y, radius, width):
#     pygame.draw.circle(screen, COLOR, (x, y), radius, width)
def draw_circle(x, y, radius):
    # Draw a circle
    pygame.draw.circle(screen, WHITE, (x, y), radius, width=1)
# -------------

while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
        # --- Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
        # ----------------
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
            elif event.key == pygame.K_RETURN:
                click_sound.play()
            else:
                None # continue
        elif event.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
        else:
            None # continue
        # -------------------
    # --- Game logic
    pos = pygame.mouse.get_pos() # position of mouse/trackpad, returns tuple (x, y)
    # x_offset = pos[0]
    x_offset = pos[0]-size[0]/2 # align mouse pointer with circles' center point
    # y_offset = pos[1]
    y_offset = pos[1]-size[1]/2
    x_offset += x_increment
    y_offset += y_increment
    if size[0]/2+x_offset < 0:
        x_offset = -size[0]/2 # prevent center point from passing left edge, solved for x_offset
    elif size[0]/2+x_offset > size[0]-1: # "-1" due to anamoly
        x_offset = size[0]-size[0]/2-1 # "-1" due to anamoly
    else:
        None # continue
    if size[1]/2+y_offset < 0: # note "if"
        y_offset = -size[1]/2 # prevent center point from passing top edge, solved for y_offset
    elif size[1]/2+y_offset > size[1]-1:
        y_offset = size[1]-size[1]/2-1
    else:
        None # continue
    pygame.mouse.set_pos(size[0]/2+x_offset, size[1]/2+y_offset) # otherwise, mouse/trackpad will be out of sync with keyboard
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=25, width=1)
    # draw_circle(size[0]/2, size[1]/2, 25) # call function and input parameters
    draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 25) # call function, input parameters, and rely on either mouse/trackpad or keyboard
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=1, width=1)
    # draw_circle(size[0]/2, size[1]/2, 1)
    draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 1)
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second