import pygame, random # import the pygame and random module
import src.canvas as canvas
from custom.classes import Rectangle

WHITE = pygame.Color("white")
BLACK = pygame.Color("black") # useful if run module on macOS
YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
CYAN = pygame.Color("cyan")
LIGHTGRAY = pygame.Color("light gray")
GRAY = pygame.Color("gray")
DARKGRAY = pygame.Color("dark gray")

# x_offset = 0 # reordered
# y_offset = 0
x_increment = 0
# y_increment = 0
w = 64 # "spaceship" sprite width reference
x_offset = -w/2
h = 64 # "spaceship" sprite height reference
invaders = pygame.sprite.Group() # create a list for "invader" sprites, no longer invaders = [], Group() is class
# counter = 0 # alternative to timer, uses frame rate, but frame rate may fluctuate
# collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
barriers = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
spaceships = pygame.sprite.Group()
sprites = pygame.sprite.Group() # all sprites
timer = 30 # set timer for 30 seconds (multiple of modulo for invaders.update())
score = 0 # initialize score
style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
style_header = pygame.font.Font(None, 30)
style_header.set_italic(True)
count = 0 # for lunging picture
retries = 2
retry_boxes = []
ticks = int() # for saving energy
game_over_sound = pygame.mixer.Sound('sounds/game_over.ogg') # Source: https://kenney.nl/assets/voiceover-pack
you_win_sound = pygame.mixer.Sound('sounds/you_win.ogg') # Source: https://kenney.nl/assets/voiceover-pack
spaceship_laser_sound = pygame.mixer.Sound('sounds/laserLarge.ogg') # Source: https://www.kenney.nl/assets/sci-fi-sounds
invader_laser_sound = pygame.mixer.Sound('sounds/laserSmall.ogg') # Source: https://www.kenney.nl/assets/sci-fi-sounds
spaceship_explosion_sound = pygame.mixer.Sound('sounds/explosionCrunch.ogg') # Source: https://www.kenney.nl/assets/sci-fi-sounds
invader_explosion_sound = pygame.mixer.Sound('sounds/lowFrequency_explosion.ogg') # Source: https://www.kenney.nl/assets/sci-fi-sounds
spaceship_picture = pygame.image.load('images/ship.png').convert() # Edited from source: https://opengameart.org/content/pixel-space-invaders (changed black to (1, 1, 1), too)
spaceship_picture = pygame.transform.scale(spaceship_picture, (w, h))
spaceship_picture_retry = pygame.transform.scale(spaceship_picture, (w/2, h/2))
# spaceship_picture.set_colorkey(BLACK)
invader_picture = pygame.image.load('images/alien.png').convert() # Edited from source: https://opengameart.org/content/alien-sprite-sheet (changed black to (1, 1, 1), too)
# invader_picture.set_colorkey(BLACK)
invader_picture_alt = pygame.image.load('images/alien_lunging.png').convert() # my picture from alien.png
# invader_picture_alt.set_colorkey(BLACK)
p = 5 # number of partitions
invader_count = 50
# wait1 = 60*5*invader_count # if spaceship hit by invader, 60 fps/invader x ~2 seconds * # invaders, since FOR loop checks all invaders remaining
# wait2 = 0 # if spaceship hit by return fire, since FOR loop checks all return fire remaining, right now none
wait1 = 60*2 # if spaceship hit by invader, 60 fps x 2 seconds
wait2 = wait1 # if spaceship hit by return fire
waiting = False # if spaceship hit by either

