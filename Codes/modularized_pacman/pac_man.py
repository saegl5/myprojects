import pygame, random # import the pygame and random module
import src.canvas as canvas

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

clock = pygame.time.Clock() # define "clock"
x_offset = 50 # reordered
y_offset = 0
x_increment = 0
x_increment_red_ghost = 1 # offsetting directly, moving at launch, direction optional
x_increment_green_ghost = 0
y_increment = 0
y_increment_red_ghost = 0 # offsetting directly
y_increment_green_ghost = 1
w = 64 # "pacman" sprite width reference
h = 64 # "pacman" sprite height reference
pellets = pygame.sprite.Group() # create a list for "pellet" sprites, no longer pellets = [], Group() is class
# collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
pacmen = pygame.sprite.Group()
red_ghosts = pygame.sprite.Group()
green_ghosts = pygame.sprite.Group()
timer = 30 # set timer for 30 seconds (multiple of modulo for random walks)
score = 0 # initialize score
style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
style_header = pygame.font.Font(None, 30)
style_header.set_italic(True)
count = 0 # for chomp picture
ticks = int() # for saving energy
# angle = 0 # redundant
game_over_sound = pygame.mixer.Sound('Sounds/game_over.ogg') # Source: https://kenney.nl/assets/voiceover-pack
you_win_sound = pygame.mixer.Sound('Sounds/you_win.ogg') # Source: https://kenney.nl/assets/voiceover-pack
pacman_walk_sound = pygame.mixer.Sound('Sounds/footstep.ogg') # Source: https://www.kenney.nl/assets/rpg-audio
ghost_hit_sound = pygame.mixer.Sound('Sounds/hit.ogg') # Source: https://www.kenney.nl/assets/sci-fi-sounds
pacman_picture = pygame.image.load('Images/pac.png').convert() # Edited from source: https://opengameart.org/content/pacman-tiles
# pacman_picture.set_colorkey(BLACK)
pacman_picture_alt = pygame.image.load('Images/pac_chomp.png').convert() # my picture from pac.png
# pacman_picture_alt.set_colorkey(BLUE)
pellet_picture = pygame.image.load('Images/dot.png').convert() # Edited from source: https://opengameart.org/content/pacman-tiles (changed black to (1, 1, 1), too)
pellet_picture = pygame.transform.scale(pellet_picture, (int(w/2), int(h/2))) # int() addresses "TypeError: integer argument expected, got float"
# pellet_picture.set_colorkey(BLACK)
red_ghost_picture = pygame.image.load('Images/red_ghost.png').convert() # corrected profile
# red_ghost_picture = pygame.transform.scale(red_ghost_picture, (int(w/2), int(h/2)))
green_ghost_picture = pygame.image.load('Images/green_ghost.png').convert() # corrected profile
# green_ghost_picture = pygame.transform.scale(green_ghost_picture, (int(w/2), int(h/2)))
pacman_picture_retry = pygame.transform.scale(pacman_picture, (int(w/2), int(h/2)))
retries = 2
retry_boxes = []

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, x, y, w, h): # define a constructor, class accepts picture, width, height, x-coordinate, and y-coordinate parameters, must type "__" before and after "init," requires "self"
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (w, h) # define size of image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        # pygame.draw.rect(self.image, COLOR, (0, 0, w, h), width=0) # draw shape on image, draw over entire image with (0, 0, w, h), where (0, 0) is located at image's top-left corner
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
        self.rect.x = canvas.size[0]/2+x_offset
        self.rect.y = canvas.size[1]/2+y_offset
    def flip(self, Bool):
        if self in red_ghosts:
            self.image = pygame.transform.flip(red_ghost_picture, flip_x=Bool, flip_y=False)
        else:
            self.image = pygame.transform.flip(green_ghost_picture, flip_x=Bool, flip_y=False)
        self.image.set_colorkey(BLACK)
    # def flip(self, sign):
    #     if sign < 0:
    #         red_ghost.image.blit(ghost_picture_1_alt, (0, 0))
    #         green_ghost.image.blit(ghost_picture_2_alt, (0, 0))
    #     elif sign > 0:
    #         red_ghost.image.blit(ghost_picture_1, (0, 0))
    #         green_ghost.image.blit(ghost_picture_2, (0, 0))

# ---------------------
# inner walls:
wall = Rectangle(100, 100, canvas.size[0]-100-100, 10)
walls.add(wall)
wall = Rectangle(100, canvas.size[1]-10-100, canvas.size[0]-100-100, 10)
walls.add(wall)
wall = Rectangle(canvas.size[0]/2-10/2, 100+10, 10, canvas.size[1]-100-100-10-10)
walls.add(wall)
for wall in walls:
    wall.image.fill(LIGHTGRAY)

