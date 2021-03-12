import pygame
pygame.init()
 
BLUE = pygame.Color("blue")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Canvas")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLUE)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()