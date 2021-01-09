# give student a drawing of multiple shapes, and have them animate it

import pygame
pygame.init()

LIGHTGRAY = (211, 211, 211)
BLACK = (0, 0, 0)

size = (100, 200)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
y_offset = 0 # <- STEP 2b, changed to "y_offset"
x_offset = 0 # <- STEP 2 (horizontal movement)
y_increment = 20 # <- STEP 4, changed to "y_increment"
x_increment = 10 # <- STEP 4

pygame.display.set_caption("STUDENT's Cool Animation")
 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(LIGHTGRAY) # clear the screen
    # --- Drawing code
    # offset = 0 <- STEP 2a
    # while offset <= 80: <- STEP 0
    pygame.draw.rect(screen, BLACK, (0+x_offset, 0+y_offset, 10, 20), width=0) # untab <- "offset" is STEP 1 (could also offset x-coordinate), "offset" became "y_offset"
    y_offset += y_increment # untab, "increment" is STEP 3, "increment" became "y_increment"
    x_offset += x_increment # <- STEP 3
    if 0+y_offset + 20 == size[1]: # <- STEP 5a
        y_increment *= -1
    elif 0+y_offset == 0: # <- STEP 5b
        y_increment *= -1
    if 0+x_offset + 10 == size[0]: # <- STEP 5a
        x_increment *= -1
    elif 0+x_offset == 0: # <- STEP 5b
        x_increment *= -1
    # ----------------
    pygame.display.flip()
    clock.tick(10)
pygame.quit()