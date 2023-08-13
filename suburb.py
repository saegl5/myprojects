"""
Suburb Drawing
"""

import pygame
import src.canvas as canvas
from custom.energy import time_stamp, save_energy
from custom.heart import heart
from math import pi, cos, sin # for drawing arcs and rotating lines

pygame.display.set_caption("QUESTABOX's Suburb Drawing")

GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color("yellow")
WHITE = pygame.Color("white")
DARKGRAY = pygame.Color("darkgray")
BLACK = pygame.Color("black")
RED = pygame.Color("red")
y_offset = 0 # road center lines
font = pygame.font.Font('/System/Library/Fonts/Supplemental/Courier New.ttf', 16)
font.set_bold(True)
font.set_italic(False)
text = font.render("There is hope!", True, BLACK)
angle_offset = 0*pi/180 # sun rays

while True: # keeps screen open
    for event in pygame.event.get(): # check for user input when open screen
        if event.type == pygame.QUIT: # user clicked close button
            canvas.close()
        time_stamp(event)
    # --- Game logic
    # --------------
    canvas.clean()
    # --- Drawing code
    pygame.draw.rect(canvas.screen, GREEN, (0, 400, 704, 112), width=0) # grass
    pygame.draw.aaline(canvas.screen, BLACK, (0, 400), (704, 400)) # outline of grass

    pygame.draw.rect(canvas.screen, GRAY, (200, 300, 100, 100), width=0) # building
    pygame.draw.aalines(canvas.screen, BLACK, False, [(280, 300), (200, 300), (200, 400), (280, 400), (280, 300), (300, 300), (300, 400), (280, 400)]) # outline of building, could also use pygame.draw.lines() with width=1
    
    pygame.draw.arc(canvas.screen, DARKGRAY, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=25) # moon, if you want a more solidly colored moon then draw circle and cover half
    pygame.draw.arc(canvas.screen, BLACK, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=1) # outline around half the moon, minimum width=1
    pygame.draw.aaline(canvas.screen, BLACK, (275, 150), (275, 200)) # outline of left side of moon

    pygame.draw.polygon(canvas.screen, BLACK, [(400, 400), (380, 512), (460, 512), (440, 400)], width=0) # road
    pygame.draw.line(canvas.screen, WHITE, (405, 400), (385, 512), width=1) # left shoulder of road
    pygame.draw.line(canvas.screen, WHITE, (455, 512), (435, 400), width=1) # right shoulder of road

    # while y_offset <= 112:
    for y_offset in range(0, 112, 20): # potential software regression
        pygame.draw.line(canvas.screen, WHITE, (419, 400+y_offset), (419, 410+y_offset), width=4)
        # y_offset += 20

    pygame.draw.ellipse(canvas.screen, WHITE, (400, 100, 200, 100), width=0) # bottom-left of cloud
    pygame.draw.ellipse(canvas.screen, WHITE, (450, 50, 200, 100), width=0) # top of cloud
    pygame.draw.ellipse(canvas.screen, WHITE, (500, 100, 200, 100), width=0) # bottom-right of cloud
    pygame.draw.ellipse(canvas.screen, BLACK, (400, 100, 200, 100), width=1) # outline of bottom-left of cloud
    pygame.draw.ellipse(canvas.screen, BLACK, (450, 50, 200, 100), width=1) # outline of top of cloud
    pygame.draw.ellipse(canvas.screen, BLACK, (500, 100, 200, 100), width=1) # outline of bottom-right of cloud, but the outlines will overlap
    pygame.draw.ellipse(canvas.screen, WHITE, (410, 110, 180, 80), width=0) # cover bottom-left of cloud outlines
    pygame.draw.ellipse(canvas.screen, WHITE, (460, 60, 180, 80), width=0) # cover top of cloud outlines
    pygame.draw.ellipse(canvas.screen, WHITE, (510, 110, 180, 80), width=0) # cover bottom-right of cloud outlines

    canvas.screen.blit(text, (475, 125))

    pygame.draw.circle(canvas.screen, YELLOW, (100, 100), radius=50, width=0) # sun, minimum radius=1
    pygame.draw.circle(canvas.screen, BLACK, (100, 100), radius=50, width=1) # outline of sun

    # HARD!
    def range_with_floats(start, stop, step): # source: https://www.edureka.co/community/93202/typeerror-float-object-cannot-be-interpreted-as-an-integer
        while stop > start:
            yield start
            start += step
    # while angle_offset <= 360*pi/180:
    for angle_offset in range_with_floats(0, 360*pi/180, 20*pi/180): # another potential software regression
        pygame.draw.line(canvas.screen, YELLOW, (100, 100), (100+100*cos(angle_offset), 100-100*sin(angle_offset)), width=2)
        # angle_offset += 20*pi/180

    heart(500, 300) # balloon (HARDER!!)
    pygame.draw.arc(canvas.screen, RED, (499, 298, 25, 50), 180*pi/180, 275*pi/180, width=2) # balloon string
    # ----------------
    canvas.show()
    save_energy()