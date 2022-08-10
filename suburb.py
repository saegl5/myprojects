"""
Suburb Drawing
"""

import pygame
import src.canvas as canvas
from custom.heart import heart
from math import pi, cos, sin

GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color("yellow")
WHITE = pygame.Color("white")
DARKGRAY = pygame.Color("darkgray")
BLACK = pygame.Color("black")
RED = pygame.Color("red")
 
pygame.display.set_caption("QUESTABOX's Suburb Drawing")

while True: # keeps screen open
    for action in pygame.event.get(): # check for user input when open screen
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
    # --- Game logic
    # --------------
    canvas.clean()
    # --- Drawing code    
    pygame.draw.rect(canvas.screen, GREEN, (0, 400, 704, 112), width=0) # grass
    pygame.draw.aaline(canvas.screen, BLACK, (0, 400), (704, 400)) # outline of grass

    pygame.draw.rect(canvas.screen, GRAY, (200, 300, 100, 100), width=0) # building
    pygame.draw.aalines(canvas.screen, BLACK, False, [(280, 300), (200, 300), (200, 400), (280, 400), (280, 300), (300, 300), (300, 400), (280, 400)]) # outline of building, could also use pygame.draw.lines() with width=1
    
    pygame.draw.arc(canvas.screen, DARKGRAY, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=25) # moon, if you want a more solidly colored moon then draw circle and cover half
    pygame.draw.arc(canvas.screen, BLACK, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=1) # outline around half the moon
    pygame.draw.aaline(canvas.screen, BLACK, (275, 150), (275, 200)) # outline of left side of moon

    pygame.draw.polygon(canvas.screen, BLACK, [(400, 400), (380, 512), (460, 512), (440, 400)], width=0) # road
    pygame.draw.line(canvas.screen, WHITE, (405, 400), (385, 512), width=1) # left shoulder of road
    pygame.draw.line(canvas.screen, WHITE, (455, 512), (435, 400), width=1) # right shoulder of road
    # road center lines
    y_offset = 0
    while y_offset <= 112:
        pygame.draw.line(canvas.screen, WHITE, (419, 400+y_offset), (419, 410+y_offset), width=4)
        y_offset += 20

    pygame.draw.ellipse(canvas.screen, WHITE, (400, 100, 200, 100), width=0) # bottom-left of cloud
    pygame.draw.ellipse(canvas.screen, WHITE, (450, 50, 200, 100), width=0) # top of cloud
    pygame.draw.ellipse(canvas.screen, WHITE, (500, 100, 200, 100), width=0) # bottom-right of cloud
    pygame.draw.ellipse(canvas.screen, BLACK, (400, 100, 200, 100), width=1) # outline of bottom-left of cloud
    pygame.draw.ellipse(canvas.screen, BLACK, (450, 50, 200, 100), width=1) # outline of top of cloud
    pygame.draw.ellipse(canvas.screen, BLACK, (500, 100, 200, 100), width=1) # outline of bottom-right of cloud, but the outlines will overlap
    pygame.draw.ellipse(canvas.screen, WHITE, (410, 110, 180, 80), width=0) # cover bottom-left of cloud outlines
    pygame.draw.ellipse(canvas.screen, WHITE, (460, 60, 180, 80), width=0) # cover top of cloud outlines
    pygame.draw.ellipse(canvas.screen, WHITE, (510, 110, 180, 80), width=0) # cover bottom-right of cloud outlines
    
    # text
    font = pygame.font.SysFont('Courier New', 16, bold=True, italic=False)
    text = font.render("There is hope!", True, BLACK)
    canvas.screen.blit(text, (475, 125))
    
    pygame.draw.circle(canvas.screen, YELLOW, (100, 100), radius=50, width=0) # sun
    pygame.draw.circle(canvas.screen, BLACK, (100, 100), radius=50, width=1) # outline of sun
    # sun rays (HARD!)
    angle_offset = 0*pi/180
    while angle_offset <= 360*pi/180:
        pygame.draw.line(canvas.screen, YELLOW, (100, 100), (100+100*cos(angle_offset), 100-100*sin(angle_offset)), width=2)
        angle_offset += 20*pi/180

    heart(500, 300) # balloon (HARDER!!)
    pygame.draw.arc(canvas.screen, RED, (499, 298, 25, 50), 180*pi/180, 275*pi/180, width=2) # balloon string
    # ----------------
    canvas.show()