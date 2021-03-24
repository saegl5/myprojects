import pygame, sys
from math import pi
pygame.init()
 
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color("yellow")
WHITE = pygame.Color("white")
DARKGRAY = pygame.Color("darkgray")
 
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
    pygame.draw.rect(screen, GRAY, (200, 300, 100, 100), width=0)
    pygame.draw.rect(screen, GREEN, (0, 400, 704, 112), width=0)
    pygame.draw.circle(screen, YELLOW, (100, 100), radius=50, width=0)
    pygame.draw.ellipse(screen, WHITE, (400, 100, 200, 100), width=0)
    pygame.draw.ellipse(screen, WHITE, (450, 50, 200, 100), width=0)
    pygame.draw.ellipse(screen, WHITE, (500, 100, 200, 100), width=0)
    pygame.draw.arc(screen, DARKGRAY, (250, 150, 50, 50), -90*pi/180, 90*pi/180, width=25)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()