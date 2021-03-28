import pygame
import sys
import random

pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
snowflakes = []
i = int() # optional

pygame.display.set_caption("QUESTABOX's Cool Animation")

for i in range(0, 200):
    x = random.randrange(0, size[0]+1)
    y = random.randrange(0, size[1]+1)
    snowflakes.append((x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            None
    screen.fill(BLUE)
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=3, width=0)
    pygame.display.flip()
    clock.tick(60)