pygame.display.set_caption("QUESTABOX's \"Space Invaders\" Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions
# # def draw_rect(display, COLOR, x, y, W, H, width):
# #     pygame.draw.rect(display, COLOR, (x, y, W, H), width)
# def draw_rect(display, x, y, W, H):
#     # Draw a rectangle
#     pygame.draw.rect(display, WHITE, (x, y, W, H), width=0)
def lunge(sprite): # calling with sprite, not group
    if count % 2 == 0: # could also have used timer, using count because did same in pac-man
        sprite.image.blit(invader_picture_alt, (0, 0))
    else:
        sprite.image.blit(invader_picture, (0, 0))
def retry(sprite):
    sprite.rect.centerx = canvas.screen.get_rect().centerx # center along bottom of display
    sprite.rect.y = canvas.size[1]-h
def return_fire(sprite, index):
    # index = 0 # example, more randomized with random.randrange(0, len(invaders))
    sprite.rect.centerx = invaders.sprites()[index].rect.centerx # align its horizontal center with "invader" sprite's horizontal center
    sprite.rect.top = invaders.sprites()[index].rect.bottom # align its bottom with "invader" sprite's bottom
    # self.image = pygame.Surface((10, 20)) # can't do, if want interactions
    sprite.image.fill(RED)
    lasers_alt.add(sprite)
    invader_laser_sound.play()
# ---------------------

# outer walls (only left and right):
wall = Rectangle(1, canvas.size[1]) # need at least some thickness, moved walls outside display
wall.rect.x = 0-1
wall.rect.y = 0
# wall.image.fill(pygame.Color(1, 1, 1)) # windows
walls.add(wall)
wall = Rectangle(1, canvas.size[1])
wall.rect.x = canvas.size[0]-1+1
wall.rect.y = 0
# wall.image.fill(pygame.Color(1, 1, 1)) # windows
walls.add(wall)
# no inner walls

# barriers (left and right)
for i in range(0, p):
    # barrier = Rectangle(50, 400, 250, 25)
    barrier = Rectangle(250/p, 25)
    barrier.rect.x = 50+i*250/p
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

for i in range(0, p):
    # barrier = Rectangle(canvas.size[0]-250-50, 400, 250, 25)
    barrier = Rectangle(250/p, 25)
    barrier.rect.x = canvas.size[0]-250-50+i*250/p
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

# x = canvas.size[0]/2+x_offset # position and offset "spaceship" sprite
# y = canvas.size[1]-h
# spaceship = Rectangle(WHITE, 64, 64) # creates a "spaceship" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
spaceship = Rectangle(w, h) # creates a "spaceship" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
# spaceship.rect.x = canvas.size[0]/2+x_offset # position and offset "spaceship" sprite
spaceship.rect.centerx = canvas.screen.get_rect().centerx # overwrites x above
spaceship.rect.y = canvas.size[1]-h
# ALIGN WITH PAC-MAN!!!
# if one wants to position spaceship randomly, then one could use a WHILE loop as done for pac-man ghosts
spaceship.image.blit(spaceship_picture, (0, 0))
spaceships.add(spaceship)

for i in range(0, retries):
    retry_boxes.append(spaceship_picture_retry)

# for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "invader" sprites
while invader_count-len(invaders) > 0: # create and add fifty "invader" sprites
    # x = random.randrange(0, canvas.size[0]+1-w/2, w/2) # position "invader" sprite, allow it to touch edge but not breach it
    # y = random.randrange(0, canvas.size[1]+1-h/2-196, h/2) # want lots of invaders, but if we use a larger step_size, many invaders may overlap, "-100" leaves space at bottom of canvas, "-96" leaves more space at bottom of canvas and want "invader" sprites equally spaced, also mitigates overlap
    # invader = Rectangle(YELLOW, 32, 32) # create a "invader" sprite
    invader = Rectangle(w/2, h/2) # create a "invader" sprite
    invader.rect.x = random.randrange(0, canvas.size[0]+1-w/2, w/2) # position "invader" sprite, allow it to touch edge but not breach it
    invader.rect.y = random.randrange(0, canvas.size[1]+1-h/2-196, h/2) # want lots of invaders, but if we use a larger step_size, many invaders may overlap, "-100" leaves space at bottom of canvas, "-96" leaves more space at bottom of canvas and want "invader" sprites equally spaced, also mitigates overlap
    invader.image.blit(invader_picture, (0, 0))
    pygame.sprite.spritecollide(invader, invaders, True) # remove any "invader" sprite in same position, essentially preventing "invader" sprites from taking same position and essentially preventing overlap, you cannot check if sprite is in group or belongs to group since each sprite is unique
    invaders.add(invader) # add "invader" sprite to list, no longer append

# we will create "laser" sprites later
first = True # but only first one

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
        elif action.type == pygame.USEREVENT:
            if timer == 0 or len(spaceships) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # stop timer, "invader" sprites stop moving too
                game_over_sound.play()
            elif len(invaders) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else: # after one second
                timer -= 1 # decrement timer
                if timer % 5 == 0: # every 5 seconds, divides into timer evenly
                    invaders.update(32) # move "invader" sprites downward
                for invader in invaders:
                    # invader.lunge() 
                    lunge(invader)   
                count += 1
                if timer % 4 == 0 and len(invaders) > 0: # some number not multiple of 5
                    laser = Rectangle(6, 40) # create "laser" sprite
                    # laser.return_fire(0)
                    return_fire(laser, 0)
                    # wait2 = 60*5*len(lasers_alt)
                if timer % 7 == 0 and len(invaders) > 1: # some number not multiple of 5
                    laser = Rectangle(6, 40) # create "laser" sprite
                    # laser.return_fire(1)
                    return_fire(laser, 1)
                    # wait2 = 60*5*len(lasers_alt)
                if timer % 11 == 0 and len(invaders) > 2: # some number not multiple of 5
                    laser = Rectangle(6, 40) # create "laser" sprite
                    # laser.return_fire(2)
                    return_fire(laser, 2)
                    # wait2 = 60*5*len(lasers_alt)
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0 and len(invaders) != 0 and len(spaceships) != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                # elif action.key == pygame.K_DOWN:
                #     y_increment = 5 # note "y_increment," and recall that y increases going downward
                # elif action.key == pygame.K_UP:
                #     y_increment = -5
                elif action.key == pygame.K_SPACE: # fire laser
                    # laser = Rectangle(CYAN, 5, 20) # create "laser" sprite 
                    laser = Rectangle(10, 20) # create "laser" sprite
                    laser.image.fill(CYAN)
                    laser.rect.centerx = spaceship.rect.centerx # align it with "spaceship" sprite's horizontal center
                    laser.rect.bottom = spaceship.rect.top + 10 # align its bottom with "spaceship" sprite's top, "+ 10" because update() is called before "laser" sprites are drawn (could probably have also drawn spaceship after lasers)
                    if first == True:
                        lasers.add(laser)
                        spaceship_laser_sound.play()
                        first = False
            else: # without "else," do nothing
                x_increment = 0
                # y_increment = 0
        elif action.type == pygame.KEYUP:
            ticks = pygame.time.get_ticks()
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                x_increment = 0
            if action.key == pygame.K_SPACE: # was elif
                first = True
            # y_increment = 0
        # -------------------------
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
        # collisions.add(removed)
        if invader_removed != []: # or "for invader in removed:"
            # wait1 = 60*5*len(invaders) # update it
            lasers.remove(laser) # remove "laser" sprite, too
            score += 1
            invader_explosion_sound.play()
        # elif laser.rect.y < -20:
        elif laser.rect.bottom < 0:
            lasers.remove(laser) # otherwise, remove "laser" sprite if it exits screen
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
    if timer != 0 and len(spaceships) != 0 and len(invaders) != 0:
        # score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2)
    #### for invader in invaders_hit_list: # FOR each invader in the list
        #### invader.reset_position()
    # counter += 1 # alternative to timer, uses frame rate, but frame rate may fluctuate
    # if counter % (60*5) == 0: # about every 5 seconds
    #     invaders.update(32) # move "invader" sprites downward, requires timer to move slowly
    # if len(spaceships) == 0 or len(invaders) == 0:
    else: # stops lasers from moving when game over or win game
        lasers.update(0)
        lasers_alt.update(0)

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
    if pygame.time.get_ticks() - ticks > 10000: # unless user stops playing for more than 10 seconds
        canvas.clock.tick(1) # in which case minimize the frame rate
