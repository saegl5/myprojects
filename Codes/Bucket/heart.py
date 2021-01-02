import pygame, math
pygame.init()

BLACK = (0, 0 ,0)
RED = (255, 0, 0)
 
size = (100, 100)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
position = (50, 50) # define x- and y-coordinates
size = 100 # define percentage

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLACK)
    # --- Drawing code
    # Polygon
    p_top = (position[0], position[1]-size/4)
    p_right = (position[0]+size/4, position[1])
    p_bottom = (position[0], position[1]+size/4)
    p_left = (position[0]-size/4, position[1])
    pygame.draw.polygon(screen, RED, [p_top, p_right, p_bottom, p_left], width=0)
    # Circles
    c_top_left = ((p_left[0]+p_top[0])/2, (p_left[1]+p_top[1])/2)
    c_top_right = ((p_top[0]+p_right[0])/2, (p_top[1]+p_right[1])/2)
    r = size/4*math.sqrt(2)/2 # from trigonometric ratios of 45-45-90 degree triangles
    pygame.draw.circle(screen, RED, c_top_left, radius=r, width=0)
    pygame.draw.circle(screen, RED, c_top_right, radius=r, width=0)
    # ----------------
    pygame.display.flip()
    clock.tick(60)
pygame.quit()