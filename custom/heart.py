"""
Draws Heart
"""

import pygame#, sys
import src.canvas as canvas # works, if run from main module

pygame.init()

BLUE = pygame.Color("blue")
RED = pygame.Color("red")
MULTIPLE = 4 # define multiple (0-5)
 
# size = (100, 100)
# screen = pygame.display.set_mode(size)
# clock = pygame.time.Clock()
def heart(x, y):
# position = (50, 50) # define x- and y-coordinates
# multiple = 4 # define multiple (0-5)
    position = (x, y) # define x- and y-coordinates

# while True:
#     for action in pygame.event.get():
#         if action.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
    # screen.fill(BLACK)
    # --- Drawing code
    # Utilizing Pythagorean triple 3:4:5 to mitigate errors
    # Doubling multiples to mitigate errors, as well
    # Polygon Corners
    p_top = (position[0], position[1]-3*2*MULTIPLE)
    p_right = (position[0]+4*2*MULTIPLE, position[1])
    p_bottom = (position[0], position[1]+3*2*MULTIPLE)
    p_left = (position[0]-4*2*MULTIPLE, position[1])
    # Circle Center
    c_top_left = ((p_left[0]+p_top[0])/2, (p_left[1]+p_top[1])/2)
    c_top_right = ((p_top[0]+p_right[0])/2, (p_top[1]+p_right[1])/2)
    # Circle Radius
    R = 5*2*MULTIPLE*1/2
    # Draw Circles
    pygame.draw.circle(canvas.screen, RED, c_top_left, radius=R, width=0)
    pygame.draw.circle(canvas.screen, RED, c_top_right, radius=R, width=0)
    # Cut Each Circle into Semi-Circles
    # (includes corrections to any remaining errors)
    pygame.draw.polygon(canvas.screen, BLUE, [(p_top[0]-1, p_top[1]), (p_right[0]-1, p_right[1]-1), (p_bottom[0]-1, p_bottom[1]+6*MULTIPLE), (p_left[0], p_left[1]-1)], width=0)
    # Draw Polygon
    # (includes corrections to any remaining errors)
    pygame.draw.polygon(canvas.screen, RED, [(p_top[0]-1, p_top[1]), (p_right[0]-1, p_right[1]-1), (p_bottom[0]-1, p_bottom[1]-1), (p_left[0], p_left[1]-1)], width=0)
    # ----------------
    # pygame.display.flip()
    # clock.tick(60)