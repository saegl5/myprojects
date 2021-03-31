import pygame # import the pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset1 = 0 # reordered, for mouse/trackpad
y_offset1 = 0
x_offset2 = 0 # reordered, for keyboard
y_offset2 = 0
x_increment = 0 # keyboard only
y_increment = 0
click_sound = pygame.mixer.Sound("click4.ogg") # "Sound" must be capitalized, example

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example

# --- Functions
# def draw_circle(COLOR, x, y, radius, width):
#     pygame.draw.circle(screen, COLOR, (x, y), radius, width)
def draw_circle_mouse_trackpad(COLOR, x1, y1, radius): # note "COLOR"
    # Draw a circle
    pygame.draw.circle(screen, COLOR, (x1, y1), radius, width=1)

def draw_circle_keyboard(COLOR, x2, y2, radius):
    # Draw a circle
    pygame.draw.circle(screen, COLOR, (x2, y2), radius, width=1)
# -------------

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        # --- Mouse events
        elif action.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
        # ----------------
        # --- Keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
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
        elif action.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
        # -------------------
    # --- Game logic
    pos = pygame.mouse.get_pos() # position of mouse/trackpad, returns tuple (x, y)
    # x_offset = pos[0]
    x_offset1 = pos[0]-size[0]/2 # align mouse pointer with circles' center point
    # y_offset = pos[1]
    y_offset1 = pos[1]-size[1]/2
    x_offset2 += x_increment
    y_offset2 += y_increment
    # if 0+x_offset1 < 0:
    #     x_offset1 = 0 # prevent center point from passing left edge
    # elif 0+x_offset1 > size[0]-1: # "-1" due to anamoly
    #     x_offset1 = size[0]-1
    # if 0+y_offset1 < 0:
    #     y_offset1 = 0 # prevent center point from passing top edge
    # elif 0+y_offset1 > size[1]-1:
    #     y_offset1 = size[1]-1
    if size[0]/2+x_offset2 < 0:
        x_offset2 = -size[0]/2 # prevent center point from passing left edge, solved for x_offset
    elif size[0]/2+x_offset2 > size[0]-1: # "-1" due to anamoly
        x_offset2 = size[0]-size[0]/2-1 # "-1" due to anamoly
    if size[1]/2+y_offset2 < 0: # note "if"
        y_offset2 = -size[1]/2 # prevent center point from passing top edge, solved for y_offset
    elif size[1]/2+y_offset2 > size[1]-1:
        y_offset2 = size[1]-size[1]/2-1
    # pygame.mouse.set_pos(size[0]/2+x_offset, size[1]/2+y_offset) # otherwise, mouse/trackpad will be out of sync with keyboard
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=25, width=1)
    # draw_circle(size[0]/2, size[1]/2, 25) # call function and input parameters
    # draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 25) # call function, input parameters, and rely on either mouse/trackpad or keyboard
    # pygame.draw.circle(screen, WHITE, (size[0]/2, size[1]/2), radius=1, width=1)
    # draw_circle(size[0]/2, size[1]/2, 1)
    # draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 1)
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        draw_circle_mouse_trackpad(BLACK, size[0]/2+x_offset1, size[1]/2+y_offset1, 25) # rely on mouse/trackpad
        draw_circle_mouse_trackpad(BLACK, size[0]/2+x_offset1, size[1]/2+y_offset1, 1)
        draw_circle_keyboard(WHITE, size[0]/2+x_offset2, size[1]/2+y_offset2, 25) # rely on keyboard
        draw_circle_keyboard(WHITE, size[0]/2+x_offset2, size[1]/2+y_offset2, 1)
    else: # either mouse/trackpad is moving or mouse/trackpad button is clicked
        draw_circle_mouse_trackpad(WHITE, size[0]/2+x_offset1, size[1]/2+y_offset1, 25) # rely on mouse/trackpad
        draw_circle_mouse_trackpad(WHITE, size[0]/2+x_offset1, size[1]/2+y_offset1, 1)
        draw_circle_keyboard(BLACK, size[0]/2+x_offset2, size[1]/2+y_offset2, 25) # rely on keyboard
        draw_circle_keyboard(BLACK, size[0]/2+x_offset2, size[1]/2+y_offset2, 1)
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second