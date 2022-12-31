"""
"Pictionary" Game
"""

import pygame
import src.canvas as canvas
from custom.energy import time_stamp, save_energy
from custom.classes import Draw
from custom.functions import fill

pygame.display.set_caption("QUESTABOX's \"Pictionary\" Game")
pygame.mouse.set_visible(False)  # hide the mouse cursor, will replace it with picture of chalk later

BLUE = pygame.Color("blue") # chalkboard color
WHITE = pygame.Color("white") # chalk mark color
LIGHTBLUE = pygame.Color(50, 50, 255) # eraser mark color
color = WHITE # default mark color
draw = False # don't draw unless press mouse/trackpad button and move
previous_x = None
previous_y = None
drawn = pygame.sprite.Group()
cursor_picture_draw = pygame.image.load('images/chalk.png').convert_alpha()
cursor_picture_erase = pygame.image.load('images/eraser.png').convert_alpha()
cursor_picture = cursor_picture_draw # default cursor picture
w = 2 # default mark size
h = 2
x_offset = 0
y_offset = 0
style = pygame.font.Font(None, 18)
tip = style.render("To erase, hold down CTRL key", True, WHITE)

while True: # keeps screen open
    for event in pygame.event.get(): # check for user input when open screen
        if event.type == pygame.QUIT: # user clicked close button
            canvas.close()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif event.type == pygame.MOUSEBUTTONUP:
            draw = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL: # for eraser
                cursor_picture = cursor_picture_erase
                color = LIGHTBLUE
                w = 12 # bigger mark
                h = 12
                x_offset = 5
                y_offset = 5
        elif event.type == pygame.KEYUP:
            cursor_picture = cursor_picture_draw
            color = WHITE # revert
            w = 2
            h = 2
            x_offset = 0
            y_offset = 0

        time_stamp(event)

    # --- Game logic
    pos = pygame.mouse.get_pos()
    if draw == True: # IF mouse/trackpad button pressed
        mark = Draw(color, w, h)
        mark.rect.x = pos[0]-x_offset
        mark.rect.y = pos[1]-y_offset
        drawn.add(mark) # preserves marks from being cleared
        fill(previous_x, previous_y, mark, color, drawn, w, h) # fill gaps between marks
        previous_x = mark.rect.x
        previous_y = mark.rect.y
    else:
        previous_x = None
        previous_y = None
    # --------------
    canvas.clean()
    # --- Drawing code    
    drawn.draw(canvas.screen)
    canvas.screen.blit(cursor_picture, (pos[0]-1.5*x_offset-7, pos[1]-cursor_picture.get_height()+1.5*y_offset+8)) # copy picture of chalk/eraser onto screen where cursor would be, shift it slightly to align chalk/eraser with drawing mark
    canvas.screen.blit(tip, (10, 10))
    # ----------------
    canvas.show()
    save_energy()