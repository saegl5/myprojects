import pygame, sys
pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
 
size = (704, 512)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
draw = False # start as "False," so won't draw unless press mouse/trackpad button and move

pygame.display.set_caption("QUESTABOX's 'Pictionary' Game")

def draw_rect(x, y, W, H):
    pygame.draw.rect(screen, WHITE, (x, y, W, H), width=1)

screen.fill(BLUE) # placed outside WHILE loop to display background

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif event.type == pygame.MOUSEBUTTONUP:
            draw = False
        else:
            None
    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-size[0]/2
    y_offset = pos[1]-size[1]/2
    if draw == True: # IF mouse/trackpad button pressed
        draw_rect(size[0]/2+x_offset, size[1]/2+y_offset, 1, 1)
    else:
        None # do not draw
    pygame.display.flip()
    clock.tick(120) # render more dots
pygame.quit()
