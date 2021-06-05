import pygame # import the pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
# x_offset1 = 0 # reordered, for mouse/trackpad, redundant
# y_offset1 = 0 # redundant
x_offset2 = 0 # reordered, for keyboard
y_offset2 = 0
x_increment = 0
y_increment = 0
click_sound = pygame.mixer.Sound("click4.ogg") # "Sound" must be capitalized, example

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
# pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional, do later

# --- Functions
# def draw_rect(display, COLOR, x, y, W, H, width):
#     pygame.draw.rect(display, COLOR, (x, y, W, H), width)
def draw_rect_mouse_trackpad(display, COLOR, x, y, W, H): # note "COLOR"
    # Draw a rectangle
    pygame.draw.rect(display, COLOR, (x, y, W, H), width=0)

def draw_rect_keyboard(display, COLOR, x, y, W, H):
    # Draw a rectangle
    pygame.draw.rect(display, COLOR, (x, y, W, H), width=0)
# -------------

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        else:
            # --- Mouse/keyboard events
            if action.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                # no issue with unintentional repeated mouse/trackpad clicks
            elif action.type == pygame.KEYDOWN: # "elif" means else if
                if action.key == pygame.K_RIGHT: # note "action.key"
                    pygame.key.set_repeat(10) # do here
                    x_increment = 5 # "5" is optional
                elif action.key == pygame.K_LEFT:
                    pygame.key.set_repeat(10)
                    x_increment = -5
                elif action.key == pygame.K_DOWN:
                    pygame.key.set_repeat(10)
                    y_increment = 5 # note "y_increment," and recall that y increases going downward
                elif action.key == pygame.K_UP:
                    pygame.key.set_repeat(10)
                    y_increment = -5
                elif action.key == pygame.K_RETURN:
                    # don't repeat, either
                    click_sound.play()
            elif action.type == pygame.KEYUP:
                pygame.key.set_repeat() # don't repeat
                x_increment = 0
                y_increment = 0
            # -------------------------
    # --- Game logic
    pos = pygame.mouse.get_pos() # position of mouse/trackpad cursor, returns tuple (x, y), "pos" needs to be defined here because get_pos() must be kept updated
    # x_offset = pos[0]
    x_offset1 = pos[0]-size[0]/2 # move rectangle to align mouse pointer with rectangle's upper-left corner
    # y_offset = pos[1]
    y_offset1 = pos[1]-size[1]/2
    x_offset2 += x_increment
    y_offset2 += y_increment
    if size[0]/2+x_offset1 < 0:
        x_offset1 = -size[0]/2 # prevent rectangle from passing left edge, solved for x_offset
    elif size[0]/2+x_offset1 + 64 > size[0]:
        x_offset1 = size[0]/2 - 64 + 0.5 # simplified, "0.5" due to anomaly
    if size[1]/2+y_offset1 < 0: # note "if"
        y_offset1 = -size[1]/2 # prevent rectangle from passing top edge, solved for y_offset
    elif size[1]/2+y_offset1 + 64 > size[1]:
        y_offset1 = size[1]/2 - 64 + 0.5 # simplified
    if size[0]/2+x_offset2 < 0:
        x_offset2 = -size[0]/2 # prevent rectangle from passing left edge, solved for x_offset
    elif size[0]/2+x_offset2 + 64 > size[0]:
        x_offset2 = size[0]/2 - 64 + 0.5 # simplified, "0.5" due to anomaly
    if size[1]/2+y_offset2 < 0: # note "if"
        y_offset2 = -size[1]/2 # prevent rectangle from passing top edge, solved for y_offset
    elif size[1]/2+y_offset2 + 64 > size[1]:
        y_offset2 = size[1]/2 - 64 + 0.5 # simplified
    # pygame.mouse.set_pos(size[0]/2+x_offset, size[1]/2+y_offset) # otherwise, mouse/trackpad will be out of sync with keyboard
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # pygame.draw.rect(screen, WHITE, (size[0]/2, size[1]/2, 64, 64), width=0)
    # draw_rect(screen, size[0]/2, size[1]/2, 64, 64) # call function and input parameters
    # draw_rect(screen, size[0]/2+x_offset, size[1]/2+y_offset, 64, 64) # call function, input parameters, and rely on either mouse/trackpad or keyboard
    if action.type == pygame.KEYDOWN or action.type == pygame.KEYUP:
        draw_rect_mouse_trackpad(screen, BLACK, size[0]/2+x_offset1, size[1]/2+y_offset1, 64, 64) # rely on mouse/trackpad
        draw_rect_keyboard(screen, WHITE, size[0]/2+x_offset2, size[1]/2+y_offset2, 64, 64) # rely on keyboard
    else: # either mouse/trackpad is moving or mouse/trackpad button is clicked
        draw_rect_mouse_trackpad(screen, WHITE, size[0]/2+x_offset1, size[1]/2+y_offset1, 64, 64) # rely on mouse/trackpad
        draw_rect_keyboard(screen, BLACK, size[0]/2+x_offset2, size[1]/2+y_offset2, 64, 64) # rely on keyboard
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
