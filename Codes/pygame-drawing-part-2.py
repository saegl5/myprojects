import pygame # import the Pygame library of functions
from math import pi # for drawing arcs
pygame.init() # initialize the game engine
 
LIGHTGRAY = (211, 211, 211) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
BLACK = (0, 0, 0) # example (part 1, part 2 and part 3)
RED = (255, 0, 0) # example (part 1)
GREEN = (0, 255, 0) # example (part 1)
BLUE = (0, 0, 255) # example (part 1)
PURPLE = (255, 0, 255) # example (part 2)

size = (700, 500) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"

pygame.display.set_caption("QUESTABOX's Cool Drawing") # title, or choose your own

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    screen.fill(LIGHTGRAY) # clear the screen
    # --- Drawing code
    # pygame.draw.rect(screen, BLACK, (275, 150, 150, 200), width=1)
    # # (distance x from origin to top-left corner, distance y from origin to top-left corner, width, height)
    # # "width" is boundary thickness, width=0 fills the rectangle
    # # unit is pixels
    # pygame.draw.circle(screen, RED, (275, 150), radius=75, width=1) 
    # # (275, 150) is the circle's centerpoint
    # # "radius" is the distance from the circle's centerpoint to its outer edge
    # # radius=0 circle disappears
    # # large width also fills circle
    # pygame.draw.ellipse(screen, GREEN, (275, 150, 150, 200), width=0) 
    # # (275, 150) is NOT the ellipse's centerpoint
    # # ellipse uses rectangle boundaries, but you can use different numbers
    # # large width also fills ellipse
    # pygame.draw.arc(screen, BLUE, (275, 150, 150, 200), 45*pi/180, 180*pi/180, width=5) 
    # # arc uses rectangle boundaries too, but again you can use different numbers
    # # needs a starting angle and ending angle, each in radians
    # # this arc is drawn from 45 degrees to 180 degrees counterclockwise
    # # radians = degrees*pi/180
    # # angles can also be negative
    # # width=0 arc disappears
    # # large width also fills arc
    pygame.draw.line(screen, PURPLE, (100, 100), (250, 150), width=4)
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin)
    pygame.draw.aaline(screen, BLACK, (100, 150), (250, 200))
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
    pygame.draw.aalines(screen, BLACK, False, [(300, 150), (450, 200), (550, 200), (600, 150)])
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.polygon(screen, BLACK, [(100, 250), (125, 350), (250, 400)], width=0) 
    # example with three sides
    pygame.draw.lines(screen, PURPLE, True, [(300, 250), (335, 350), (450, 400)], width=1)
    # the first and last points are connected to make third line/side
    # could also use anti-aliased lines
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality