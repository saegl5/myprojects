import pygame, sys
pygame.init()
 
BLUE = pygame.Color("blue")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Canvas")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            None
    screen.fill(BLUE)
    pygame.display.flip()
    clock.tick(60)