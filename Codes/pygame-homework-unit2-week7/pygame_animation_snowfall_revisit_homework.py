import pygame, sys, random
pygame.init()
 
WHITE = pygame.Color("white")

size = (704, 512)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
background_image = pygame.image.load("snowman.png") # background image from https://pixabay.com/photos/snowman-blue-background-scarf-2995146/, see License.txt
snowflakes = []
i = int()
r = 4

pygame.display.set_caption("QUESTABOX's Cool Animation")

for i in range(0, 50):
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
    screen.blit(background_image, (0, 0))
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=r, width=0)
        snowflakes[i][1] += 1
        if snowflakes[i][1] > size[1]+r:
            snowflakes[i][1] = random.randrange(-50, -r)
            snowflakes[i][0] = random.randrange(0, size[0]+1)
        else:
            None
    pygame.display.flip()
    clock.tick(60)
pygame.quit()