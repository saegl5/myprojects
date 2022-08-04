"""
"Space Invaders" Game
"""

import pygame, random
import src.canvas as canvas
import src.efficiency as efficiency
from custom.classes import Rectangle
from custom.functions import left_wall, right_wall

WHITE = pygame.Color("white")
BLACK = pygame.Color("black") # useful if run module on macOS
YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
GREEN = pygame.Color("green")

x_increment = 0 # speed
w = 64 # "spaceship" sprite width reference
h = 64 # "spaceship" sprite height reference

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
spaceship_picture = pygame.transform.scale(spaceship_picture, (w, h))
spaceship_picture_retry = pygame.transform.scale(spaceship_picture, (w/2, h/2))
invader_picture = pygame.image.load('images/alien.png').convert()
invader_picture_alt = pygame.image.load('images/alien_lunging.png').convert()

timer = 30 # 30 seconds (multiple of modulo for invaders.update())
score = 0
first = True # for spaceship laser
count = 0 # for lunging picture
retries = 2
retry_boxes = []
p = 5 # chop up each barrier into 5 pieces
invader_count = 50
wait1 = 60*2 # if spaceship hit by invader, 60 fps x 2 seconds
wait2 = wait1 # if spaceship hit by return fire
waiting = False # if spaceship hit by either