# outer walls (left, right, top, bottom):
wall = Rectangle(0-1, 0, 1, canvas.size[1]) # need at least some thickness, moved walls outside display
walls.add(wall)
wall = Rectangle(canvas.size[0]-1+1, 0, 1, canvas.size[1])
walls.add(wall)
wall = Rectangle(1, 0-1, canvas.size[0]-2, 1)
walls.add(wall)
wall = Rectangle(1, canvas.size[1]-1+1, canvas.size[0]-2, 1)
walls.add(wall)

pacman = Rectangle(canvas.size[0]/2+x_offset, canvas.size[1]/2+y_offset, w, h) # creates a "pacman" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
# if one wants to position pac-man randomly, then one could use a WHILE loop as done for ghosts
pacman.image.blit(pacman_picture, (0, 0))
pacmen.add(pacman)

# for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "pellet" sprites
while 50-len(pellets) > 0: # create and add fifty "pellet" sprites
    x = random.randrange(0, canvas.size[0]+1-w/2, w/2) # position "pellet" sprite, allow it to touch edge but not breach it
    y = random.randrange(0, canvas.size[1]+1-h/2, h/2) #  want "pellet" sprites equally spaced, also mitigates overlap
    pellet = Rectangle(x, y, w/2, h/2) # create a "pellet" sprite
    pellet.image.blit(pellet_picture, (0, 0))
    pygame.sprite.spritecollide(pellet, pellets, True) # remove any "pellet" sprite in list in same position, essentially preventing "pellet" sprites from taking same position and essentially preventing overlap, you cannot check if sprite is in group or belongs to group since each sprite is unique
    pellets.add(pellet) # add "pellet" sprite to list, no longer append
    for wall in walls:
        pygame.sprite.spritecollide(wall, pellets, True) # remove any "pellet" sprite in list in same position

for i in range(0, retries):
    retry_boxes.append(pacman_picture_retry)

while True: # put first, else when try to get second (green) ghost moving it will move prematurely
    x = random.randrange(0, canvas.size[0]+1-w)
    y = random.randrange(0, canvas.size[1]+1-h)
    ghost = Rectangle(x, y, w, h)
    ghost.image.blit(green_ghost_picture, (0, 0))
    green_ghosts.add(ghost)
    stuck = pygame.sprite.spritecollide(ghost, walls, False)
    if stuck != []:
        green_ghosts.remove(ghost)
    else:
        break

