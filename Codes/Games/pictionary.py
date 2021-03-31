import pygame
import sys

pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
draw = False # start as "False," so won't draw unless press mouse/trackpad button and move

pygame.display.set_caption("QUESTABOX's 'Pictionary' Game")

def draw_circle(x, y, radius):
    pygame.draw.circle(screen, WHITE, (x, y), radius, width=1)

screen.fill(BLUE) # placed outside WHILE loop to display background

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif event.type == pygame.MOUSEBUTTONUP:
            draw = False
    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-size[0]/2
    y_offset = pos[1]-size[1]/2
    if draw == True: # IF mouse/trackpad button pressed
        draw_circle(size[0]/2+x_offset, size[1]/2+y_offset, 1)
    pygame.display.flip()
    clock.tick(120) # render more dots