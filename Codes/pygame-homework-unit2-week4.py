import pygame
pygame.init()

LIGHTGRAY = (211, 211, 211)
BLACK = (0, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
snowflakes = []
snowflakes.append((69, 185))
snowflakes.append((246, 28))
snowflakes.append((338, 81))
snowflakes.append((459, 123))
snowflakes.append((529, 109))
snowflakes.append((671, 423))

pygame.display.set_caption("QUESTABOX's Cool Animation")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLACK)
    for center_point in snowflakes:
        pygame.draw.circle(screen, LIGHTGRAY, center_point, radius=3, width=0)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()