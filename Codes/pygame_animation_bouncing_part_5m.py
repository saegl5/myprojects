# give student a drawing of multiple shapes, and have them animate it

import pygame
pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

size = (100, 200)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
y_offset = 0 # <- STEP 2b, changed to "y_offset"
x_offset = 0 # <- STEP 2 (horizontal movement)
y_increment = 20 # <- STEP 4, changed to "y_increment"
x_increment = 20 # <- STEP 4

pygame.display.set_caption("STUDENT's Cool Animation")
 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the screen
    # --- Drawing code
    # offset = 0 <- STEP 2a
    # while offset <= 180: <- STEP 0
    pygame.draw.rect(screen, WHITE, (0+x_offset, 0+y_offset, 20, 20), width=1) # untab <- "offset" is STEP 1 (could also offset x-coordinate), "offset" became "y_offset"
    pygame.draw.ellipse(screen, WHITE, (0+x_offset, 0+y_offset, 20, 20), width=1)
    y_offset += y_increment # untab, "increment" is STEP 3, "increment" became "y_increment"
    x_offset += x_increment # <- STEP 3
    # if 0+y_offset + 20 == size[1]: # <- STEP 5a
    #     y_increment *= -1
    # elif 0+y_offset == 0: # <- STEP 5b
    #     y_increment *= -1
    if 0+y_offset + 20 == size[1] or 0+y_offset == 0: # <- STEP 5a-b
        y_increment *= -1
    # if 0+x_offset + 20 == size[0]: # <- STEP 5a
    #     x_increment *= -1
    # elif 0+x_offset == 0: # <- STEP 5b
    #     x_increment *= -1
    else:
        None # continue
    if 0+x_offset + 20 == size[0] or 0+x_offset == 0: # <- STEP 5a-b
        x_increment *= -1
    else:
        None # continue
    # ----------------
    pygame.display.flip()
    clock.tick(10)
pygame.quit()