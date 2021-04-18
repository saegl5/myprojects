import pygame # import the pygame module
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

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional

# --- Functions
# def draw_rect(COLOR, x, y, W, H, width):
#     pygame.draw.rect(screen, COLOR, (x, y, W, H), width)
def draw_rect(x, y, W, H):
    # Draw a rectangle
    pygame.draw.rect(screen, WHITE, (x, y, W, H), width=1)
# -------------

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if action.key == pygame.K_RIGHT: # note "action.key"
                x_increment = 5 # "5" is optional
            elif action.key == pygame.K_LEFT:
                x_increment = -5
            elif action.key == pygame.K_DOWN:
                y_increment = 5 # note "y_increment," and recall that y increases going downward
            elif action.key == pygame.K_UP:
                y_increment = -5
        elif action.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
        # -------------------------
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    if size[0]/2+x_offset < 0:
        x_offset = -size[0]/2 # prevent rectangle from passing left edge, solved for x_offset
    elif size[0]/2+x_offset+25 > size[0]:
        x_offset = size[0]/2-25 # simplified
    if size[1]/2+y_offset < 0: # note "if"
        y_offset = -size[1]/2 # prevent rectangle from passing top edge, solved for y_offset
    elif size[1]/2+y_offset+25 > size[1]:
        y_offset = size[1]/2-25 # simplified
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # pygame.draw.rect(screen, WHITE, (size[0]/2, size[1]/2, 25, 25), width=1)
    # draw_rect(size[0]/2, size[1]/2, 25, 25) # call function and input parameters

    draw_rect(size[0]/2+x_offset, size[1]/2+y_offset, 25, 25) # call function, input parameters, and rely on keyboard

    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
