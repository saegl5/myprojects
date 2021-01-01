import pygame, math
pygame.init()

BLACK = (0, 0 ,0)
RED = (255, 0, 0)
 
size = (100, 100)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLACK)
    # --- Drawing code
    offset1 = 20
    c_x = (25+50)/2
    c_y = (50+75)/2
    a = 50-c_x
    b = c_y-50
    pygame.draw.circle(screen, RED, (c_x, c_y-offset1), radius=math.sqrt(a**2 + b**2), width=0)
    c_x = (50+75)/2
    c_y = c_x
    a = c_x-50
    b = a
    pygame.draw.circle(screen, RED, (c_x, c_y-offset1), radius=math.sqrt(a**2 + b**2), width=0)
    offset2 = 1
    pygame.draw.polygon(screen, RED, [(50, 50-offset1), (75-offset2*2, 75-offset1-offset2*2), (50, 100-offset1-offset2*5), (25+offset2, 75-offset1-offset2)], width=0)
    # ----------------
    pygame.display.flip()
    clock.tick(60)
pygame.quit()