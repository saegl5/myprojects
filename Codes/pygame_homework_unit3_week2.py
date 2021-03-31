import pygame
import sys
import random

pygame.init()
 
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")

size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
snowflakes = []
i = int()
r = 4
# background_image is okay

pygame.display.set_caption("QUESTABOX's Cool Animation")

for i in range(0, 50):
    x = random.randrange(0, size[0]+1)
    y = random.randrange(0, size[1]+1)
    snowflakes.append((x, y))
    snowflakes[i] = list(snowflakes[i])

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE) # background_image is okay
    for i in range(0, len(snowflakes)):
        # highlight one point, so we can track it
        pygame.draw.circle(screen, BLACK, snowflakes[i], radius=r, width=1)
        pygame.draw.circle(screen, BLACK, snowflakes[i], radius=1, width=1) # optional
        pygame.draw.circle(screen, WHITE, snowflakes[0], radius=r, width=1)
        pygame.draw.circle(screen, WHITE, snowflakes[0], radius=1, width=1) # optional
        # width=0 is okay, too
        snowflakes[i][1] += 1
        if snowflakes[i][1] > size[1]+r:
            snowflakes[i][1] = random.randrange(-50, -r)
            snowflakes[i][0] = random.randrange(0, size[0]+1) # challenge
    pygame.display.flip()
    clock.tick(60)