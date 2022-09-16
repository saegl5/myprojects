"""
"Space Invaders" Game
"""

import pygame, random
import src.canvas as canvas
from custom.energy import time_stamp, save_energy
from custom.classes import Rectangle
from custom.functions import left_wall, right_wall

pygame.display.set_caption("QUESTABOX's \"Space Invaders\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second), plays with time_stamp

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

spaceship_picture = pygame.image.load('images/ship.png').convert()
spaceship_picture = pygame.transform.scale(spaceship_picture, (W, H))
spaceship_picture_retry = pygame.transform.scale(spaceship_picture, (W/2, H/2))
invader_picture = pygame.image.load('images/alien.png').convert()
invader_picture_alt = pygame.image.load('images/alien_lunging.png').convert()

INVADER_COUNT = 50
timer = 30 # 30 seconds (multiple of modulo for invaders.update())
score = 0
first = True # for spaceship laser
count = 0 # for lunging picture
retries = 2
retry_boxes = []
P = 5 # chop up each barrier into 5 pieces
wait1 = canvas.fps*2 # if spaceship hit by invader, 60 fps x 2 seconds
wait2 = wait1 # if spaceship hit by return fire
waiting = False # if spaceship hit by either

# --- Functions
def lunge(sprite):
    if count % 2 == 0: # could also have used timer
        sprite.image.blit(invader_picture_alt, (0, 0)) # change picture
    else:
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
# ---------------------

# outer walls
walls.add(left_wall())
walls.add(right_wall())

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

while INVADER_COUNT-len(invaders) > 0: # create and add fifty "invader" sprites
    invader = Rectangle(W/2, H/2)
    invader.rect.x = random.randrange(0, canvas.SIZE[0]+1-W/2, W/2) # allow sprite to touch edge but not breach it
    invader.rect.y = random.randrange(0, canvas.SIZE[1]+1-H/2-196, H/2) # 196px space at canvas bottom
    invader.image.blit(invader_picture, (0, 0))
    pygame.sprite.spritecollide(invader, invaders, True) # remove any sprite in same position, you cannot check if sprite is already in group or already belongs to group since each sprite is unique
    invaders.add(invader)

# we will create "laser" sprites later

while True: # keeps screen open
    for action in pygame.event.get(): # check for user input when open screen
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()

        elif action.type == pygame.USEREVENT: # for timer, "elif" means else if
            if timer == 0 or len(spaceships) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # disable timer
                game_over_sound.play()
            elif len(invaders) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else: # after one second
                timer -= 1
                for invader in invaders:
                    lunge(invader) # all "invader" sprites lunge
                count += 1
                if timer % 5 == 0: # every 5 seconds
                    invaders.update(32) # move "invader" sprites downward
                if timer % 4 == 0 and len(invaders) > 0: # some number not multiple of 5
                    laser = Rectangle(6, 40)
                    return_fire(laser, 0)
                if timer % 7 == 0 and len(invaders) > 1:
                    laser = Rectangle(6, 40)
                    return_fire(laser, 1)
                if timer % 11 == 0 and len(invaders) > 2:
                    laser = Rectangle(6, 40)
                    return_fire(laser, 2)

        # --- Keyboard events
        elif action.type == pygame.KEYDOWN:
            if timer != 0 and len(invaders) != 0 and len(spaceships) != 0:
                if action.key == pygame.K_RIGHT:
                    x_inc = 5
                if action.key == pygame.K_LEFT:
                    x_inc = -5
                if action.key == pygame.K_SPACE: # fire laser
                    laser = Rectangle(10, 20)
                    laser.rect.centerx = spaceship.rect.centerx
                    laser.rect.bottom = spaceship.rect.top + 10 # "+ 10" because update() is called before "laser" sprites are drawn
                    laser.image.fill(YELLOW)
                    if first == True:
                        lasers.add(laser)
                        spaceship_laser_sound.play()
                        first = False
            else:
                x_inc = 0

        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                x_inc = 0
            if action.key == pygame.K_SPACE:
                first = True

        time_stamp(action)
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

    if timer != 0 and len(spaceships) != 0 and len(invaders) != 0:
        lasers.update(-10)
        lasers_alt.update(2)
    else: # stops lasers from moving when game over or win game
        lasers.update(0)
        lasers_alt.update(0)
    score = len(collisions)

    # --------------

    canvas.clean()
    timer_header = style_header.render("Time Left", False, RED) # "False" for anti-aliased
    timer_text = style.render(str(timer), False, RED)
    score_header = style_header.render("Score", False, GREEN)
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, BLACK)
    you_win_text = style.render(None, False, GREEN)
    if timer == 0 or len(spaceships) == 0:
        game_over_text = style.render("Game Over", False, BLACK)
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    sprites.empty()
    sprites.add(walls, barriers, invaders, lasers_alt, spaceships, lasers) # spaceships is redundant

    # --- Drawing code
    sprites.draw(canvas.screen)
    canvas.screen.blit(spaceship.image, (spaceship.rect.x, spaceship.rect.y)) # so you can see it, even if game over
    canvas.screen.blit(timer_header, (10, 10))
    canvas.screen.blit(timer_text, (10, 30))
    for i in range(0, retries):
        canvas.screen.blit(retry_boxes[i], (100+i*W/2, 10)) # to right of timer
        retry_boxes[i].set_colorkey(BLACK)
    canvas.screen.blit(score_header, (canvas.SIZE[0]-score_header.get_width()-10, 10)) # near top-right corner
    canvas.screen.blit(score_text, (canvas.SIZE[0]-score_text.get_width()-10, 30))
    canvas.screen.blit(game_over_text, game_over_text.get_rect(center = canvas.screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    canvas.screen.blit(you_win_text, you_win_text.get_rect(center = canvas.screen.get_rect().center))
    # ----------------

    canvas.show()
    save_energy()