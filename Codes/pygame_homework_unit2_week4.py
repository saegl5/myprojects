import pygame
pygame.init()

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

size = (704, 512)
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
    screen.fill(BLUE)
    for center_point in snowflakes:
        pygame.draw.circle(screen, WHITE, center_point, radius=3, width=0)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()