import pygame
import sys

pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Game")

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-size[0]/2-25 # "-25" is optional
    y_offset = pos[1]-size[1]/2-25 # "-25" is optional
    pygame.draw.rect(screen, WHITE, (size[0]/2+x_offset, size[1]/2+y_offset, 50, 50), width=1)
    pygame.draw.rect(screen, WHITE, (size[0]/2+25+x_offset, size[1]/2+25+y_offset, 1, 1), width=1) # optional
    pygame.display.flip()
    clock.tick(60)