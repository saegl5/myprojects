import pygame # import the Pygame module
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
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    pygame.draw.line(screen, PURPLE, (100, 100), (250, 150), width=4)
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin)
    pygame.draw.aaline(screen, WHITE, (100, 150), (250, 200))
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.lines(screen, PURPLE, False, [(300, 100), (450, 150), (550, 150), (600, 100)], width=4)
    # example with three lines
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin),
    # (distance x2 from origin, distance y2 from origin),
    # (distance x3 from origin, distance y3 from origin)
    # "False" means the first and last points are not connected
    # "True" means they are connected
    # distances/points are nested in brackets
    # append distances/points to make more lines, remove them to make fewer lines
    pygame.draw.aalines(screen, WHITE, False, [(300, 150), (450, 200), (550, 200), (600, 150)])
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.polygon(screen, WHITE, [(100, 250), (125, 350), (250, 400)], width=1)
    # example with three sides
    pygame.draw.lines(screen, PURPLE, True, [(300, 250), (335, 350), (450, 400)], width=1)
    # the first and last points are connected to make third line/side
    # could also use anti-aliased lines
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second