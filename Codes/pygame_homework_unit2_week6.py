import pygame, sys, random
pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

size = (704, 512)
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            None
    screen.fill(BLUE)
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=3, width=0)
        snowflakes[i][1] += 1
        if snowflakes[i][1] > size[1]+3:
            snowflakes[i][1] = random.randrange(-50, -3) # -50 is optional
        else:
            None
    pygame.display.flip()
    clock.tick(60)
pygame.quit()