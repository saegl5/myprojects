import pygame # import the pygame module
import sys # import the sys module
from math import pi, cos, sin # for drawing arcs and rotating lines

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
radius1 = 80 # define "radius" for rotating lines
radius2 = 30

pygame.display.set_caption("QUESTABOX's Cool Drawing") # title, example

while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    pygame.draw.rect(screen, WHITE, (20, 20, 40, 60), width=1)
    # (distance x from origin to top-left corner, distance y from origin to top-left corner, width, height)
    # "width" is boundary thickness, width=0 fills the rectangle
    # unit is pixels
    pygame.draw.circle(screen, WHITE, (30, 140), radius=10, width=1)
    # (30, 140) is the circle's centerpoint
    # "radius" is the distance from the circle's centerpoint to its outer edge
    # radius=0 circle disappears
    # large width also fills circle
    pygame.draw.ellipse(screen, WHITE, (20, 220, 60, 40), width=1)
    # (20, 220) is NOT the ellipse's centerpoint
    # ellipse uses rectangle boundaries, but you can use different numbers
    # large width also fills ellipse
    pygame.draw.arc(screen, WHITE, (20, 320, 50, 50), 0*pi/180, 90*pi/180, width=1)
    # arc uses rectangle boundaries too, but again you can use different numbers
    # needs a starting angle and ending angle, each in radians
    # this arc is drawn from 45 degrees to 180 degrees counterclockwise
    # radians = degrees*pi/180
    # angles can also be negative
    # width=0 arc disappears
    # large width also fills arc
    pygame.draw.line(screen, WHITE, (20, 440), (50, 470), width=4)
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin)
    pygame.draw.aaline(screen, WHITE, (220, 20), (250, 50))
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.lines(screen, WHITE, False, [(220, 380), (350, 390), (500, 380), (520, 330)], width=3)
    # example with three lines
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin),
    # (distance x2 from origin, distance y2 from origin),
    # (distance x3 from origin, distance y3 from origin)
    # "False" means the first and last points are not connected
    # "True" means they are connected
    # distances/points are nested in brackets
    # append distances/points to make more lines, remove them to make fewer lines
    pygame.draw.aalines(screen, WHITE, False, [(220, 480), (350, 490), (500, 480), (520, 430)])
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.polygon(screen, WHITE, [(220, 260), (300, 280), (320, 230)], width=1)
    # example with three sides
    # pygame.draw.lines(screen, PURPLE, True, [(300, 250), (335, 350), (450, 400)], width=1)
    # # the first and last points are connected to make third line/side
    # # could also use anti-aliased lines
    angle_offset = 0*pi/180 # initialize offset
    while angle_offset <= 360*pi/180: # loop until angle_offset = 360*pi/180 (inclusive)
        pygame.draw.line(screen, WHITE, (300, 160), (300+radius1*cos(angle_offset), 160-radius2*sin(angle_offset)), width=1) # added one offset to one set of coordinates
        angle_offset += 20*pi/180 # increment offset by 20*pi/180 each loop, shorthand for angle_offset = angle_offset + 20*pi/180
    # could have also offset x and/or y
    # initial offsets can also be nonzero (i.e., positive or negative), and so can decrements/increments
    # could also use "and" or "or" for conditional statement
    # "inclusive" means including limit, whereas "exclusive" means not including it
    # in (x, y), "x" and "y" are called coordinates
    # for decrements loop WHILE offset > or >=
    # for increments, loop WHILE offset < or <=
    # could also use a FOR loop
    # could also loop other shapes
    font = pygame.font.SysFont('Courier New', 14, bold=False, italic=False) # (font family, size [pixels], bold, italics), stylizes the text
    text1 = font.render("Rectangle:", True, WHITE) # (string, anti-aliased [i.e., thin and smooth], color), creates an image of the text
    text2 = font.render("Circle:", True, WHITE)
    text3 = font.render("Ellipse: (filled)", True, WHITE)
    text4 = font.render("Arc:", True, WHITE)
    text5 = font.render("Straight line:", True, WHITE)
    text6 = font.render("(width=4)", True, WHITE)
    text7 = font.render("Straight antialiased line:", True, WHITE)
    text8 = font.render("Loops and offsets: (example)", True, WHITE)
    text9 = font.render("Polygon:", True, WHITE)
    text10 = font.render("Multiple contiguous straight line segments: (width=3)", True, WHITE)
    text11 = font.render("Multiple contiguous straight antialiased line segments:", True, WHITE)
    screen.blit(text1, (5, 0)) # (image, position), copies the image of text onto the screen
    screen.blit(text2, (5, 100))
    screen.blit(text3, (5, 200))
    screen.blit(text4, (5, 300))
    screen.blit(text5, (5, 400))
    screen.blit(text6, (5, 420))
    screen.blit(text7, (200, 0))
    screen.blit(text8, (200, 100))
    screen.blit(text9, (200, 200))
    screen.blit(text10, (200, 300))
    screen.blit(text11, (200, 400))
    # the process of creating and copying the image is what causes the delay in opening the canvas
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second