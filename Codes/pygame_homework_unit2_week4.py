import pygame
import sys

pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
snowflakes = []
snowflakes.append((69, 185))
snowflakes.append((246, 28))
snowflakes.append((338, 81))
snowflakes.append((459, 123))
snowflakes.append((529, 109))
snowflakes.append((671, 423))

pygame.display.set_caption("QUESTABOX's Cool Animation")

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    for center_point in snowflakes:
        pygame.draw.circle(screen, WHITE, center_point, radius=3, width=0)
    pygame.display.flip()
    clock.tick(60)