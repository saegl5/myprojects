import pygame # import the pygame module
import sys # import the sys module
import random # import the random module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
BLACK = pygame.Color("black") # useful if run module on macOS
YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
LIGHTGRAY = pygame.Color("light gray")
GRAY = pygame.Color("gray")
DARKGRAY = pygame.Color("dark gray")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
x_increment_red_ghost = 1 # offsetting directly, moving at launch, direction optional
x_increment_green_ghost = 0
y_increment = 0
y_increment_red_ghost = 0 # offsetting directly
y_increment_green_ghost = 1
W = 64 # "pacman" sprite width reference
H = 64 # "pacman" sprite height reference
pellets = pygame.sprite.Group() # create a list for "pellet" sprites, no longer pellets = [], Group() is class
# collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
pacmen = pygame.sprite.Group()
timer = 30 # set timer for 30 seconds (multiple of modulo for random walks)
score = 0 # initialize score
style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
count = 0 # for chomp picture
ticks = int() # for saving energy
# angle = 0 # redundant
game_over_sound = pygame.mixer.Sound('Sounds/game_over.ogg') # Source: https://kenney.nl/assets/voiceover-pack
you_win_sound = pygame.mixer.Sound('Sounds/you_win.ogg') # Source: https://kenney.nl/assets/voiceover-pack
pacman_picture = pygame.image.load('Images/pac.png').convert() # Edited from source: https://opengameart.org/content/pacman-tiles
# pacman_picture.set_colorkey(BLACK)
pacman_picture_alt = pygame.image.load('Images/pac_chomp.png').convert() # my picture from pac.png
# pacman_picture_alt.set_colorkey(BLUE)
pellet_picture = pygame.image.load('Images/dot.png').convert() # Edited from source: https://opengameart.org/content/pacman-tiles (changed black to (1, 1, 1), too)
pellet_picture = pygame.transform.scale(pellet_picture, (int(W/2), int(H/2))) # int() addresses "TypeError: integer argument expected, got float"
# pellet_picture.set_colorkey(BLACK)
red_ghost_picture = pygame.image.load('Images/red_ghost.png').convert() # corrected profile
# red_ghost_picture = pygame.transform.scale(red_ghost_picture, (int(W/2), int(H/2)))
green_ghost_picture = pygame.image.load('Images/green_ghost.png').convert() # corrected profile
# green_ghost_picture = pygame.transform.scale(green_ghost_picture, (int(W/2), int(H/2)))
retries = 2

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, x, y, W, H): # define a constructor, class accepts picture, width, height, x-coordinate, and y-coordinate parameters, must type "__" before and after "init," requires "self"
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (W, H) # define size of image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # draw shape on image, draw over entire image with (0, 0, W, H), where (0, 0) is located at image's top-left corner
        # self.image.blit(sprite_picture, (0, 0))
        self.image.set_colorkey(BLACK) # windows only and newer python
        self.rect = self.image.get_rect() # pair image with rectangle object, where (rect.x, rect.y) is located at rectangle object's top-left corner
        # sprite consists of image and rectangle object
        self.rect.x = x
        self.rect.y = y
    # def update(self):
        # self.rect.y += 32 # increase sprites' rect.y by 32 pixels
    def turn(self, angle): # calling with sprite, not group
        if count == 1: # in case there is a quick KEYDOWN and KEYUP event
            self.image.blit(pacman_picture_alt, (0, 0))
        if count == 5: # else appears to chomp too long
            self.image = pygame.transform.rotate(pacman_picture, angle)         
        if count % 10 == 0:
            self.image.blit(pacman_picture_alt, (0, 0))
        if count % 20 == 0:
            self.image = pygame.transform.rotate(pacman_picture, angle)         
        self.image.set_colorkey(BLACK)
    def retry(self):
        self.rect.x = size[0]/2
        self.rect.y = size[1]/2
    # def flip(self, sign):
    #     if sign < 0:
    #         red_ghost.image.blit(ghost_picture_1_alt, (0, 0))
    #         green_ghost.image.blit(ghost_picture_2_alt, (0, 0))
    #     elif sign > 0:
    #         red_ghost.image.blit(ghost_picture_1, (0, 0))
    #         green_ghost.image.blit(ghost_picture_2, (0, 0))

