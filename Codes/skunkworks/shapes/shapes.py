import pygame
import src.canvas as canvas # import the pygame module
from math import pi, cos, sin # for drawing arcs and rotating lines

pygame.init() # initialize any submodules that require it
 
BLUE = pygame.Color("blue") # example
BLACK = pygame.Color("black") # example
WHITE = pygame.Color("white") # example (part 1, part 2 and part 3)
RED = pygame.Color("red") # example (part 1)
GREEN = pygame.Color("green") # example (part 1)
YELLOW = pygame.Color("yellow") # example (part 1)
# PURPLE = pygame.Color("purple") # example (part 2)

clock = pygame.time.Clock() # define "clock"
radius = 100 # define "radius" for rotating lines
radius1 = 80 # define "radius" for rotating lines
radius2 = 30

pygame.display.set_caption("Shapes") # title, example

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
    # --- Game logic
    # --------------
    canvas.screen.fill(BLUE) # clear the display
    # --- Drawing code
    pygame.draw.rect(canvas.screen, WHITE, (20, 20, 40, 60), width=1)
    # (distance x from origin to top-left corner, distance y from origin to top-left corner, width, height)
    # "width" is boundary thickness, width=0 fills the rectangle
    # unit is pixels
    pygame.draw.circle(canvas.screen, WHITE, (30, 140), radius=10, width=1)
    # (30, 140) is the circle's centerpoint
    # "radius" is the distance from the circle's centerpoint to its outer edge
    # radius=0 circle disappears
    # large width also fills circle
    pygame.draw.ellipse(canvas.screen, WHITE, (20, 220, 60, 40), width=0) # was width=1
    # (20, 220) is NOT the ellipse's centerpoint
    # ellipse uses rectangle boundaries, but you can use different numbers
    # large width also fills ellipse
    pygame.draw.arc(canvas.screen, WHITE, (20, 320, 50, 50), 0*pi/180, 90*pi/180, width=1)
    # arc uses rectangle boundaries too, but again you can use different numbers
    # needs a starting angle and ending angle, each in radians
    # this arc is drawn from 45 degrees to 180 degrees counterclockwise
    # radians = degrees*pi/180
    # angles can also be negative
    # width=0 arc disappears
    # large width also fills arc
    pygame.draw.line(canvas.screen, WHITE, (20, 440), (50, 470), width=10)
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin)
    pygame.draw.aaline(canvas.screen, WHITE, (220, 20), (250, 50))
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.lines(canvas.screen, WHITE, False, [(220, 380), (350, 390), (500, 380), (520, 330)], width=3)
    # example with three lines
    # (distance x0 from origin, distance y0 from origin),
    # (distance x1 from origin, distance y1 from origin),
    # (distance x2 from origin, distance y2 from origin),
    # (distance x3 from origin, distance y3 from origin)
    # "False" means the first and last points are not connected
    # "True" means they are connected
    # distances/points are nested in brackets
    # append distances/points to make more lines, remove them to make fewer lines
    pygame.draw.aalines(canvas.screen, WHITE, False, [(220, 480), (350, 490), (500, 480), (520, 430)])
    # anti-aliased (i.e., thin and smooth)
    pygame.draw.polygon(canvas.screen, WHITE, [(220, 260), (300, 280), (320, 230)], width=1)
    # example with three sides
    # pygame.draw.lines(screen, PURPLE, True, [(300, 250), (335, 350), (450, 400)], width=1)
    # # the first and last points are connected to make third line/side
    # # could also use anti-aliased lines
    # pygame.draw.line(screen, PURPLE, (100, 100), (250, 150), width=4) # without the loop
    # y_offset = 0 # initialize offset
    # while y_offset < 50: # loop until y_offset = 50 (exclusive)
    #     pygame.draw.line(screen, PURPLE, (100, 100+y_offset), (250, 150+y_offset), width=4) # added an offset
    #     y_offset += 10 # increment offset by 10 each loop, shorthand for y_offset = y_offset+10
    # could have offset x, instead of y
    # "exclusive" means not including limit
    # offsets can also be decremented
    # x_offset = 0 # initialize offsets
    # y_offset = 0
    # while x_offset >= -20 or y_offset < 50: # loop until x_offset = -20 (inclusive) or y_offset = 50 (exclusive)
    #     pygame.draw.line(screen, PURPLE, (100+x_offset, 100+y_offset), (250+x_offset, 150+y_offset), width=4) # added another offset
    #     x_offset -= 5 # decrement offset by 5 each loop, shorthand for x_offset = x_offset - 5
    #     y_offset += 10
    # initial offsets can also be nonzero (i.e., positive or negative)
    # decrements/increments can also be negative
    # could also use "and" instead of "or"
    # could also loop until just one offset reaches limit
    # do not need to offset both coordinates
    # in (x, y), "x" and "y" are called coordinates
    # for decrements loop WHILE offset > or >=
    # for increments, loop WHILE offset < or <=
    # x_offset = 100 # initialize offsets
    # y_offset = 0
    # while y_offset < 80: # loop until y_offset = 80 (exclusive)
    #     pygame.draw.line(screen, PURPLE, (100+x_offset, 100+y_offset), (250, 150+y_offset), width=4) # removed offset from one x-coordinate
    #     x_offset -= 5 # old: if outside loop and relies on mouse, trackpad or keyboard input, becomes game logic
    #     y_offset += 10 # old: if outside loop and relies on mouse, trackpad or keyboard input, becomes game logic
    # could also use a FOR loop
    # could also loop other shapes
    # # can also offset angles
    angle_offset = 0*pi/180 # initialize offset
    while angle_offset <= 360*pi/180: # loop until angle_offset = 360*pi/180 (inclusive)
        pygame.draw.line(canvas.screen, WHITE, (300, 160), (300+radius1*cos(angle_offset), 160-radius2*sin(angle_offset)), width=1) # added one offset to one set of coordinates
        angle_offset += 20*pi/180 # increment offset by 20*pi/180 each loop, shorthand for angle_offset = angle_offset+20*pi/180
    # could have also offset x and/or y
    # initial offsets can also be nonzero (i.e., positive or negative), and so can decrements/increments
    # could also use "and" or "or" for conditional statement
    # "inclusive" means including limit, whereas "exclusive" means not including it
    # angle_offset = 0*pi/180
    # while angle_offset <= 360*pi/180: # loop until angle_offset = 360*pi/180 (inclusive)
    #     pygame.draw.line(screen, PURPLE, (100, 100), (250+radius*cos(angle_offset), 150-radius*sin(angle_offset)), width=4)
    #     angle_offset += 20*pi/180
    # you can use two radii, as well
    font = pygame.font.SysFont('Courier New', 14, bold=False, italic=False) # (font family, size [pixels], bold, italics), stylizes the text
    text1 = font.render("Rectangle:", True, WHITE) # (string, anti-aliased [i.e., thin and smooth], color), creates an image of the text
    text2 = font.render("Circle:", True, WHITE)
    text3 = font.render("Ellipse: (filled)", True, WHITE)
    text4 = font.render("Arc:", True, WHITE)
    text5 = font.render("Straight line:", True, WHITE)
    text6 = font.render("(width=10)", True, WHITE)
    text7 = font.render("Straight antialiased line:", True, WHITE)
    text8 = font.render("Loops and offsets: (example)", True, WHITE)
    text9 = font.render("Polygon:", True, WHITE)
    text10 = font.render("Multiple contiguous straight line segments: (width=3)", True, WHITE)
    text11 = font.render("Multiple contiguous straight antialiased line segments:", True, WHITE)
    canvas.screen.blit(text1, (5, 0)) # (image, position), copies the image of text onto the screen
    canvas.screen.blit(text2, (5, 100))
    canvas.screen.blit(text3, (5, 200))
    canvas.screen.blit(text4, (5, 300))
    canvas.screen.blit(text5, (5, 400))
    canvas.screen.blit(text6, (5, 420))
    canvas.screen.blit(text7, (200, 0))
    canvas.screen.blit(text8, (200, 100))
    canvas.screen.blit(text9, (200, 200))
    canvas.screen.blit(text10, (200, 300))
    canvas.screen.blit(text11, (200, 400))
    # the process of creating and copying the image is what causes the delay in opening the canvas
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second