pygame.display.set_caption("QUESTABOX's \"Space Invaders\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second), plays with efficiency snapshot

# --- Functions
def lunge(sprite):
    if count % 2 == 0: # could also have used timer
        sprite.image.blit(invader_picture_alt, (0, 0)) # change picture
    else:
        sprite.image.blit(invader_picture, (0, 0)) # revert
def retry(sprite):
    sprite.rect.centerx = canvas.screen.get_rect().centerx # center along bottom of screen
    sprite.rect.y = canvas.size[1]-h
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
for i in range(0, p):
    barrier = Rectangle(250/p, 25)
    barrier.rect.x = 50+i*250/p
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

# right barrier
for i in range(0, p):
    barrier = Rectangle(250/p, 25)
    barrier.rect.x = canvas.size[0]-250-50+i*250/p
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

spaceship = Rectangle(w, h)
spaceship.rect.centerx = canvas.screen.get_rect().centerx
spaceship.rect.y = canvas.size[1]-h
spaceship.image.blit(spaceship_picture, (0, 0))
spaceships.add(spaceship)
for i in range(0, retries):
    retry_boxes.append(spaceship_picture_retry)

while invader_count-len(invaders) > 0: # create and add fifty "invader" sprites
    invader = Rectangle(w/2, h/2)
    invader.rect.x = random.randrange(0, canvas.size[0]+1-w/2, w/2) # allow sprite to touch edge but not breach it
    invader.rect.y = random.randrange(0, canvas.size[1]+1-h/2-196, h/2) # 196px space at canvas bottom
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
                    x_increment = 5
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                elif action.key == pygame.K_SPACE: # fire laser
                    laser = Rectangle(10, 20)
                    laser.rect.centerx = spaceship.rect.centerx
                    laser.rect.bottom = spaceship.rect.top + 10 # "+ 10" because update() is called before "laser" sprites are drawn
                    laser.image.fill(YELLOW)
                    if first == True:
                        lasers.add(laser)
                        spaceship_laser_sound.play()
                        first = False
            else:
                x_increment = 0

        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                x_increment = 0
            elif action.key == pygame.K_SPACE:
                first = True

        efficiency.snapshot(action)
        # -------------------
        
    # --- Game logic
    # x_offset += x_increment
    # y_offset += y_increment
    # if canvas.size[0]/2+x_offset < 0:
    #     x_offset = -canvas.size[0]/2 # prevent "spaceship" sprite from breaching left edge, solved for x_offset
    # elif canvas.size[0]/2+x_offset + w > canvas.size[0]:
    #     x_offset = canvas.size[0]/2 - w # simplified
    # if canvas.size[1]/2+y_offset < 0: # note "if"
    #     y_offset = -canvas.size[1]/2 # prevent "spaceship" sprite from breaching top edge, solved for y_offset
    # elif canvas.size[1]/2+y_offset + h > canvas.size[1]:
    #     y_offset = canvas.size[1]/2 - h # simplified
    # spaceship.rect.x = canvas.size[0]/2+x_offset # position and offset "spaceship" sprite <- do earlier
    for i in range(0, abs(x_increment)+1): # increment x-coordinate *abs(x_increment)* many times
        if x_increment == 0:
            pass # don't increment x-coordinate
        else:
            spaceship.rect.x += x_increment/abs(x_increment) # bypass offset for new positions, always += -1 or += 1 depending on direction of movement
        wall_spaceship_hit = pygame.sprite.spritecollide(spaceship, walls, False) # DON'T remove a "wall" sprite, if "spaceship" sprite hits it, returns a list
        # instead...
        if wall_spaceship_hit != []: # align, then break out of above loop
            for wall in wall_spaceship_hit: # wall that spaceship hit
                if x_increment > 0: # moving rightward
                    spaceship.rect.right = wall.rect.left
                else: # moving leftward, x_increment = 0 not hitting wall
                    spaceship.rect.left = wall.rect.right # reverse
            break # no sense in completing above loop, if hit wall

    # spaceship.rect.y = canvas.size[1]-h #/2+y_offset <- do earlier

    # removed = pygame.sprite.spritecollide(spaceship, invaders, True) # remove a "invader" sprite, if "spaceship" sprite collides with it
    for laser in lasers: # "laser" sprite was not created before WHILE loop, for any laser in lasers
        invader_removed = pygame.sprite.spritecollide(laser, invaders, True) # remove a "invader" sprite, if "laser" sprite collides with it
        collisions.add(invader_removed) # when "invader" sprite is removed from invaders group, add it to collisions group
        if invader_removed != []: # or "for invader in removed:"
            # wait1 = 60*5*len(invaders) # update it
            lasers.remove(laser) # remove "laser" sprite, too
            invader_explosion_sound.play()
        # elif laser.rect.y < -20:
        elif laser.rect.bottom < 0:
            lasers.remove(laser) # otherwise, remove "laser" sprite if it exits screen

    if timer != 0 and len(spaceships) != 0 and len(invaders) != 0:
        score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2)
    #### for invader in invaders_hit_list: # FOR each invader in the list
        #### invader.reset_position()
    # counter += 1 # alternative to timer, uses frame rate, but frame rate may fluctuate
    # if counter % (60*5) == 0: # about every 5 seconds
    #     invaders.update(32) # move "invader" sprites downward, requires timer to move slowly
    # if len(spaceships) == 0 or len(invaders) == 0:
    else: # stops lasers from moving when game over or win game
        score = len(collisions)
        lasers.update(0)
        lasers_alt.update(0)

    for invader in invaders:
        # touched = pygame.sprite.spritecollide(invader, spaceships, True)
        # spaceships.remove(touched)
        # if wait1 == 60*5*len(invaders):
        if wait1 == 60*2 and waiting == False:
            spaceship_removed = pygame.sprite.spritecollide(invader, spaceships, True) # similar to pac-man ghosts
        elif wait1 == 60*2 and waiting == True:
            break
        else:
            spaceship_removed = [] # we will wait to check for collision
            wait1 -= 1
            if wait1 == 0:
                # wait1 = 60*5*len(invaders)
                wait1 = 60*2
                waiting = False
            break
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed) # will reposition the spaceship
            # spaceship.retry()
            retry(spaceship)
            retries -= 1
            wait1 -= 1
            waiting = True
            break
    for laser in lasers_alt:
        # if wait2 == 60*5*len(lasers_alt):
        if wait2 == 60*2 and waiting == False:
            spaceship_removed = pygame.sprite.spritecollide(laser, spaceships, True)
        elif wait2 == 60*2 and waiting == True:
        # elif waiting == True:
            break
        else:
            spaceship_removed = [] # we will wait to check for collision
            wait2 -= 1
            if wait2 == 0:
                # wait2 = 60*5*len(lasers_alt)
                wait2 = 60*2
                waiting = False
            break
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed) # repositioning the spaceship
            # spaceship.retry()
            retry(spaceship)
            lasers_alt.remove(laser)
            retries -= 1
            # wait2 = 60*5*len(lasers_alt)
            wait2 -= 1
            waiting = True
            break            
        elif laser.rect.top > canvas.size[1]:
            lasers_alt.remove(laser)
            # wait2 = 60*5*len(lasers_alt)

    for laser in lasers_alt:
        barrier_removed = pygame.sprite.spritecollide(laser, barriers, True)
        if barrier_removed != []:
            lasers_alt.remove(laser)
            # wait2 = 60*5*len(lasers_alt)

    # for laser in lasers:
    #     barrier_removed = pygame.sprite.spritecollide(laser, barriers, True)
    #     if barrier_removed != []:
    #         lasers.remove(laser)
    # --------------
    canvas.clean()
    timer_header = style_header.render("Time Left", False, RED)
    timer_text = style.render(str(timer), False, RED) # ("time remaining", anti-aliased, COLOR)
    score_header = style_header.render("Score", False, GREEN)
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, pygame.Color("black"))
    you_win_text = style.render(None, False, GREEN)
    if timer == 0 or len(spaceships) == 0:
        # # spaceship.image.fill(WHITE)
        # pygame.draw.rect(spaceship.image, WHITE, (0, 0, w, h), width=0)
        # for invader in invaders:
        #     pygame.draw.rect(invader.image, DARKGRAY, (0, 0, w/2, h/2), width=0)
        # for laser in lasers:
        #     laser.image.fill(LIGHTGRAY)
        # for laser in lasers_alt:
        #     laser.image.fill(DARKGRAY)
        # canvas.screen.fill(GRAY)
        # timer_header = style_header.render("Time Left", False, DARKGRAY)
        # timer_text = style.render(str(timer), False, DARKGRAY)
        # score_header = style_header.render("Score", False, DARKGRAY)
        # score_text = style.render(str(score), False, DARKGRAY)
        game_over_text = style.render("Game Over", False, pygame.Color("black"))
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)        
    # sprites.add(invaders, walls, barriers, lasers, lasers_alt, spaceships)
    sprites.empty()
    sprites.add(walls, barriers, invaders, lasers_alt, spaceships, lasers)
    # --- Drawing code
    # pygame.draw.rect(canvas.screen, WHITE, (canvas.size[0]/2, canvas.size[1]/2, 64, 64), width=0)
    # draw_rect(canvas.screen, canvas.size[0]/2, canvas.size[1]/2, 64, 64) # call function and input parameters
    # draw_rect(canvas.screen, canvas.size[0]/2+x_offset, canvas.size[1]/2+y_offset, 64, 64) # call function, input parameters, and rely on keyboard
    # walls.draw(canvas.screen) # draw sprites on screen using group
    # barriers.draw(canvas.screen)
    # invaders.draw(canvas.screen)
    # lasers_alt.draw(canvas.screen)
    # lasers.draw(canvas.screen)
    sprites.draw(canvas.screen)
    canvas.screen.blit(spaceship.image, (spaceship.rect.x, spaceship.rect.y)) # draw sprite on screen, so you can see block
    canvas.screen.blit(timer_header, (10, 10))
    canvas.screen.blit(timer_text, (10, 30)) # copy image of text onto screen at (10, 10)
    for i in range(0, retries):
        canvas.screen.blit(retry_boxes[i], (100+i*w/2, 10))
        retry_boxes[i].set_colorkey(BLACK)
        # if timer == 0:
        #     pygame.draw.rect(retry_boxes[i], WHITE, [0, 0, w/2, h/2], 0)
    canvas.screen.blit(score_header, (canvas.size[0]-score_header.get_width()-10, 10))
    canvas.screen.blit(score_text, (canvas.size[0]-score_text.get_width()-10, 30)) # near top-right corner
    canvas.screen.blit(game_over_text, game_over_text.get_rect(center = canvas.screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument (recall: positional args vs keyword args)
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    canvas.screen.blit(you_win_text, you_win_text.get_rect(center = canvas.screen.get_rect().center))
    # ----------------
    canvas.show()
    efficiency.activate()