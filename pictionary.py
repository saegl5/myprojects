"""
"Pictionary" Game
"""

import pygame
import src.canvas as canvas
from custom.energy import time_stamp, save_energy

pygame.display.set_caption("QUESTABOX's \"Pictionary\" Game")
pygame.mouse.set_visible(False)  # hide the mouse cursor, will replace it with picture of chalk later

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
draw = False # don't draw unless press mouse/trackpad button and move
previous_x = None
previous_y = None
drawn = pygame.sprite.Group()
cursor_picture = pygame.image.load('images/chalk.png').convert()
cursor_picture.set_colorkey(BLUE)

class Draw(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        SIZE = (2, 2) # thicker drawing marks
        self.image = pygame.Surface(SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

def fill(sprite):
    global previous_x
    global previous_y
    if previous_x != None: # or previous_y != None
        diff_x = sprite.rect.x - previous_x
        diff_y = sprite.rect.y - previous_y
        steps = max(abs(diff_x), abs(diff_y))
        if steps != 0: # cannot divide by zero
            dx = diff_x / steps
            dy = diff_y / steps
            for i in range(int(steps)):
                mark = Draw()
                previous_x += dx
                previous_y += dy
                mark.rect.x = previous_x
                mark.rect.y = previous_y
                drawn.add(mark) # preserves marks from being cleared

while True: # keeps screen open
    for action in pygame.event.get(): # check for user input when open screen
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()

        elif action.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif action.type == pygame.MOUSEBUTTONUP:
            draw = False

        time_stamp(action)

    # --- Game logic
    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-canvas.SIZE[0]/2
    y_offset = pos[1]-canvas.SIZE[1]/2
    if draw == True: # IF mouse/trackpad button pressed
        mark = Draw()
        mark.rect.x = canvas.SIZE[0]/2+x_offset
        mark.rect.y = canvas.SIZE[1]/2+y_offset
        drawn.add(mark) # preserves marks from being cleared
        fill(mark) # fill gaps between marks
        previous_x = mark.rect.x
        previous_y = mark.rect.y
    else:
        previous_x = None
        previous_y = None
    # --------------
    canvas.clean()
    # --- Drawing code    
    drawn.draw(canvas.screen)
    canvas.screen.blit(cursor_picture, (pos[0]-11, pos[1])) # copy picture of chalk onto screen where cursor would be, shift it slightly to align chalk with drawing mark
    # ----------------
    canvas.show()
    save_energy()