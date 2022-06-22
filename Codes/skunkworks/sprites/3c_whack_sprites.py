"""
Whack Sprites
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
player = c.Rectangle(width, height)
player.image.fill(WHITE) # example
player.rect.centerx = canvas.screen.get_rect().centerx # could also specify rect.x
player.rect.centery = canvas.screen.get_rect().centery # could also specify rect.y
block1 = c.Rectangle(width/2, height/2)
block1.image.fill(CYAN) # example
block1.rect.x = 100 # example
block1.rect.y = 200 # example
# (x, y) is the location of sprite's top-left corner
block2 = c.Rectangle(width*2, height*2)
block2.image.fill(CYAN) # example
block2.rect.x = 400
block2.rect.y = 200
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(block1)
sprites.add(block2)
blocks = pygame.sprite.Group()
blocks.add(block1)
blocks.add(block2)
speed = 5 # example
x_increment = 0
y_increment = 0
pygame.key.set_repeat(10) # optional, 10 millisecond delay between repeats, smoothes out movement
whacked = False

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
    removed = pygame.sprite.spritecollide(player, blocks, True) # list removed block
    for block in removed:
        for other_block in blocks: # not in removed list
            if whacked == False:
                whacked = True
                f.swap(block, other_block) # see functions.py
    if removed == []: # player is not hitting any block, making list empty
        whacked = False
    for block in removed:
        sprites.add(block)
        blocks.add(block)

    canvas.clean()

    # Drawing code
    sprites.draw(canvas.screen)

    canvas.show()