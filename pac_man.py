"""
"Pac-Man" Game
"""

import pygame, random
import src.canvas as canvas
from custom.classes import Rectangle

WHITE = pygame.Color("white")
BLACK = pygame.Color("black") # useful if run module on macOS
RED = pygame.Color("red")
GREEN = pygame.Color("green")

x_offset = 50 # don't start on wall
y_offset = 0
x_increment = 0 # speed
y_increment = 0
x_increment_red_ghost = 1 # moving rightward at launch
y_increment_red_ghost = 0
x_increment_green_ghost = 0
y_increment_green_ghost = 1
W_pacman = 64 # these variables are for images
H_pacman = 64
W_pellet = 32
H_pellet = 32
W_ghost = 64
H_ghost = 64

pellets = pygame.sprite.Group() # not pellets = []
collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
pacmen = pygame.sprite.Group()
red_ghosts = pygame.sprite.Group()
green_ghosts = pygame.sprite.Group()
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
pellet_picture = pygame.transform.scale(pellet_picture, (W_pellet, H_pellet))
red_ghost_picture = pygame.image.load('images/red_ghost.png').convert()
green_ghost_picture = pygame.image.load('images/green_ghost.png').convert()
pacman_picture_retries = pygame.transform.scale(pacman_picture, (W_pacman/2, H_pacman/2))

timer = 30 # 30 seconds (multiple of modulo for random walks)
score = 0
count = 0 # for chomp picture
ticks = int()
angle = 0 # redundant
retries = 2

