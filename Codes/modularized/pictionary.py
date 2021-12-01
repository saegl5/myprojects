"""
"Pictionary" Game
"""

import pygame
import src.frame as frame
import src.canvas as canvas
import src.efficiency as efficiency
import custom.classes as classes
import custom.functions as functions

pygame.display.set_caption("QUESTABOX's \"Pictionary\" Game")

WHITE = pygame.Color("white")
draw = False # start as "False," so won't draw unless press mouse/trackpad button and move
previous_x = None
previous_y = None
drawn = pygame.sprite.Group()
cursor = pygame.image.load('images/chalk.png').convert()
cursor.set_colorkey(canvas.BLUE)
pygame.mouse.set_visible(False)  # hide the system cursor, will replace it with image of chalk later

while True:
    for action in pygame.event.get():
        frame.open(action)

        if action.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif action.type == pygame.MOUSEBUTTONUP:
            draw = False

        efficiency.snapshot(action)

    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-frame.size[0]/2
    y_offset = pos[1]-frame.size[1]/2
    if draw == True: # IF mouse/trackpad button pressed
        mark = classes.Draw(WHITE)
        mark.rect.x = frame.size[0]/2+x_offset
        mark.rect.y = frame.size[1]/2+y_offset
        drawn.add(mark) # preserves marks from being cleared
        functions.fill(previous_x, previous_y, mark, WHITE, drawn) # fill gaps between marks
        previous_x = mark.rect.x
        previous_y = mark.rect.y
    else:
        previous_x = None
        previous_y = None

    canvas.clean()

    drawn.draw(canvas.screen)
    canvas.screen.blit(cursor, (pos[0]-11, pos[1])) # copy image of chalk onto screen where cursor would be, shift it slightly to align chalk with drawing mark
    
    canvas.show()
    efficiency.activate()