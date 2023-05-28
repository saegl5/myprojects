"""
"Space Invaders" Game
"""

import pygame
import src.canvas as canvas
from custom.energy import time_stamp, save_energy
from custom.classes import Rectangle
from custom.functions import left_wall, right_wall

pygame.display.set_caption("QUESTABOX's \"Space Invaders\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
W = 64 # "spaceship" sprite width reference
H = 64 # "spaceship" sprite height reference
x_inc = 0 # speed

invaders = pygame.sprite.Group() # not invaders = []
collisions = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
spaceships = pygame.sprite.Group()
barriers = pygame.sprite.Group()
walls = pygame.sprite.Group()
sprites = pygame.sprite.Group() # all sprites

style = pygame.font.Font(None, 100) # faster than SysFont(), "None" utilizes default font (i.e., freesansbold.ttf)
style_header = pygame.font.Font(None, 30)
style_header.set_italic(True)

game_over_sound = pygame.mixer.Sound('sounds/game_over.ogg')
you_win_sound = pygame.mixer.Sound('sounds/you_win.ogg')
spaceship_laser_sound = pygame.mixer.Sound('sounds/laserLarge.ogg')
spaceship_explosion_sound = pygame.mixer.Sound('sounds/explosionCrunch.ogg')
invader_laser_sound = pygame.mixer.Sound('sounds/laserSmall.ogg')
invader_explosion_sound = pygame.mixer.Sound('sounds/lowFrequency_explosion.ogg')

spaceship_picture = pygame.image.load('images/ship.png').convert_alpha()
spaceship_picture = pygame.transform.scale(spaceship_picture, (W, H))
spaceship_picture_retry = pygame.transform.scale(spaceship_picture, (W/2, H/2))
invader_picture = pygame.image.load('images/alien.png').convert_alpha()
invader_picture_alt = pygame.image.load('images/alien_lunging.png').convert_alpha()

repeated = 0 # times
score = 0
first = True # for spaceship laser
px = 10 # for spaceship laser too
count = 0 # for lunging picture
retries = 2
retry_boxes = []
P = 5 # chop up each barrier into 5 pieces
wait1 = canvas.fps*2 # if spaceship hit by invader, 60 fps x 2 seconds
wait2 = wait1 # if spaceship hit by return fire
waiting = False # if spaceship hit by either
played = False

# --- Functions
def lunge(sprite):
    if count % (canvas.fps*1) == 0: # could also have used timer
        sprite.image = pygame.Surface((W, H), pygame.SRCALPHA) # otherwise blitting on same surface
        sprite.image.blit(invader_picture_alt, (0, 0)) # change picture
    if count % (canvas.fps*2) == 0:
        sprite.image = pygame.Surface((W, H), pygame.SRCALPHA)
        sprite.image.blit(invader_picture, (0, 0)) # revert
def retry(sprite):
    sprite.rect.centerx = canvas.screen.get_rect().centerx # center along bottom of screen
    sprite.rect.y = canvas.SIZE[1]-H
def return_fire(sprite, index):
    sprite.image.fill(RED)
    sprite.rect.centerx = invaders.sprites()[index].rect.centerx
    sprite.rect.top = invaders.sprites()[index].rect.bottom
    lasers_alt.add(sprite)
    invader_laser_sound.play()
def invaders_add(x, y):
    invader = Rectangle(W/2, H/2)
    invader.rect.x, invader.rect.y = x, y
    invader.image.blit(invader_picture, (0, 0))
    invaders.add(invader)
# ---------------------

# outer walls
walls.add(left_wall(), right_wall())

# left barrier
for i in range(0, P):
    barrier = Rectangle(250/P, 25)
    barrier.rect.x = 50+i*250/P
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

# right barrier
for i in range(0, P):
    barrier = Rectangle(250/P, 25)
    barrier.rect.x = canvas.SIZE[0]-250-50+i*250/P
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

spaceship = Rectangle(W, H)
spaceship.rect.centerx = canvas.screen.get_rect().centerx
spaceship.rect.y = canvas.SIZE[1] - H
spaceship.image.blit(spaceship_picture, (0, 0))
spaceships.add(spaceship)
for i in range(0, retries):
    retry_boxes.append(spaceship_picture_retry)

invaders_add(W/2*1, H/2) # (32, 32)
invaders_add(W/2*3, H) # (96, 64)
invaders_add(W/2*5, H/2) # (160, 32)
invaders_add(W/2*7, H) # (224, 64)
invaders_add(W/2*9, H/2) # (288, 32)
invaders_add(W/2*11, H) # (352, 64)
invaders_add(W/2*13, H/2) # (416, 32)
invaders_add(W/2*15, H) # (480, 64)
invaders_add(W/2*17, H/2) # (544, 32)
invaders_add(W/2*19, H) # (608, 64)
# make sure to leave space at canvas bottom

# we will create "laser" sprites later

while True: # keeps screen open
    for event in pygame.event.get(): # check for user input when open screen
        if event.type == pygame.QUIT: # user clicked close button
            canvas.close()

        # --- Keyboard events
        elif event.type == pygame.KEYDOWN:
            if len(invaders) != 0 and len(spaceships) != 0: # game still in play
                if event.key == pygame.K_RIGHT:
                    x_inc = 5
                if event.key == pygame.K_LEFT:
                    x_inc = -5
                if event.key == pygame.K_SPACE: # fire laser
                    laser = Rectangle(10, 20)
                    laser.rect.centerx = spaceship.rect.centerx
                    laser.rect.bottom = spaceship.rect.top + px # update() is called before "laser" sprites are drawn
                    laser.image.fill(YELLOW)
                    if first == True:
                        lasers.add(laser)
                        spaceship_laser_sound.play()
                        first = False
            else:
                x_inc = 0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_inc = 0
            if event.key == pygame.K_SPACE:
                first = True

        time_stamp(event)
        # -------------------
        
    # --- Game logic
    spaceship.rect.x += x_inc
    hit = pygame.sprite.spritecollide(spaceship, walls, False) # don't remove wall, returns a list
    for wall in hit: # wall that spaceship hit
        if x_inc > 0:
            spaceship.rect.right = wall.rect.left
        else: # x_inc = 0 not hitting a wall
            spaceship.rect.left = wall.rect.right

    for laser in lasers: # "laser" sprite was not created before WHILE loop
        invader_removed = pygame.sprite.spritecollide(laser, invaders, True) # remove invader
        collisions.add(invader_removed) # when invader is removed, add it to collisions group
        if invader_removed != []: # OR for invader in invader_removed:
            lasers.remove(laser) # remove laser, too
            invader_explosion_sound.play()
        elif laser.rect.bottom < 0: # lasers leave canvas
            lasers.remove(laser)

    for invader in invaders:
        if wait1 == canvas.fps*2 and waiting == False:
            spaceship_removed = pygame.sprite.spritecollide(invader, spaceships, True)
        elif wait1 == canvas.fps*2 and waiting == True:
            break
        else:
            spaceship_removed = [] # we will wait to check for collision
            wait1 -= 1
            if wait1 == 0:
                wait1 = canvas.fps*2
                waiting = False
            break
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed) # will reposition the spaceship
            retry(spaceship)
            retries -= 1
            wait1 -= 1
            waiting = True
            break # makes timing extra precise
    
    for laser in lasers_alt:
        if wait2 == canvas.fps*2 and waiting == False:
            spaceship_removed = pygame.sprite.spritecollide(laser, spaceships, True)
        elif wait2 == canvas.fps*2 and waiting == True:
            break
        else:
            spaceship_removed = []
            wait2 -= 1
            if wait2 == 0:
                wait2 = canvas.fps*2
                waiting = False
            break
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed)
            retry(spaceship)
            lasers_alt.remove(laser)
            retries -= 1
            wait2 -= 1
            waiting = True
            break            
        elif laser.rect.top > canvas.SIZE[1]:
            lasers_alt.remove(laser)

    for laser in lasers_alt:
        barrier_removed = pygame.sprite.spritecollide(laser, barriers, True)
        if barrier_removed != []:
            lasers_alt.remove(laser)

    if len(spaceships) == 0 and played == False:
        game_over_sound.play()
        played = True
    elif len(invaders) == 0 and played == False:
        you_win_sound.play()
        played = True
    else:        
        count += 1        
        for invader in invaders:
            lunge(invader) # all "invader" sprites lunge
        repeated += 1
        if repeated % (canvas.fps*5) == 0: # every 5 seconds
            invaders.update(32) # move "invader" sprites downward
        if repeated % (canvas.fps*4) == 0 and len(invaders) > 0: # some number not multiple of 5
            laser = Rectangle(6, 40)
            return_fire(laser, 0)
        if repeated % (canvas.fps*7) == 0 and len(invaders) > 1:
            laser = Rectangle(6, 40)
            return_fire(laser, 1)
        if repeated % (canvas.fps*11) == 0 and len(invaders) > 2:
            laser = Rectangle(6, 40)
            return_fire(laser, 2)

    if len(spaceships) != 0 and len(invaders) != 0:
        lasers.update(-px)
        lasers_alt.update(2)
    else: # stops lasers from moving when game over or win game
        lasers.update(0)
        lasers_alt.update(0)
    score = len(collisions)

    # --------------

    canvas.clean()
    score_header = style_header.render("Score", False, GREEN) # "False" for anti-aliased
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, BLACK)
    you_win_text = style.render(None, False, GREEN)
    if len(spaceships) == 0:
        game_over_text = style.render("Game Over", False, BLACK)
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    sprites.empty() # could instead have done sprites.remove(laser) multiple times above
    sprites.add(walls, barriers, invaders, lasers_alt, spaceships, lasers) # spaceships is redundant

    # --- Drawing code
    sprites.draw(canvas.screen)
    canvas.screen.blit(spaceship.image, (spaceship.rect.x, spaceship.rect.y)) # so you can see it, even if game over
    for i in range(0, retries):
        canvas.screen.blit(retry_boxes[i], (10+i*W/2, 10)) # to right of timer
    canvas.screen.blit(score_header, (canvas.SIZE[0]-score_header.get_width()-10, 10)) # near top-right corner
    canvas.screen.blit(score_text, (canvas.SIZE[0]-score_text.get_width()-10, 30))
    canvas.screen.blit(game_over_text, game_over_text.get_rect(center = canvas.screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    canvas.screen.blit(you_win_text, you_win_text.get_rect(center = canvas.screen.get_rect().center))
    # ----------------

    canvas.show()
    save_energy()