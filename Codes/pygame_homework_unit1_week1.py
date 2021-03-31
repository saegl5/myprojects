import pygame
import sys

pygame.init()
 
BLUE = pygame.Color("blue")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Canvas")

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    pygame.display.flip()
    clock.tick(60)