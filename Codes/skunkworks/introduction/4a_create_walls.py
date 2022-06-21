"""
Confine Sprite
"""

import pygame
import src.canvas as canvas
import custom.classes as c
import custom.functions as f

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
# pos = int() # for mouse/trackpad
speed = 5 # example
x_increment = 0
y_increment = 0
sprites.add(f.walls()) # see functions.py
pygame.key.set_repeat(10) # optional, 10 millisecond delay between repeats, smoothes out movement

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
    
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
    player.rect.x += x_increment
    player.rect.y += y_increment

    canvas.clean()

    # Drawing code
    sprites.draw(canvas.screen)

    canvas.show()