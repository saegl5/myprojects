import pygame # import the pygame module
import sys # import the sys module
# from math import pi # for drawing arcs

pygame.init() # initialize any submodules that require it
 
BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white") # example (part 1, part 2 and part 3)
RED = pygame.Color("red") # example (part 1)
GREEN = pygame.Color("green") # example (part 1)
YELLOW = pygame.Color("yellow") # example (part 1)
PURPLE = pygame.Color("purple") # example (part 2)

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"

pygame.display.set_caption("QUESTABOX's Cool Drawing") # title, example

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # pygame.draw.line(screen, PURPLE, (100, 100), (250, 150), width=4) # without the loop
    # y_offset = 0 # initialize offset
    # while y_offset < 50: # loop until y_offset = 50 (exclusive)
    #     pygame.draw.line(screen, PURPLE, (100, 100+y_offset), (250, 150+y_offset), width=4) # added an offset
    #     y_offset += 10 # increment offset by 10 each loop, shorthand for y_offset = y_offset+10
    # # could have offset x, instead of y
    # # "exclusive" means not including limit
    # # offsets can also be decremented
    # x_offset = 0 # initialize offsets
    # y_offset = 0
    # while x_offset >= -20 or y_offset < 50: # loop until x_offset = -20 (inclusive) or y_offset = 50 (exclusive)
    #     pygame.draw.line(screen, PURPLE, (100+x_offset, 100+y_offset), (250+x_offset, 150+y_offset), width=4) # added another offset
    #     x_offset -= 5 # decrement offset by 5 each loop, shorthand for x_offset = x_offset - 5
    #     y_offset += 10
    # # initial offsets can also be nonzero (i.e., positive or negative)
    # # decrements/increments can also be negative
    # # could also use "and" instead of "or"
    # # could also loop until just one offset reaches limit
    # # do not need to offset both coordinates
    # # in (x, y), "x" and "y" are called coordinates
    # # for decrements loop WHILE offset > or >=
    # # for increments, loop WHILE offset < or <=
    x_offset = 100 # initialize offsets
    y_offset = 0
    while y_offset < 80: # loop until y_offset = 80 (exclusive)
        pygame.draw.line(screen, PURPLE, (100+x_offset, 100+y_offset), (250, 150+y_offset), width=4) # removed offset from one x-coordinate
        x_offset -= 5 # if outside loop and relies on mouse, trackpad or keyboard input, becomes game logic
        y_offset += 10 # if outside loop and relies on mouse, trackpad or keyboard input, becomes game logic
    # could also use a FOR loop
    # could also loop other shapes
    # can also offset angles
    font = pygame.font.SysFont('Courier New', 16, bold=False, italic=False) # (font family, size [pixels], bold, italics), stylizes the text
    text = font.render("Hello world!", True, WHITE) # (string, anti-aliased [i.e., thin and smooth], color), creates an image of the text
    screen.blit(text, (400, 100)) # (image, position), copies the image of text onto the screen
    # the process of creating and copying the image is what causes the delay in opening the canvas
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second