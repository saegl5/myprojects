"""
Create Sprite
"""

import pygame
import src.canvas as canvas
import custom.classes as c

pygame.display.set_caption("Sprite")

WHITE = pygame.Color("white")
width = 64
height = 64
player = c.Rectangle(width, height) # see classes.py
player.image.fill(WHITE) # example
player.rect.centerx = canvas.screen.get_rect().centerx # could also specify rect.x with optional offset
player.rect.centery = canvas.screen.get_rect().centery # could also specify rect.y with optional offset
sprites = pygame.sprite.Group()
sprites.add(player)

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
    
        # Not using mouse/trackpad
        
        # Keyboard events
            
    # Game logic
    
    canvas.clean()

    # Drawing code
    sprites.draw(canvas.screen)

    canvas.show()