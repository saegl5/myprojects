import pygame
import sys

pygame.init()

BLACK = pygame.Color("black")
RED = pygame.Color("red")
 
size = (100, 100)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
position = (50, 50) # define x- and y-coordinates
multiple = 4 # define multiple (0-5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLACK)
    # --- Drawing code
    # Utilizing Pythagorean triple 3:4:5 to mitigate errors
    # Doubling multiples to mitigate errors, as well
    # Polygon Corners
    p_top = (position[0], position[1]-3*2*multiple)
    p_right = (position[0]+4*2*multiple, position[1])
    p_bottom = (position[0], position[1]+3*2*multiple)
    p_left = (position[0]-4*2*multiple, position[1])
    # Circle Center
    c_top_left = ((p_left[0]+p_top[0])/2, (p_left[1]+p_top[1])/2)
    c_top_right = ((p_top[0]+p_right[0])/2, (p_top[1]+p_right[1])/2)
    # Circle Radius
    r = 5*2*multiple*1/2
    # Draw Circles
    pygame.draw.circle(screen, RED, c_top_left, radius=r, width=0)
    pygame.draw.circle(screen, RED, c_top_right, radius=r, width=0)
    # Cut Each Circle into Semi-Circles
    # (includes corrections to any remaining errors)
    pygame.draw.polygon(screen, BLACK, [(p_top[0]-1, p_top[1]), (p_right[0]-1, p_right[1]-1), (p_bottom[0]-1, p_bottom[1]+6*multiple), (p_left[0], p_left[1]-1)], width=0)
    # Draw Polygon
    # (includes corrections to any remaining errors)
    pygame.draw.polygon(screen, RED, [(p_top[0]-1, p_top[1]), (p_right[0]-1, p_right[1]-1), (p_bottom[0]-1, p_bottom[1]-1), (p_left[0], p_left[1]-1)], width=0)
    # ----------------
    pygame.display.flip()
    clock.tick(60)