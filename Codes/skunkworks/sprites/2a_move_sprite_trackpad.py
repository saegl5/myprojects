"""
Move Sprite Using TrackPad
(Alternative: Mouse)
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

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        # Mouse/trackpad events
        elif action.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos() # returns tuple, (x, y)
    
    # Game logic
    player.rect.x = pos[0]-width/2 # move sprite to align cursor with it's center
    player.rect.y = pos[1]-height/2

    canvas.clean()

    # Drawing code
    sprites.draw(canvas.screen)

    canvas.show()