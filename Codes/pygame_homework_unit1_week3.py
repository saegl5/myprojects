import pygame, sys
from math import pi
pygame.init()
 
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color("yellow")
WHITE = pygame.Color("white")
DARKGRAY = pygame.Color("darkgray")
BLACK = pygame.Color("black")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Drawing")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            None
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
    pygame.display.flip()
    clock.tick(60)
pygame.quit()