pygame.display.set_caption("QUESTABOX's \"Pac-Man\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

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
    sprite.rect.x = canvas.size[0]/2+x_offset
    sprite.rect.y = canvas.size[1]/2+y_offset
def flip_horizontal(sprite, Bool):
    if sprite in red_ghosts:
        sprite.image = pygame.transform.flip(red_ghost_picture, flip_x=Bool, flip_y=False)
    else:
        sprite.image = pygame.transform.flip(green_ghost_picture, flip_x=Bool, flip_y=False)
    sprite.image.set_colorkey(BLACK)
# ---------------------

# left wall
wall = Rectangle(1, canvas.size[1]) # need at least some thickness
wall.rect.x = -1 # moved walls outside screen
wall.rect.y = 0
walls.add(wall)
# right wall
wall = Rectangle(1, canvas.size[1])
wall.rect.x = canvas.size[0]
wall.rect.y = 0
walls.add(wall)
# top wall
wall = Rectangle(canvas.size[0]-2, 1) # no overlap
wall.rect.x = 1
wall.rect.y = -1
walls.add(wall)
# bottom wall
wall = Rectangle(canvas.size[0]-2, 1)
wall.rect.x = 1
wall.rect.y = canvas.size[1]
walls.add(wall)

# inner top wall
wall = Rectangle(canvas.size[0]-200, 10) # leave room around walls
wall.rect.x = 100
wall.rect.y = 100
walls.add(wall)
# inner bottom wall
wall = Rectangle(canvas.size[0]-200, 10)
wall.rect.x = 100
wall.rect.y = canvas.size[1]-110 # wall is 10px thick
walls.add(wall)
# inner middle wall
wall = Rectangle(10, canvas.size[1]-220)
wall.rect.x = canvas.size[0]/2-5 # places wall in center
wall.rect.y = 110
walls.add(wall)

# all walls
for wall in walls:
    wall.image.fill(WHITE)

pacman = Rectangle(W_pacman, H_pacman)
pacman.rect.x = canvas.size[0]/2+x_offset
pacman.rect.y = canvas.size[1]/2+y_offset
pacman.image.blit(pacman_picture, (0, 0))
pacmen.add(pacman)

while True: # put green "ghost" sprite first, else when try to get ghost moving it will move prematurely
    ghost = Rectangle(W_ghost, H_ghost)
    ghost.rect.x = random.randrange(0, canvas.size[0]+1-W_ghost) # don't need step_size
    ghost.rect.y = random.randrange(0, canvas.size[1]+1-H_ghost)
    ghost.image.blit(green_ghost_picture, (0, 0))
    green_ghosts.add(ghost)
    stuck = pygame.sprite.spritecollide(ghost, walls, False)
    if stuck != []:
        green_ghosts.remove(ghost)
    else:
        break

while True:
    ghost = Rectangle(W_ghost, H_ghost)
    ghost.rect.x = random.randrange(0, canvas.size[0]+1-W_ghost)
    ghost.rect.y = random.randrange(0, canvas.size[1]+1-H_ghost)
    ghost.image.blit(red_ghost_picture, (0, 0))
    red_ghosts.add(ghost)
    stuck = pygame.sprite.spritecollide(ghost, walls, False)
    if stuck != []:
        red_ghosts.remove(ghost)
    else:
        break

while 50-len(pellets) > 0: # create and add fifty "pellet" sprites
    pellet = Rectangle(W_pellet, H_pellet)
    pellet.rect.x = random.randrange(0, canvas.size[0]+1-W_pellet, W_pellet) # allow sprite to touch edge but not breach it
    pellet.rect.y = random.randrange(0, canvas.size[1]+1-H_pellet, H_pellet)
    pellet.image.blit(pellet_picture, (0, 0))
    pygame.sprite.spritecollide(pellet, pellets, True) # remove any sprite in same position, you cannot check if sprite is already in group or already belongs to group since each sprite is unique
    pellets.add(pellet)
    for wall in walls:
        pygame.sprite.spritecollide(wall, pellets, True)

while True: # keeps screen open
    for action in pygame.event.get(): # check for user input when open screen
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()

        elif action.type == pygame.USEREVENT: # for timer, "elif" means else if
            if timer == 0 or len(pacmen) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # disable timer
                game_over_sound.play()
            elif len(pellets) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else: # after one second
                timer -= 1
                if timer % 10 == 0: # every 10 seconds
                    y_increment_green_ghost = random.choice([-1, 0, 1])
                    if y_increment_green_ghost == 0:
                        x_increment_green_ghost = random.choice([-1, 1])
                    else: # when y_increment_green_ghost = -1 or 1
                        x_increment_green_ghost = 0 # always moving
                elif timer % 5 == 0:
                    x_increment_red_ghost = random.choice([-1, 0, 1])
                    if x_increment_red_ghost == 0:
                        y_increment_red_ghost = random.choice([-1, 1])
                    else:
                        y_increment_red_ghost = 0

        # --- Keyboard events
        elif action.type == pygame.KEYDOWN:
            if timer != 0 and len(pellets) != 0 and len(pacmen) != 0:
                if action.key == pygame.K_RIGHT:
                    x_increment = 5
                    angle = 0
                    turn(pacman, angle) # placing here also helps with using keyboard combination to take screenshots
                    count += 1
                    if count % 15 == 0: # delay
                        pacman_walk_sound.play()
                if action.key == pygame.K_UP: # recall that y increases going downward
                    y_increment = -5
                    angle = 90
                    turn(pacman, angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                if action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                    turn(pacman, angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                if action.key == pygame.K_DOWN:
                    y_increment = 5
                    angle = 270
                    turn(pacman, angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
            else:
                x_increment = 0
                y_increment = 0
                
        elif action.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
            count = 0
            turn(pacman, angle)
            ticks = pygame.time.get_ticks()
        # -------------------
        
    # --- Game logic
    pacman.rect.x += x_increment
    wall_pacman_hit_x = pygame.sprite.spritecollide(pacman, walls, False) # don't remove wall, returns a list
    for wall in wall_pacman_hit_x: # wall that pacman hit
        if x_increment > 0:
            pacman.rect.right = wall.rect.left
        else: # x_increment = 0 not hitting a wall
            pacman.rect.left = wall.rect.right
    
    pacman.rect.y += y_increment
    wall_pacman_hit_y = pygame.sprite.spritecollide(pacman, walls, False)
    for wall in wall_pacman_hit_y:
        if y_increment > 0:
            pacman.rect.bottom = wall.rect.top
        else: # y_increment = 0 not hitting a wall
            pacman.rect.top = wall.rect.bottom

    pellet_removed = pygame.sprite.spritecollide(pacman, pellets, True) # remove pellet
    collisions.add(pellet_removed) # when pellet is removed, add it to collisions group

    for ghost in red_ghosts:
        wall_ghost_hit_x = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_x != []:
            x_increment_red_ghost *= -1
        ghost.rect.x += x_increment_red_ghost # increment here, else ghost may get stuck on wall

        wall_ghost_hit_y = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_y != []:
            y_increment_red_ghost *= -1
        ghost.rect.y += y_increment_red_ghost

    for ghost in green_ghosts:
        wall_ghost_hit_x = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_x != []:
            x_increment_green_ghost *= -1
        ghost.rect.x += x_increment_green_ghost

        wall_ghost_hit_y = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_y != []:
            y_increment_green_ghost *= -1
        ghost.rect.y += y_increment_green_ghost

    for ghost in red_ghosts:
        pacman_removed = pygame.sprite.spritecollide(ghost, pacmen, True)
        if pacman_removed != []: # we will wait to check for collision
            ghost_hit_sound.play()
        if pacman_removed != [] and retries > 0:
            pacmen.add(pacman_removed) # will reposition pac-man
            retry(pacman)
            retries -= 1

    for ghost in green_ghosts:
        pacman_removed = pygame.sprite.spritecollide(ghost, pacmen, True)
        if pacman_removed != []:
            ghost_hit_sound.play()
        if pacman_removed != [] and retries > 0:
            pacmen.add(pacman_removed)
            retry(pacman)
            retries -= 1

    for ghost in red_ghosts: # put down here, since there are two ways increment changes sign: choice() and collisions
        if x_increment_red_ghost < 0 or y_increment_red_ghost < 0: # ghost moving leftward or upward
            flip_horizontal(ghost, True)
        elif timer != 0 and len(pacmen) != 0 and len(pellets) != 0:
            flip_horizontal(ghost, False)
    for ghost in green_ghosts:
        if x_increment_green_ghost < 0 or y_increment_green_ghost < 0:
            flip_horizontal(ghost, True)
        elif timer != 0 and len(pacmen) != 0 and len(pellets) != 0:
            flip_horizontal(ghost, False)

    if timer != 0 and len(pacmen) != 0 and len(pellets) != 0:
        pass
    else: # stops ghosts from moving when game over or win game
        x_increment_red_ghost = 0
        y_increment_red_ghost = 0
        x_increment_green_ghost = 0
        y_increment_green_ghost = 0
    score = len(collisions)

    if retries == 2: # default
        pacman_retries_box_1 = pacman_picture_retries
        pacman_retries_box_2 = pacman_picture_retries
    elif retries == 1:
        pacman_retries_box_1 = pacman_picture_retries
        pacman_retries_box_2 = pygame.Surface((0, 0)) # blank box
    else:
        pacman_retries_box_1 = pygame.Surface((0, 0))
        pacman_retries_box_2 = pygame.Surface((0, 0))
    pacman_retries_box_1.set_colorkey(BLACK)
    pacman_retries_box_2.set_colorkey(BLACK)
    # --------------

    canvas.clean()
    timer_header = style_header.render("Time Left", False, RED) # "False" for anti-aliased
    timer_text = style.render(str(timer), False, RED)
    score_header = style_header.render("Score", False, GREEN)
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, BLACK)
    you_win_text = style.render(None, False, GREEN)
    if timer == 0 or len(pacmen) == 0:
        game_over_text = style.render("Game Over", False, BLACK)
    if len(pellets) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    sprites.empty()
    sprites.add(walls, pellets, red_ghosts, green_ghosts, pacmen) # pacmen is redundant

    # --- Drawing code
    sprites.draw(canvas.screen)
    canvas.screen.blit(pacman.image, (pacman.rect.x, pacman.rect.y)) # so you can see it, even if game over
    canvas.screen.blit(timer_header, (10, 10))
    canvas.screen.blit(timer_text, (10, 30))
    canvas.screen.blit(pacman_retries_box_1, (100, 10)) # to right of timer
    canvas.screen.blit(pacman_retries_box_2, (100+W_pacman/2, 10)) # side-by-side
    canvas.screen.blit(score_header, (canvas.size[0]-score_header.get_width()-10, 10)) # near top-right corner
    canvas.screen.blit(score_text, (canvas.size[0]-score_text.get_width()-10, 30))
    canvas.screen.blit(game_over_text, game_over_text.get_rect(center = canvas.screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    canvas.screen.blit(you_win_text, you_win_text.get_rect(center = canvas.screen.get_rect().center))
    # ----------------

    canvas.show()
    if pygame.time.get_ticks() - ticks > 10000:
        canvas.clock.tick(1)
