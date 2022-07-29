"""
"Pictionary" Game
"""

import pygame
import src.canvas as canvas

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

draw = False # start as "False," so won't draw unless press mouse/trackpad button and move
previous_x = None
previous_y = None
drawn = pygame.sprite.Group()
ticks = int() # for saving energy

pygame.display.set_caption("QUESTABOX's \"Pictionary\" Game")

cursor_picture = pygame.image.load('images/chalk.png').convert()
cursor_picture.set_colorkey(BLUE)
pygame.mouse.set_visible(False)  # hide the system cursor, will replace it with picture of chalk later

class Draw(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (2, 2) # thicker drawing marks
        self.image = pygame.Surface(size)
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

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()

        elif action.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif action.type == pygame.MOUSEBUTTONUP:
            draw = False
            ticks = pygame.time.get_ticks()

    pos = pygame.mouse.get_pos()
    x_offset = pos[0]-canvas.size[0]/2
    y_offset = pos[1]-canvas.size[1]/2
    if draw == True: # IF mouse/trackpad button pressed
        mark = Draw()
        mark.rect.x = canvas.size[0]/2+x_offset
        mark.rect.y = canvas.size[1]/2+y_offset
        drawn.add(mark) # preserves marks from being cleared
        fill(mark) # fill gaps between marks
        previous_x = mark.rect.x
        previous_y = mark.rect.y
    else:
        previous_x = None
        previous_y = None

    canvas.clean()

    drawn.draw(canvas.screen)
    canvas.screen.blit(cursor_picture, (pos[0]-11, pos[1])) # copy picture of chalk onto screen where cursor would be, shift it slightly to align chalk with drawing mark
    
    canvas.show()
    if pygame.time.get_ticks() - ticks > 10000: # unless user stops playing for 10 seconds
        canvas.clock.tick(1) # in which case minimize the frame rate