# ---------------------
# inner walls:
wall = Rectangle(100, 100, size[0]-100-100, 10)
walls.add(wall)
wall = Rectangle(100, size[1]-10-100, size[0]-100-100, 10)
walls.add(wall)
wall = Rectangle(size[0]/2-10/2, 100+10, 10, size[1]-100-100-10-10)
walls.add(wall)
for wall in walls:
    wall.image.fill(LIGHTGRAY)

# outer walls (left, right, top, bottom):
wall = Rectangle(0-1, 0, 1, size[1]) # need at least some thickness, moved walls outside display
walls.add(wall)
wall = Rectangle(size[0]-1+1, 0, 1, size[1])
walls.add(wall)
wall = Rectangle(1, 0-1, size[0]-2, 1)
walls.add(wall)
wall = Rectangle(1, size[1]-1+1, size[0]-2, 1)
walls.add(wall)

pacman = Rectangle(size[0]/2+x_offset, size[1]/2+y_offset, W, H) # creates a "pacman" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
pacman.image.blit(pacman_picture, (0, 0))
pacmen.add(pacman)

# for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "pellet" sprites
while 50-len(pellets) > 0: # create and add fifty "pellet" sprites
    x = random.randrange(0, size[0]+1-W/2, W/2) # position "pellet" sprite, allow it to touch edge but not breach it
    y = random.randrange(0, size[1]+1-H/2, H/2) #  want "pellet" sprites equally spaced, also mitigates overlap
    pellet = Rectangle(x, y, W/2, H/2) # create a "pellet" sprite
    pellet.image.blit(pellet_picture, (0, 0))
    pygame.sprite.spritecollide(pellet, pellets, True) # remove any "pellet" sprite in list in same position, essentially preventing "pellet" sprites from taking same position and essentially preventing overlap, you cannot check if sprite is in group or belongs to group since each sprite is unique
    pellets.add(pellet) # add "pellet" sprite to list, no longer append
    for wall in walls:
        pygame.sprite.spritecollide(wall, pellets, True) # remove any "pellet" sprite in list in same position

while True:
    x = random.randrange(0, size[0]+1-W, W)
    y = random.randrange(0, size[1]+1-H, H)
    red_ghost = Rectangle(x, y, W, H)
    red_ghost.image.blit(red_ghost_picture, (0, 0))
    stuck = pygame.sprite.spritecollide(red_ghost, walls, False)
    if stuck:
        red_ghost.kill()
        continue # create new sprite
    else:
        break # exit loop, not quitting game

