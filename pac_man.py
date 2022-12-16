"""
"Pac-Man" Game
"""

import pygame, random
import src.canvas as canvas
from custom.energy import time_stamp, save_energy
from custom.classes import Rectangle
from custom.functions import left_wall, right_wall, top_wall, bottom_wall

pygame.display.set_caption("QUESTABOX's \"Pac-Man\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
X_OFFSET = 50 # don't start on wall
Y_OFFSET = 0
W = 64 # "pacman" sprite width reference
H = 64 # "pacman" sprite height reference
x_inc = 0 # speed
y_inc = 0
x_inc_red_ghost = 1 # moving rightward at launch
y_inc_red_ghost = 0

pellets = pygame.sprite.Group() # not pellets = []
collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
pacmen = pygame.sprite.Group()
red_ghosts = pygame.sprite.Group()
sprites = pygame.sprite.Group() # all sprites

style = pygame.font.Font(None, 100) # faster than SysFont(), "None" utilizes default font (i.e., freesansbold.ttf)
style_header = pygame.font.Font(None, 30)
style_header.set_italic(True)

game_over_sound = pygame.mixer.Sound('sounds/game_over.ogg')
you_win_sound = pygame.mixer.Sound('sounds/you_win.ogg')
pacman_walk_sound = pygame.mixer.Sound('sounds/footstep.ogg')
ghost_hit_sound = pygame.mixer.Sound('sounds/hit.ogg')

pacman_picture = pygame.image.load('images/pac.png').convert()
pacman_picture_alt = pygame.image.load('images/pac_chomp.png').convert()
pellet_picture = pygame.image.load('images/dot.png').convert()
pellet_picture = pygame.transform.scale(pellet_picture, (int(W/2), int(H/2))) # int() addresses "TypeError: integer argument expected, got float"
red_ghost_picture = pygame.image.load('images/red_ghost.png').convert()
pacman_picture_retry = pygame.transform.scale(pacman_picture, (int(W/2), int(H/2)))

PELLET_COUNT = 50
repeated = 0 # times
score = 0
count = 0 # for chomp picture
retries = 2
retry_boxes = []
wait = canvas.fps*2 # if pacman hit by red ghost, 60 fps x 2 seconds
waiting = False # if pacman hit by either
played = False
angle = 0

# --- Functions
def turn(sprite, angle):
    if count == 1: # in case there is a quick KEYDOWN and KEYUP event
        sprite.image.blit(pacman_picture_alt, (0, 0))
    if count == 5: # else appears to chomp too long
        sprite.image = pygame.transform.rotate(pacman_picture, angle)
    if count % 10 == 0:
        sprite.image.blit(pacman_picture_alt, (0, 0))
    if count % 20 == 0:
        sprite.image = pygame.transform.rotate(pacman_picture, angle)
    sprite.image.set_colorkey(BLACK)
def retry(sprite):
    sprite.rect.x = canvas.SIZE[0]/2+X_OFFSET
    sprite.rect.y = canvas.SIZE[1]/2+Y_OFFSET
def flip_horizontal(sprite, Bool):
    if sprite in red_ghosts:
        sprite.image = pygame.transform.flip(red_ghost_picture, flip_x=Bool, flip_y=False)
    sprite.image.set_colorkey(BLACK)
# ---------------------

# outer walls
walls.add(left_wall(), right_wall(), top_wall(), bottom_wall())

# inner top wall
wall = Rectangle(canvas.SIZE[0]-200, 10) # leave room around walls
wall.rect.x = 100
wall.rect.y = 100
walls.add(wall)
# inner bottom wall
wall = Rectangle(canvas.SIZE[0]-200, 10)
wall.rect.x = 100
wall.rect.y = canvas.SIZE[1]-110 # wall is 10px thick
walls.add(wall)
# inner middle wall
wall = Rectangle(10, canvas.SIZE[1]-220)
wall.rect.x = canvas.SIZE[0]/2-5 # places wall in center
wall.rect.y = 110
walls.add(wall)

# all walls
for wall in walls:
    wall.image.fill(WHITE)

pacman = Rectangle(W, H)
pacman.rect.x = canvas.SIZE[0]/2+X_OFFSET
pacman.rect.y = canvas.SIZE[1]/2+Y_OFFSET
pacman.image.blit(pacman_picture, (0, 0))
pacmen.add(pacman)
for i in range(0, retries):
    retry_boxes.append(pacman_picture_retry)

while True:
    ghost = Rectangle(W, H)
    ghost.rect.x = random.randrange(0, canvas.SIZE[0]+1-W)
    ghost.rect.y = random.randrange(0, canvas.SIZE[1]+1-H)
    ghost.image.blit(red_ghost_picture, (0, 0))
    red_ghosts.add(ghost)
    stuck = pygame.sprite.spritecollide(ghost, walls, False)
    obstruct = pygame.sprite.spritecollide(ghost, pacmen, False)
    if stuck != [] or obstruct != []:
        red_ghosts.remove(ghost)
    else:
        break

while PELLET_COUNT-len(pellets) > 0: # create and add fifty "pellet" sprites
    pellet = Rectangle(W/2, H/2)
    pellet.rect.x = random.randrange(0, canvas.SIZE[0], W/2) # allow sprite to touch edge but not breach it
    pellet.rect.y = random.randrange(0, canvas.SIZE[1], H/2)
    pellet.image.blit(pellet_picture, (0, 0))
    pygame.sprite.spritecollide(pellet, pellets, True) # remove any sprite in same position, you cannot check if sprite is already in group or already belongs to group since each sprite is unique
    pellets.add(pellet)
    for wall in walls:
        pygame.sprite.spritecollide(wall, pellets, True)

while True: # keeps screen open
    for event in pygame.event.get(): # check for user input when open screen
        if event.type == pygame.QUIT: # user clicked close button
            canvas.close()

        # --- Keyboard events
        elif event.type == pygame.KEYDOWN:
            if len(pellets) != 0 and len(pacmen) != 0: # game still in play
                if event.key == pygame.K_RIGHT:
                    x_inc = 5
                    angle = 0
                    turn(pacman, angle) # placing here also helps with using keyboard combination to take screenshots
                    count += 1
                    if count % 15 == 0: # delay
                        pacman_walk_sound.play()
                if event.key == pygame.K_UP: # recall that y increases going downward
                    y_inc = -5
                    angle = 90
                    turn(pacman, angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                if event.key == pygame.K_LEFT:
                    x_inc = -5
                    angle = 180
                    turn(pacman, angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                if event.key == pygame.K_DOWN:
                    y_inc = 5
                    angle = 270
                    turn(pacman, angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
            else:
                x_inc = 0
                y_inc = 0
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_inc = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_inc = 0
            count = 0
            pacman.image = pygame.transform.rotate(pacman_picture, angle)
            pacman.image.set_colorkey(BLACK)

        time_stamp(event)
        # -------------------
        
    # --- Game logic
    pacman.rect.x += x_inc
    wall_pacman_hit_x = pygame.sprite.spritecollide(pacman, walls, False) # don't remove wall, returns a list
    for wall in wall_pacman_hit_x: # wall that pacman hit
        if x_inc > 0:
            pacman.rect.right = wall.rect.left
        else: # x_inc = 0 not hitting a wall
            pacman.rect.left = wall.rect.right
    
    pacman.rect.y += y_inc
    wall_pacman_hit_y = pygame.sprite.spritecollide(pacman, walls, False)
    for wall in wall_pacman_hit_y:
        if y_inc > 0:
            pacman.rect.bottom = wall.rect.top
        else: # y_inc = 0 not hitting a wall
            pacman.rect.top = wall.rect.bottom

    pellet_removed = pygame.sprite.spritecollide(pacman, pellets, True) # remove pellet
    collisions.add(pellet_removed) # when pellet is removed, add it to collisions group

    for ghost in red_ghosts:
        wall_ghost_hit_x = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_x != []:
            x_inc_red_ghost *= -1
        ghost.rect.x += x_inc_red_ghost # increment here, else ghost may get stuck on wall

        wall_ghost_hit_y = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_y != []:
            y_inc_red_ghost *= -1
        ghost.rect.y += y_inc_red_ghost

    for ghost in red_ghosts:
        if wait == canvas.fps*2 and waiting == False:
            pacman_removed = pygame.sprite.spritecollide(ghost, pacmen, True)
        elif wait == canvas.fps*2 and waiting == True:
            break        
        else:
            pacman_removed = [] # we will wait to check for collision
            wait -= 1
            if wait == 0:
                wait = canvas.fps*2
                waiting = False
            break
        if pacman_removed != []:
            ghost_hit_sound.play()
        if pacman_removed != [] and retries > 0:
            pacmen.add(pacman_removed) # will reposition pac-man
            retry(pacman)
            retries -= 1
            wait -= 1
            waiting = True
            break # makes timing extra precise

    for ghost in red_ghosts: # put down here, since there are two ways increment changes sign: choice() and collisions
        if x_inc_red_ghost < 0 or y_inc_red_ghost < 0: # ghost moving leftward or upward
            flip_horizontal(ghost, True)
        elif len(pacmen) != 0 and len(pellets) != 0:
            flip_horizontal(ghost, False)

    if len(pacmen) == 0 and played == False:
        pacman.image = pygame.transform.rotate(pacman_picture, angle)
        pacman.image.set_colorkey(BLACK)
        game_over_sound.play()
        played = True
    elif len(pellets) == 0 and played == False:
        pacman.image = pygame.transform.rotate(pacman_picture, angle)
        pacman.image.set_colorkey(BLACK)
        you_win_sound.play()
        played = True
    else:
        repeated += 1
        if repeated % (canvas.fps*5) == 0: # every 5 seconds
            x_inc_red_ghost = random.choice([-1, 0, 1])
            if x_inc_red_ghost == 0:
                y_inc_red_ghost = random.choice([-1, 1])
            else: # when y_inc_red_ghost = -1 or 1
                y_inc_red_ghost = 0 # always moving

    if len(pacmen) != 0 and len(pellets) != 0:
        pass
    else: # stops ghosts from moving when game over or win game
        x_inc_red_ghost = 0
        y_inc_red_ghost = 0
    score = len(collisions)

    # --------------

    canvas.clean()
    score_header = style_header.render("Score", False, GREEN) # "False" for anti-aliased
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, BLACK)
    you_win_text = style.render(None, False, GREEN)
    if len(pacmen) == 0:
        game_over_text = style.render("Game Over", False, BLACK)
    if len(pellets) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    sprites.empty() # redundant
    sprites.add(walls, pellets, red_ghosts, pacmen) # pacmen is redundant

    # --- Drawing code
    sprites.draw(canvas.screen)
    canvas.screen.blit(pacman.image, (pacman.rect.x, pacman.rect.y)) # so you can see it, even if game over
    for i in range(0, retries):
        canvas.screen.blit(retry_boxes[i], (10+i*W/2, 10)) # to right of timer
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