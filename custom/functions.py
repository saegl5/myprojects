"""
Connects Marks
"""

from custom.classes import Draw

def fill(previous_x, previous_y, sprite, color, drawn, w, h):
    if previous_x != None: # or previous_y != None
        diff_x = sprite.rect.x - previous_x
        diff_y = sprite.rect.y - previous_y
        steps = max(abs(diff_x), abs(diff_y))
        if steps != 0: # cannot divide by zero
            dx = diff_x / steps
            dy = diff_y / steps
            for i in range(int(steps)):
                mark = Draw(color, w, h)
                previous_x += dx
                previous_y += dy
                mark.rect.x = previous_x
                mark.rect.y = previous_y
                drawn.add(mark) # preserves marks from being cleared

"""
Construct Outer Walls
"""

import src.canvas as canvas  # works, if run from main module
from custom.classes import Rectangle

def left_wall():
    wall = Rectangle(1, canvas.SIZE[1]) # need at least some thickness
    wall.rect.x = -1 # moved walls outside screen
    wall.rect.y = 0
    return wall

def right_wall():
    wall = Rectangle(1, canvas.SIZE[1])
    wall.rect.x = canvas.SIZE[0]
    wall.rect.y = 0
    return wall

def top_wall():
    wall = Rectangle(canvas.SIZE[0]-2, 1) # no overlap
    wall.rect.x = 1
    wall.rect.y = -1
    return wall

def bottom_wall():
    wall = Rectangle(canvas.SIZE[0]-2, 1)
    wall.rect.x = 1
    wall.rect.y = canvas.SIZE[1]
    return wall

"""
Walk Mario
"""

import pygame

def walk(count, sprite, sprite_sheet, frame_list, width, height, facing_left):
    if count == 1: # in case there is a quick KEYDOWN and KEYUP event
        # sprite.rect.w = frame_list[2][2], don't use since walk in midair
        sprite.image = pygame.Surface((frame_list[2][2], frame_list[1][3])).convert_alpha()
        sprite.image.blit(sprite_sheet, (0, 0), (frame_list[1][0], frame_list[1][1], frame_list[1][2], height))
        sprite.image = pygame.transform.flip(sprite.image, flip_x=facing_left, flip_y=False)
    if count == 5: # else mario appears to hover
        # sprite.rect.w = frame_list[2][2], don't use since walk in midair
        sprite.image = pygame.Surface((frame_list[2][2], frame_list[2][3])).convert_alpha()
        sprite.image.blit(sprite_sheet, (0, 0), (frame_list[2][0], frame_list[2][1], width, height))
        sprite.image = pygame.transform.flip(sprite.image, flip_x=facing_left, flip_y=False)
    if count % 10 == 0: # on count of 10
        # sprite.rect.w = frame_list[2][2], don't use since walk in midair
        sprite.image = pygame.Surface((frame_list[2][2], frame_list[1][3])).convert_alpha()
        sprite.image.blit(sprite_sheet, (0, 0), (frame_list[1][0], frame_list[1][1], frame_list[1][2], height))
        sprite.image = pygame.transform.flip(sprite.image, flip_x=facing_left, flip_y=False)
    if count % 20 == 0:
        # sprite.rect.w = frame_list[2][2], don't use since walk in midair
        sprite.image = pygame.Surface((frame_list[2][2], frame_list[2][3])).convert_alpha()
        sprite.image.blit(sprite_sheet, (0, 0), (frame_list[2][0], frame_list[2][1], width, height))
        sprite.image = pygame.transform.flip(sprite.image, flip_x=facing_left, flip_y=False)

"""
Stand Mario
"""

def stand(sprite, sprite_sheet, frame_list, width, height, facing_left):
    sprite.image = pygame.Surface((frame_list[0][2], frame_list[0][3])).convert_alpha()
    sprite.image.blit(sprite_sheet, (0, 0), (frame_list[0][0], frame_list[0][1], width, height))
    sprite.image = pygame.transform.flip(sprite.image, flip_x=facing_left, flip_y=False)