while True:
    x = random.randrange(0, size[0]+1-W, W)
    y = random.randrange(0, size[1]+1-H, H)
    green_ghost = Rectangle(x, y, W, H)
    green_ghost.image.blit(green_ghost_picture, (0, 0))
    stuck = pygame.sprite.spritecollide(green_ghost, walls, False)
    if stuck:
        green_ghost.kill()
        continue
    else:
        break

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        elif action.type == pygame.USEREVENT:
            if timer == 0 or len(pacmen) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # stop timer
                game_over_sound.play()
            elif len(pellets) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else: # after one second
                timer -= 1 # decrement timer
                if timer % 5 == 0:
                    x_increment_red_ghost = random.randint(-1, 1) # let Python choose direction and speed
                    if x_increment_red_ghost == 0:
                        y_increment_red_ghost = random.choice([-1, 1]) # always moving
                    # red_ghost.image = pygame.transform.flip(red_ghost.image, True, False)
                    # red_ghost.image.set_colorkey(BLACK)                    
                    y_increment_green_ghost = random.randint(-1, 1)
                    if y_increment_green_ghost == 0:
                        x_increment_green_ghost = random.choice([-1, 1])
                    # green_ghost.image = pygame.transform.flip(green_ghost.image, True, False)
                    # green_ghost.image.set_colorkey(BLACK)
                if timer % 10 == 0:
                    y_increment_red_ghost = random.randint(-1, 1) # let Python choose direction and speed
                    if y_increment_red_ghost == 0:
                        x_increment_red_ghost = random.choice([-1, 1]) # always moving
                    x_increment_green_ghost = random.randint(-1, 1)
                    if x_increment_green_ghost == 0:
                        y_increment_green_ghost = random.choice([-1, 1])

                # if timer % 5 == 0: # every 5 seconds
                # red_ghost.rect.x += x_increment_ghost # move "ghost" sprites downward
                # green_ghost.rect.y += y_increment_ghost # move "ghost" sprites downward
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0 and len(pellets) != 0 and len(pacmen) != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                    angle = 0
                    pacman.turn(angle) # place in IF statement, if using keyboard combination to take screenshots
                    count += 1
                elif action.key == pygame.K_UP:
                    y_increment = -5
                    angle = 90
                    pacman.turn(angle)
                    count += 1
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                    pacman.turn(angle)
                    count += 1
                elif action.key == pygame.K_DOWN:
                    y_increment = 5 # note "y_increment," and recall that y increases going downward
                    angle = 270
                    pacman.turn(angle)
                    count += 1
                else: # without "else," do nothing
                    x_increment = 0
                    y_increment = 0
            else: # without "else," do nothing
                x_increment = 0
                y_increment = 0
        elif action.type == pygame.KEYUP:
            ticks = pygame.time.get_ticks()
            x_increment = 0
            y_increment = 0
            count = 0
            pacman.turn(angle)
            # if action.key == pygame.K_RIGHT: 
            # pacman.image.blit(pacman_picture, (0, 0))

        # -------------------------
    # --- Game logic
    # x_offset += x_increment
    # y_offset += y_increment

    # if size[0]/2+x_offset < 0:
    #     x_offset = -size[0]/2 # prevent "pacman" and "ghost" sprites from breaching left edge, solved for x_offset
    # elif size[0]/2+x_offset + W > size[0]:
    #     x_offset = size[0]/2 - W # simplified
    # if size[1]/2+y_offset < 0: # note "if"
    #     y_offset = -size[1]/2 # prevent "pacman" and "ghost" sprites from breaching top edge, solved for y_offset
    # elif size[1]/2+y_offset + H > size[1]:
    #     y_offset = size[1]/2 - H # simplified

    # pacman.rect.x = size[0]/2+x_offset # position and offset "pacman" sprite <- do earlier
    pacman.rect.x += x_increment # bypass offset for new positions
    wall_pacman_hit_x = pygame.sprite.spritecollide(pacman, walls, False) # DON'T remove a "wall" sprite, if "pacman" sprite hits it, returns a list
    # instead...
    for wall in wall_pacman_hit_x: # wall that pacman hit
        if x_increment > 0: # moving rightward
            pacman.rect.right = wall.rect.left
        else: # moving leftward, x_increment = 0 not hitting wall
            pacman.rect.left = wall.rect.right # reverse
    
    # pacman.rect.y = size[1]/2+y_offset <- do earlier
    pacman.rect.y += y_increment # bypass offset for new positions, must put here or else goes around wall
    wall_pacman_hit_y = pygame.sprite.spritecollide(pacman, walls, False)
    for wall in wall_pacman_hit_y:
        if y_increment > 0:
            pacman.rect.bottom = wall.rect.top
        else:
            pacman.rect.top = wall.rect.bottom

    # if timer % 10 == 0:
    red_ghost.rect.x += x_increment_red_ghost # move "ghost" sprites rightward
    wall_red_ghost_hit_x = pygame.sprite.spritecollide(red_ghost, walls, False)
    if len(wall_red_ghost_hit_x) != 0:
        x_increment_red_ghost *= -1

    red_ghost.rect.y += y_increment_red_ghost # move "ghost" sprites downward
    wall_red_ghost_hit_y = pygame.sprite.spritecollide(red_ghost, walls, False)
    if len(wall_red_ghost_hit_y) != 0:
        y_increment_red_ghost *= -1

    green_ghost.rect.x += x_increment_green_ghost
    wall_green_ghost_hit_x = pygame.sprite.spritecollide(green_ghost, walls, False)
    if len(wall_green_ghost_hit_x) != 0:
        x_increment_green_ghost *= -1

    green_ghost.rect.y += y_increment_green_ghost
    wall_green_ghost_hit_y = pygame.sprite.spritecollide(green_ghost, walls, False)
    if len(wall_green_ghost_hit_y) != 0:
        y_increment_green_ghost *= -1

    # red_ghost.rect.x = size[0]/2+x_offset
    # green_ghost.rect.y = size[1]/2+y_offset
    # pygame.sprite.spritecollide(pacman, ghosts, True) # remove a "ghost" sprite, if "pacman" sprite collides with it
    pellet_removed = pygame.sprite.spritecollide(pacman, pellets, True) # remove a "pellet" sprite, if "pacman" sprite collides with it
    # collisions.add(removed)
    if len(pellet_removed) != 0: # or "for pellet in removed:"
        score += 1
    # if timer != 0:
        # score = len(collisions)
    pacman_removed_a = pygame.sprite.spritecollide(green_ghost, pacmen, True)
    if len(pacman_removed_a) != 0 and retries > 0:
        pacmen.add(pacman_removed_a)
        pacman.retry()
        retries -= 1
    pacman_removed_b = pygame.sprite.spritecollide(red_ghost, pacmen, True)
    if len(pacman_removed_b) != 0 and retries > 0:
        pacmen.add(pacman_removed_b)
        pacman.retry()
        retries -= 1
    if len(pacmen) == 0:
        x_increment_green_ghost = 0
        y_increment_green_ghost = 0
        x_increment_red_ghost = 0
        y_increment_red_ghost = 0
    # --------------
    screen.fill(BLUE) # clear the display
    timer_text = style.render(str(timer), True, RED) # ("time remaining", anti-aliased, COLOR)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, BLACK)
    you_win_text = style.render(None, True, GREEN)
    if timer == 0 or len(pacmen) == 0:
        pacman.image.fill(WHITE)
        for pellet in pellets:
            pygame.draw.rect(pellet.image, LIGHTGRAY, (0, 0, W/2, H/2), width=0)
        for wall in walls:
            wall.image.fill(DARKGRAY)
        pygame.draw.rect(green_ghost.image, LIGHTGRAY, (0, 0, W, H), width = 0)
        pygame.draw.rect(red_ghost.image, LIGHTGRAY, (0, 0, W, H), width = 0)
        screen.fill(GRAY)
        timer_text = style.render(str(timer), True, DARKGRAY)
        score_text = style.render(str(score), True, DARKGRAY)
        game_over_text = style.render("Game Over", True, BLACK)
    if len(pellets) == 0:
        you_win_text = style.render("WINNER!", True, GREEN)
    # --- Drawing code
    walls.draw(screen) # draw sprites on screen using list
    pellets.draw(screen)
    screen.blit(red_ghost.image, (red_ghost.rect.x, red_ghost.rect.y))
    screen.blit(green_ghost.image, (green_ghost.rect.x, green_ghost.rect.y))
    screen.blit(pacman.image, (pacman.rect.x, pacman.rect.y)) # draw sprite on screen
    screen.blit(timer_text, (10, 10)) # copy image of text onto screen at (10, 10)
    screen.blit(score_text, (size[0]-score_text.get_width()-10, 10)) # near top-right corner
    screen.blit(game_over_text, game_over_text.get_rect(center = screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument (recall: positional args vs keyword args)
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    screen.blit(you_win_text, you_win_text.get_rect(center = screen.get_rect().center))
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
    if pygame.time.get_ticks() - ticks > 10000: # unless user stops playing for more than 10 seconds
        # pygame.time.set_timer(pygame.USEREVENT, 0)
        clock.tick(1) # in which case minimize the frame rate
    # if pygame.time.set_timer(pygame.USEREVENT, 0) == True:
        # print("true") # and pygame.time.get_ticks() - ticks <= 10000:
        # pygame.time.set_timer(pygame.USEREVENT, 1000)