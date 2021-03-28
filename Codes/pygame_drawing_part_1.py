import pygame # import the Pygame module
import sys # import the sys module
from math import pi # for drawing arcs

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
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    pygame.draw.rect(screen, WHITE, (275, 150, 150, 200), width=1)
    # (distance x from origin to top-left corner, distance y from origin to top-left corner, width, height)
    # "width" is boundary thickness, width=0 fills the rectangle
    # unit is pixels
    pygame.draw.circle(screen, RED, (275, 150), radius=75, width=1) 
    # (275, 150) is the circle's centerpoint
    # "radius" is the distance from the circle's centerpoint to its outer edge
    # radius=0 circle disappears
    # large width also fills circle
    pygame.draw.ellipse(screen, GREEN, (275, 150, 150, 200), width=1)
    # (275, 150) is NOT the ellipse's centerpoint
    # ellipse uses rectangle boundaries, but you can use different numbers
    # large width also fills ellipse
    pygame.draw.arc(screen, YELLOW, (275, 150, 150, 200), 45*pi/180, 180*pi/180, width=5)
    # arc uses rectangle boundaries too, but again you can use different numbers
    # needs a starting angle and ending angle, each in radians
    # this arc is drawn from 45 degrees to 180 degrees counterclockwise
    # radians = degrees*pi/180
    # angles can also be negative
    # width=0 arc disappears
    # large width also fills arc
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second