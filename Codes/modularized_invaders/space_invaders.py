import pygame, random # import the pygame and random module
import src.canvas as canvas

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
BLACK = pygame.Color("black") # useful if run module on macOS
YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
CYAN = pygame.Color("cyan")
LIGHTGRAY = pygame.Color("light gray")
GRAY = pygame.Color("gray")
DARKGRAY = pygame.Color("dark gray")

clock = pygame.time.Clock() # define "clock"
# x_offset = 0 # reordered
# y_offset = 0
x_increment = 0
# y_increment = 0
w = 64 # "spaceship" sprite width reference
x_offset = -w/2
h = 64 # "spaceship" sprite height reference
invaders = pygame.sprite.Group() # create a list for "invader" sprites, no longer invaders = [], Group() is class
# collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
barriers = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
spaceships = pygame.sprite.Group()
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

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, x, y, w, h): # define a constructor, class accepts width, height, x-coordinate, and y-coordinate parameters, must type "__" before and after "init," requires "self"
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
    def update(self, px): # you cannot simply name another function/method
        self.rect.y += px # increase sprites' rect.y by px pixels
    def lunge(self): # calling with sprite, not group
        if count % 2 == 0: # could also have used timer, using count because did same in pac-man
            self.image.blit(invader_picture_alt, (0, 0))
        else:
            self.image.blit(invader_picture, (0, 0))
    def retry(self):
        self.rect.x = canvas.size[0]/2+x_offset # center along bottom of display, bypassed offset
        self.rect.y = canvas.size[1]-h
    def return_fire(self, index):
        # index = 0 # example, more randomized with random.randrange(0, len(invaders))
        self.rect.centerx = invaders.sprites()[index].rect.centerx # align its horizontal center with "invader" sprite's horizontal center
        self.rect.top = invaders.sprites()[index].rect.bottom # align its bottom with "invader" sprite's bottom
        # self.image = pygame.Surface((10, 20)) # can't do, if want interactions
        self.image.fill(RED)
        lasers_alt.add(self)
        invader_laser_sound.play()
# ---------------------

# outer walls (only left and right):
wall = Rectangle(0-1, 0, 1, canvas.size[1]) # need at least some thickness, moved walls outside display
# wall.image.fill(pygame.Color(1, 1, 1)) # windows
walls.add(wall)
wall = Rectangle(canvas.size[0]-1+1, 0, 1, canvas.size[1])
# wall.image.fill(pygame.Color(1, 1, 1)) # windows
walls.add(wall)
# no inner walls

# barriers (left and right)
for i in range(0, p):
    # barrier = Rectangle(50, 400, 250, 25)
    barrier = Rectangle(50+i*250/p, 400, 250/p, 25)
    barrier.image.fill(WHITE)
    barriers.add(barrier)

for i in range(0, p):
    # barrier = Rectangle(canvas.size[0]-250-50, 400, 250, 25)
    barrier = Rectangle(canvas.size[0]-250-50+i*250/p, 400, 250/p, 25)
    barrier.image.fill(WHITE)
    barriers.add(barrier)

x = canvas.size[0]/2+x_offset # position and offset "spaceship" sprite
y = canvas.size[1]-h
spaceship = Rectangle(x, y, w, h) # creates a "spaceship" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
# ALIGN WITH PAC-MAN!!!
# if one wants to position spaceship randomly, then one could use a WHILE loop as done for pac-man ghosts
spaceship.image.blit(spaceship_picture, (0, 0))
spaceships.add(spaceship)

for i in range(0, retries):
    retry_boxes.append(spaceship_picture_retry)

