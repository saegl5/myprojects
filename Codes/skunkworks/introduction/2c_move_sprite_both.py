"""
Move Sprite Using Keyboard and TrackPad
"""

import pygame
import src.canvas as canvas
import custom.classes as c

pygame.display.set_caption("Sprite")

WHITE = pygame.Color("white")
width = 64
height = 64
player = c.Rectangle(width, height)
player.image.fill(WHITE) # example
player.rect.centerx = canvas.screen.get_rect().centerx # could also specify rect.x
player.rect.centery = canvas.screen.get_rect().centery # could also specify rect.y
sprites = pygame.sprite.Group()
sprites.add(player)
pos = int()
speed = 5 # example
x_increment = 0
y_increment = 0
pygame.key.set_repeat(10) # optional, 10 millisecond delay between repeats, smooths out movement

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        # Mouse/trackpad events
        elif action.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos() # returns tuple, (x, y)
    
        # Keyboard events
        elif action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RIGHT: # note "action.key"
                x_increment = speed
            elif action.key == pygame.K_UP:
                y_increment = -speed # y decreases going upward
            elif action.key == pygame.K_LEFT:
                x_increment = -speed
            elif action.key == pygame.K_DOWN:
                y_increment = speed # y increases going downward
        elif action.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
         
    # Game logic
    if action.type == pygame.MOUSEMOTION:
        player.rect.x = pos[0]-width/2 # move sprite to align cursor with it's center
        player.rect.y = pos[1]-height/2
    else:
        player.rect.x += x_increment
        player.rect.y += y_increment
        pygame.mouse.set_pos(player.rect.centerx, player.rect.centery) # otherwise, mouse/trackpad will be out of sync with keyboard

    canvas.clean()

    # Drawing code
    sprites.draw(canvas.screen)

    canvas.show()