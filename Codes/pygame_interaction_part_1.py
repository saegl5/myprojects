import pygame # import the pygame module
import sys # import the sys module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
 
size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
# offsets are specified by mouse/trackpad position
# no increments are initialized or specified

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example

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
    # --- Game logic
    pos = pygame.mouse.get_pos() # position of mouse/trackpad, returns tuple (x, y), "pos" needs to be defined here because get_pos() must be kept updated
    # x_offset = pos[0]
    x_offset = pos[0]-size[0]/2-25/2 # move rectangle to align mouse pointer with rectangle's center point
    # y_offset = pos[1]
    y_offset = pos[1]-size[1]/2-25/2
    if size[0]/2+x_offset <= 0:
        x_offset = -size[0]/2 # prevent rectangle from passing left edge, solved for x_offset
    elif size[0]/2+x_offset+25 >= size[0]:
        x_offset = size[0]-size[0]/2-25
    if size[1]/2+y_offset <= 0: # note "if"
        y_offset = -size[1]/2 # prevent rectangle from passing top edge, solved for y_offset
    elif size[1]/2+y_offset+25 >= size[1]:
        y_offset = size[1]-size[1]/2-25
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # pygame.draw.rect(screen, WHITE, (size[0]/2, size[1]/2, 25, 25), width=1)
    # draw_rect(size[0]/2, size[1]/2, 25, 25) # call function and input parameters
    draw_rect(size[0]/2+x_offset, size[1]/2+y_offset, 25, 25) # call function, input parameters, and rely on mouse/trackpad
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second