# for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "invader" sprites
while 50-len(invaders) > 0: # create and add fifty "invader" sprites
    x = random.randrange(0, canvas.size[0]+1-w/2, w/2) # position "invader" sprite, allow it to touch edge but not breach it
    y = random.randrange(0, canvas.size[1]+1-h/2-196, h/2) # "-96" leaves space at bottom of canvas and want "invader" sprites equally spaced, also mitigates overlap
    invader = Rectangle(x, y, w/2, h/2) # create a "invader" sprite
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
                    invader.lunge()
                count += 1
                if timer % 4 == 0 and len(invaders) > 0: # some number not multiple of 5
                    laser = Rectangle(int(), int(), 10, 20) # create "laser" sprite
                    laser.return_fire(0)                
                if timer % 7 == 0 and len(invaders) > 1: # some number not multiple of 5
                    laser = Rectangle(int(), int(), 10, 20) # create "laser" sprite
                    laser.return_fire(1)
                if timer % 11 == 0 and len(invaders) > 2: # some number not multiple of 5
                    laser = Rectangle(int(), int(), 10, 20) # create "laser" sprite
                    laser.return_fire(2)
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0 and len(invaders) != 0 and len(spaceships) != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                elif action.key == pygame.K_SPACE: # fire laser
                    laser = Rectangle(int(), int(), 10, 20) # create "laser" sprite
                    laser.image.fill(CYAN)
                    laser.rect.centerx = spaceship.rect.centerx # align it with "spaceship" sprite's horizontal center
                    laser.rect.bottom = spaceship.rect.top + 10 # align its bottom with "spaceship" sprite's top, "+ 10" because update() is called before "laser" sprites are drawn (could probably have also drawn spaceship after lasers)
                    if first == True:
                        lasers.add(laser)
                        spaceship_laser_sound.play()
                        first = False
            else: # without "else," do nothing
                x_increment = 0
        elif action.type == pygame.KEYUP:
            ticks = pygame.time.get_ticks()
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                x_increment = 0
            if action.key == pygame.K_SPACE:
                first = True
        # -------------------------
    # --- Game logic
    # x_offset += x_increment

    # if canvas.size[0]/2+x_offset < 0:
    #     x_offset = -canvas.size[0]/2 # prevent "spaceship" sprite from breaching left edge, solved for x_offset
    # elif canvas.size[0]/2+x_offset + w > canvas.size[0]:
    #     x_offset = canvas.size[0]/2 - w # simplified

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

    # spaceship.rect.y = canvas.size[1]-h <- do earlier

    # removed = pygame.sprite.spritecollide(spaceship, invaders, True) # remove a "invader" sprite, if "spaceship" sprite collides with it
    for laser in lasers: # "laser" sprite was not created before WHILE loop, for any laser in lasers
        invader_removed = pygame.sprite.spritecollide(laser, invaders, True) # remove a "invader" sprite, if "laser" sprite collides with it
        # collisions.add(removed)
        if invader_removed != []: # or "for invader in removed:"
            lasers.remove(laser) # remove "laser" sprite, too
            score += 1
            invader_explosion_sound.play()
        elif laser.rect.bottom < 0:
            lasers.remove(laser) # otherwise, remove "laser" sprite if it exits screen
    for invader in invaders:
        # touched = pygame.sprite.spritecollide(invader, spaceships, True)
        # spaceships.remove(touched)
        spaceship_removed = pygame.sprite.spritecollide(invader, spaceships, True) # similar to pac-man ghosts
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed and retries > 0:
            spaceships.add(spaceship_removed) # will reposition the spaceship
            spaceship.retry()
            retries -= 1
    for laser in lasers_alt:
        spaceship_removed = pygame.sprite.spritecollide(laser, spaceships, True)
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed) # repositioning the spaceship
            spaceship.retry()
            lasers_alt.remove(laser)
            retries -= 1
            retry_boxes.pop()
        elif laser.rect.top > canvas.size[1]:
            lasers_alt.remove(laser)
    if timer != 0 and len(spaceships) != 0 and len(invaders) != 0:
        # score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2)
    # if len(spaceships) == 0 or len(invaders) == 0:
    else: # stops lasers from moving when game over or win game
        lasers.update(0)
        lasers_alt.update(0)

    for laser in lasers_alt:
        barrier_removed = pygame.sprite.spritecollide(laser, barriers, True)
        if barrier_removed != []:
            lasers_alt.remove(laser)

    # for laser in lasers:
    #     barrier_removed = pygame.sprite.spritecollide(laser, barriers, True)
    #     if barrier_removed != []:
    #         lasers.remove(laser)
    # --------------
    canvas.screen.fill(BLUE) # clear the display
    timer_header = style_header.render("Time Left", False, RED)
    timer_text = style.render(str(timer), False, RED) # ("time remaining", anti-aliased, COLOR)
    score_header = style_header.render("Score", False, GREEN)
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, pygame.Color("black"))
    you_win_text = style.render(None, False, GREEN)
    if timer == 0 or len(spaceships) == 0:
        # spaceship.image.fill(WHITE)
        pygame.draw.rect(spaceship.image, WHITE, (0, 0, w, h), width=0)
        for invader in invaders:
            pygame.draw.rect(invader.image, DARKGRAY, (0, 0, w/2, h/2), width=0)
        for laser in lasers:
            laser.image.fill(LIGHTGRAY)
        for laser in lasers_alt:
            laser.image.fill(DARKGRAY)
        canvas.screen.fill(GRAY)
        timer_header = style_header.render("Time Left", False, DARKGRAY)
        timer_text = style.render(str(timer), False, DARKGRAY)
        score_header = style_header.render("Score", False, DARKGRAY)
        score_text = style.render(str(score), False, DARKGRAY)
        game_over_text = style.render("Game Over", False, pygame.Color("black"))
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    # --- Drawing code
    walls.draw(canvas.screen) # draw sprites on screen using list
    barriers.draw(canvas.screen)
    invaders.draw(canvas.screen)
    lasers_alt.draw(canvas.screen)
    canvas.screen.blit(spaceship.image, (spaceship.rect.x, spaceship.rect.y)) # draw sprite on screen, so you can see block
    lasers.draw(canvas.screen)
    canvas.screen.blit(timer_header, (10, 10))
    canvas.screen.blit(timer_text, (10, 30)) # copy image of text onto screen at (10, 10)
    for i in range(0, retries):
        canvas.screen.blit(retry_boxes[i], (100+i*w/2, 10))
        retry_boxes[i].set_colorkey(BLACK)
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
        clock.tick(1) # in which case minimize the frame rate
