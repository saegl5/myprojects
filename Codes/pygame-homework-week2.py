import pygame
from math import pi
pygame.init()
 
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUEGRAY = (77, 77, 255)
 
size = (700, 500)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Drawing")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLUE)
    pygame.draw.rect(screen, GRAY, [200, 300, 100, 100], width=0)
    pygame.draw.rect(screen, GREEN, [0, 400, 700, 100], width=0)
    pygame.draw.circle(screen, YELLOW, [100, 100], radius=50, width=0)
    pygame.draw.ellipse(screen, WHITE, [400, 100, 200, 100], width=0)
    pygame.draw.ellipse(screen, WHITE, [450, 50, 200, 100], width=0)
    pygame.draw.ellipse(screen, WHITE, [500, 100, 200, 100], width=0)
    pygame.draw.arc(screen, BLUEGRAY, [250, 150, 50, 50], -90*pi/180, 90*pi/180, width=25)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()