while True:
    x = random.randrange(0, canvas.size[0]+1-w)
    y = random.randrange(0, canvas.size[1]+1-h)
    ghost = Rectangle(x, y, w, h)
    ghost.image.blit(red_ghost_picture, (0, 0))
    red_ghosts.add(ghost)
    stuck = pygame.sprite.spritecollide(ghost, walls, False)
    if stuck != []:
        red_ghosts.remove(ghost)
    else:
        break # exit loop, not quitting game

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT:
            canvas.close()
        elif action.type == pygame.USEREVENT:
            if timer == 0 or len(pacmen) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # stop timer
                game_over_sound.play()
            elif len(pellets) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else: # after one second
                timer -= 1 # decrement timer
                if timer % 10 == 0:
                    y_increment_green_ghost = random.choice([-1, 0, 1]) # let Python choose direction and speed
                    if y_increment_green_ghost == 0:
                        x_increment_green_ghost = random.choice([-1, 1])
                    else:
                        x_increment_green_ghost = 0
                    # green_ghost.image = pygame.transform.flip(green_ghost.image, True, False)
                    # green_ghost.image.set_colorkey(BLACK)
                elif timer % 5 == 0:
                    x_increment_red_ghost = random.choice([-1, 0, 1]) # let Python choose direction and speed
                    if x_increment_red_ghost == 0:
                        y_increment_red_ghost = random.choice([-1, 1])
                    else:
                        y_increment_red_ghost = 0
                    # red_ghost.image = pygame.transform.flip(red_ghost.image, True, False)
                    # red_ghost.image.set_colorkey(BLACK)                    
                    # y_increment_red_ghost = random.randint(-1, 1) # let Python choose direction and speed
                    # if y_increment_red_ghost == 0:
                    #     x_increment_red_ghost = random.choice([-1, 1]) # always moving
                    # x_increment_green_ghost = random.randint(-1, 1)
                    # if x_increment_green_ghost == 0:
                    #     y_increment_green_ghost = random.choice([-1, 1])

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
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                elif action.key == pygame.K_UP:
                    y_increment = -5
                    angle = 90
                    pacman.turn(angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                    pacman.turn(angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
                elif action.key == pygame.K_DOWN:
                    y_increment = 5 # note "y_increment," and recall that y increases going downward
                    angle = 270
                    pacman.turn(angle)
                    count += 1
                    if count % 15 == 0:
                        pacman_walk_sound.play()
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

    # if canvas.size[0]/2+x_offset < 0:
    #     x_offset = -canvas.size[0]/2 # prevent "pacman" and "ghost" sprites from breaching left edge, solved for x_offset
    # elif canvas.size[0]/2+x_offset + w > canvas.size[0]:
    #     x_offset = canvas.size[0]/2 - w # simplified
    # if canvas.size[1]/2+y_offset < 0: # note "if"
    #     y_offset = -canvas.size[1]/2 # prevent "pacman" and "ghost" sprites from breaching top edge, solved for y_offset
    # elif canvas.size[1]/2+y_offset + h > canvas.size[1]:
    #     y_offset = canvas.size[1]/2 - h # simplified

    # pacman.rect.x = canvas.size[0]/2+x_offset # position and offset "pacman" sprite <- do earlier
    # permits faster moving pac-man, could use technique for red ghost too
    for i in range(0, abs(x_increment)+1): # increment x-coordinate *abs(x_increment)* many times
        if x_increment == 0:
            pass # don't increment x-coordinate
        else:
            pacman.rect.x += x_increment/abs(x_increment) # bypass offset for new positions, always += -1 or += 1 depending on direction of movement
        wall_pacman_hit_x = pygame.sprite.spritecollide(pacman, walls, False) # DON'T remove a "wall" sprite, if "pacman" sprite hits it, returns a list
        # instead...
        if wall_pacman_hit_x != []: # align, then break out of above loop
            for wall in wall_pacman_hit_x: # wall that pacman hit
                if x_increment > 0: # moving rightward
                    pacman.rect.right = wall.rect.left
                else: # moving leftward, x_increment = 0 not hitting wall
                    pacman.rect.left = wall.rect.right # reverse
            break # no sense in completing above loop, if hit wall
    
    # pacman.rect.y = canvas.size[1]/2+y_offset <- do earlier
    # takes care of if pacman appears on wall
    # again, permits faster moving pac-man, could use technique for green ghost too
    for j in range(0, abs(y_increment)+1): # increment y-coordinate *abs(y_increment)* many times
        if y_increment == 0:
            pass # don't increment y-coordinate
        else:
            pacman.rect.y += y_increment/abs(y_increment) # must put here or else goes around wall, again bypass offset for new positions, always += -1 or += 1 depending on direction of movement
        wall_pacman_hit_y = pygame.sprite.spritecollide(pacman, walls, False) # again, DON'T remove a "wall" sprite, if "pacman" sprite hits it, returns a list
        # instead...
        if wall_pacman_hit_y != []: # align, then break out of above loop
            for wall in wall_pacman_hit_y: # wall that pacman hit
                if y_increment > 0: # moving rightward
                    pacman.rect.bottom = wall.rect.top
                else: # moving leftward, y_increment = 0 not hitting wall
                    pacman.rect.top = wall.rect.bottom  # reverse
            break # no sense in completing above loop, if hit wall

    # if timer % 10 == 0:
    for ghost in red_ghosts:
        wall_ghost_hit_x = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_x != []:
            x_increment_red_ghost *= -1
        ghost.rect.x += x_increment_red_ghost # move "ghost" sprites rightward

        wall_ghost_hit_y = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_y != []:
            y_increment_red_ghost *= -1
        ghost.rect.y += y_increment_red_ghost # move "ghost" sprites downward

    for ghost in green_ghosts:
        wall_ghost_hit_x = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_x != []:
            x_increment_green_ghost *= -1
        ghost.rect.x += x_increment_green_ghost

        wall_ghost_hit_y = pygame.sprite.spritecollide(ghost, walls, False)
        if wall_ghost_hit_y != []:
            y_increment_green_ghost *= -1
        ghost.rect.y += y_increment_green_ghost

    # theoretically, ghosts could still get stuck, but it would be extremely unusual

    # red_ghost.rect.x = canvas.size[0]/2+x_offset
    # green_ghost.rect.y = canvas.size[1]/2+y_offset
    # pygame.sprite.spritecollide(pacman, ghosts, True) # remove a "ghost" sprite, if "pacman" sprite collides with it
    pellet_removed = pygame.sprite.spritecollide(pacman, pellets, True) # remove a "pellet" sprite, if "pacman" sprite collides with it
    # collisions.add(removed)
    if pellet_removed != []: # or "for pellet in removed:"
        score += 1
    # if timer != 0:
        # score = len(collisions)
    if timer != 0 and len(pacmen) != 0 and len(pellets) != 0:
        pass
    else: # stops ghosts from moving when game over or win game
        x_increment_green_ghost = 0
        y_increment_green_ghost = 0
        x_increment_red_ghost = 0
        y_increment_red_ghost = 0
    for ghost in red_ghosts:
        pacman_removed = pygame.sprite.spritecollide(ghost, pacmen, True) # pac-man can bypass ghost for insane speeds
        if pacman_removed != []:
            ghost_hit_sound.play()
        if pacman_removed != [] and retries > 0:
            pacmen.add(pacman_removed)
            pacman.retry()
            retries -= 1
            retry_boxes.pop()
    for ghost in green_ghosts:
        pacman_removed = pygame.sprite.spritecollide(ghost, pacmen, True) # pac-man can bypass ghost for insane speeds
        if pacman_removed != []:
            ghost_hit_sound.play()
        if pacman_removed != [] and retries > 0:
            pacmen.add(pacman_removed)
            pacman.retry()
            retries -= 1
            retry_boxes.pop()
    for ghost in red_ghosts: # put down here, since there are two ways increment changes sign: choice() and collisions
        if x_increment_red_ghost < 0 or y_increment_red_ghost < 0:
            ghost.flip(True) # tell flip() which ghost it is
        else:
            ghost.flip(False)
    for ghost in green_ghosts:
        if x_increment_green_ghost < 0 or y_increment_green_ghost < 0:
            ghost.flip(True)
        else:
            ghost.flip(False)
    # --------------
    canvas.screen.fill(BLUE) # clear the display
    timer_header = style_header.render("Time Left", False, RED)
    timer_text = style.render(str(timer), False, RED) # ("time remaining", anti-aliased, COLOR)
    score_header = style_header.render("Score", False, GREEN)
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, BLACK)
    you_win_text = style.render(None, False, GREEN)
    if timer == 0 or len(pacmen) == 0:
        # pacman.image.fill(WHITE)
        pygame.draw.rect(pacman.image, WHITE, (0, 0, w, h), width=0)
        for pellet in pellets:
            pygame.draw.rect(pellet.image, LIGHTGRAY, (0, 0, w/2, h/2), width=0)
        for wall in walls:
            wall.image.fill(DARKGRAY)
        for ghost in red_ghosts:
            pygame.draw.rect(ghost.image, DARKGRAY, (0, 0, w, h), width = 0)
        for ghost in green_ghosts:
            pygame.draw.rect(ghost.image, DARKGRAY, (0, 0, w, h), width = 0)
        canvas.screen.fill(GRAY)
        timer_header = style_header.render("Time Left", False, DARKGRAY)
        timer_text = style.render(str(timer), False, DARKGRAY)
        score_header = style_header.render("Score", False, DARKGRAY)
        score_text = style.render(str(score), False, DARKGRAY)
        game_over_text = style.render("Game Over", False, BLACK)
    if len(pellets) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    # --- Drawing code
    walls.draw(canvas.screen) # draw sprites on screen using list
    pellets.draw(canvas.screen)
    # canvas.screen.blit(red_ghost.image, (red_ghost.rect.x, red_ghost.rect.y))
    # canvas.screen.blit(green_ghost.image, (green_ghost.rect.x, green_ghost.rect.y))
    red_ghosts.draw(canvas.screen) # previous code override what we want
    green_ghosts.draw(canvas.screen) # previous code override what we want
    canvas.screen.blit(pacman.image, (pacman.rect.x, pacman.rect.y)) # draw sprite on screen, so you can see block
    canvas.screen.blit(timer_header, (10, 10))
    canvas.screen.blit(timer_text, (10, 30)) # copy image of text onto screen at (10, 10)
    for i in range(0, retries):
        canvas.screen.blit(retry_boxes[i], (100+i*w/2, 10))
        retry_boxes[i].set_colorkey(BLACK) # not passed through class definition
        if timer == 0:
            pygame.draw.rect(retry_boxes[i], WHITE, [0, 0, w/2, h/2], 0)
    canvas.screen.blit(score_header, (canvas.size[0]-score_header.get_width()-10, 10))
    canvas.screen.blit(score_text, (canvas.size[0]-score_text.get_width()-10, 30)) # near top-right corner
    canvas.screen.blit(game_over_text, game_over_text.get_rect(center = canvas.screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument (recall: positional args vs keyword args)
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    canvas.screen.blit(you_win_text, you_win_text.get_rect(center = canvas.screen.get_rect().center))
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
    if pygame.time.get_ticks() - ticks > 10000: # unless user stops playing for more than 10 seconds
        # pygame.time.set_timer(pygame.USEREVENT, 0)
        clock.tick(1) # in which case minimize the frame rate
    # if pygame.time.set_timer(pygame.USEREVENT, 0) == True:
        # print("true") # and pygame.time.get_ticks() - ticks <= 10000:
        # pygame.time.set_timer(pygame.USEREVENT, 1000)