import pygame
import random
pygame.init()

LIGHTGRAY = (211, 211, 211)
BLACK = (0, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
snowflakes = []
i = int() # optional

pygame.display.set_caption("QUESTABOX's Cool Animation")

for i in range(0, 200):
    x = random.randrange(0, size[0]+1)
    y = random.randrange(0, size[1]+1)
    snowflakes.append((x, y))
    snowflakes[i] = list(snowflakes[i])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLACK)
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(screen, LIGHTGRAY, snowflakes[i], radius=3, width=0)
        snowflakes[i][1] += 1
        if snowflakes[i][1] > size[1]+3:
            snowflakes[i][1] = random.randrange(-50, -3) # -50 is optional
            snowflakes[i][0] = random.randrange(0, size[0]+1)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()