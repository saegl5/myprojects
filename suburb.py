import pygame
import sys
import src.heart as heart
from math import pi, cos, sin

pygame.init()
 
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color("yellow")
WHITE = pygame.Color("white")
DARKGRAY = pygame.Color("darkgray")
BLACK = pygame.Color("black")
RED = pygame.Color("red")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Suburb Drawing")

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    pygame.draw.rect(screen, GRAY, (200, 300, 100, 100), width=0) # building
    pygame.draw.rect(screen, GREEN, (0, 400, 704, 112), width=0) # grass
    pygame.draw.circle(screen, YELLOW, (100, 100), radius=50, width=0) # sun
    pygame.draw.ellipse(screen, WHITE, (400, 100, 200, 100), width=0) # cloud
    pygame.draw.ellipse(screen, WHITE, (450, 50, 200, 100), width=0) # cloud
    pygame.draw.ellipse(screen, WHITE, (500, 100, 200, 100), width=0) # cloud
    pygame.draw.arc(screen, DARKGRAY, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=25) # moon
    pygame.draw.polygon(screen, BLACK, [(400, 400), (380, 512), (460, 512), (440, 400)], width=0) # road
    pygame.draw.line(screen, WHITE, (405, 400), (385, 512), width=1) # road shoulder
    pygame.draw.line(screen, WHITE, (455, 512), (435, 400), width=1) # road shoulder
    pygame.draw.aaline(screen, BLACK, (0, 400), (704, 400)) # outline grass
    pygame.draw.aalines(screen, BLACK, False, [(280, 300), (200, 300), (200, 400), (280, 400), (280, 300), (300, 300), (300, 400), (280, 400)]) # outline building, could also use pygame.draw.lines() with width=1
    pygame.draw.circle(screen, BLACK, (100, 100), radius=50, width=1) # outline sun
    pygame.draw.ellipse(screen, BLACK, (400, 100, 200, 100), width=1) # outline cloud
    pygame.draw.ellipse(screen, BLACK, (450, 50, 200, 100), width=1) # outline cloud
    pygame.draw.ellipse(screen, BLACK, (500, 100, 200, 100), width=1) # outline cloud
    pygame.draw.ellipse(screen, WHITE, (410, 110, 180, 80), width=0) # cover some cloud outline
    pygame.draw.ellipse(screen, WHITE, (460, 60, 180, 80), width=0) # cover some cloud outline
    pygame.draw.ellipse(screen, WHITE, (510, 110, 180, 80), width=0) # cover some cloud outline
    pygame.draw.arc(screen, BLACK, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=1) # outline around moon
    pygame.draw.aaline(screen, BLACK, (275, 150), (275, 200)) # outline left part of moon
    y_offset = 0 # road center lines
    while y_offset <= 112:
        pygame.draw.line(screen, WHITE, (419, 400+y_offset), (419, 410+y_offset), width=4)
        y_offset += 20
    angle_offset = 0*pi/180 # sun rays (HARD!!)
    while angle_offset <= 360*pi/180:
        pygame.draw.line(screen, YELLOW, (100, 100), (100+100*cos(angle_offset), 100-100*sin(angle_offset)), width=2)
        angle_offset += 20*pi/180
    font = pygame.font.SysFont('Courier New', 16, bold=True, italic=False)
    text = font.render("There is hope!", True, BLACK)
    screen.blit(text, (475, 125))
    heart.draw(500, 300) # balloon
    pygame.draw.arc(screen, RED, (499, 298, 25, 50), 180*pi/180, 275*pi/180, width=2) # balloon string
    pygame.display.flip()
    clock.tick(60)