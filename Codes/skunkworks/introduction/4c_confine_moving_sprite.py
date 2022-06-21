"""
Confine Moving Sprite
"""

import pygame
import src.canvas as canvas
import custom.classes as c
import custom.functions as f

pygame.display.set_caption("Sprites")

WHITE = pygame.Color("white")
CYAN = pygame.Color("cyan")
width = 64
height = 64
block = c.Rectangle(width/2, height/2)
block.image.fill(CYAN) # example
block.rect.x = 100 # example
block.rect.y = 200 # example
# (x, y) is the location of sprite's top-left corner
sprites = pygame.sprite.Group()
sprites.add(block)
speed = 5 # example
x_increment = speed
y_increment = 0
sprites.add(f.walls())
pygame.key.set_repeat(10) # optional, 10 millisecond delay between repeats, smoothes out movement

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
    
        # Keyboard events
         
    # Game logic
    block.rect.x += x_increment
    hit_x = pygame.sprite.spritecollide(block, f.walls(), False) # list wall hit
    for wall in hit_x:
        x_increment *= -1
    block.rect.y += y_increment # okay, if not moving diagonally
    hit_y = pygame.sprite.spritecollide(block, f.walls(), False) # list wall hit
    for wall in hit_y:
        y_increment *= -1

    canvas.clean()

    # Drawing code
    sprites.draw(canvas.screen)

    canvas.show()