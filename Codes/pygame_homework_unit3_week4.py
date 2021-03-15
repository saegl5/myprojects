import pygame
pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

pygame.display.set_caption("QUESTABOX's Cool Game")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLUE)
    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-size[0]/2-25 # "-25" is optional
    y_offset = pos[1]-size[1]/2-25 # "-25" is optional
    pygame.draw.rect(screen, WHITE, (size[0]/2+x_offset, size[1]/2+y_offset, 50, 50), width=1)
    pygame.draw.rect(screen, WHITE, (size[0]/2+25+x_offset, size[1]/2+25+y_offset, 1, 1), width=1) # optional
    pygame.display.flip()
    clock.tick(60)
pygame.quit()