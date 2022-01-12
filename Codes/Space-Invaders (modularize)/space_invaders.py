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
CYAN = pygame.Color("cyan")
LIGHTGRAY = pygame.Color("light gray")
GRAY = pygame.Color("gray")
DARKGRAY = pygame.Color("dark gray")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
# y_offset = 0
x_increment = 0
# y_increment = 0
W = 64 # "spaceship" sprite width reference
H = 64 # "spaceship" sprite height reference
invaders = pygame.sprite.Group() # create a list for "invader" sprites, no longer invaders = [], Group() is class
# collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
spaceships = pygame.sprite.Group()
timer = 30 # set timer for 30 seconds (multiple of modulo for invaders.update())
score = 0 # initialize score
style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
count = 0 # for lunging picture
retries = 2
retries_boxes = []
ticks = int() # for saving energy
game_over_sound = pygame.mixer.Sound('Sounds/game_over.ogg') # Source: https://kenney.nl/assets/voiceover-pack
you_win_sound = pygame.mixer.Sound('Sounds/you_win.ogg') # Source: https://kenney.nl/assets/voiceover-pack
spaceship_picture = pygame.image.load('Images/ship.png').convert() # Edited from source: https://opengameart.org/content/pixel-space-invaders (changed black to (1, 1, 1), too)
spaceship_picture = pygame.transform.scale(spaceship_picture, (W, H))
spaceship_picture_retries = pygame.transform.scale(spaceship_picture, (W/2, H/2))
# spaceship_picture.set_colorkey(BLACK)
invader_picture = pygame.image.load('Images/alien.png').convert() # Edited from source: https://opengameart.org/content/alien-sprite-sheet (changed black to (1, 1, 1), too)
# invader_picture.set_colorkey(BLACK)
invader_picture_alt = pygame.image.load('Images/alien_lunging.png').convert() # my picture from alien.png
# invader_picture_alt.set_colorkey(BLACK)

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, x, y, W, H): # define a constructor, class accepts width, height, x-coordinate, and y-coordinate parameters, must type "__" before and after "init," requires "self"
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
    def update(self, px): # you cannot simply name another function/method
        self.rect.y += px # increase sprites' rect.y by px pixels
    def lunge(self): # calling with sprite, not group
        if count % 2 == 0: # could also have used timer, using count because did same in pac-man
            self.image.blit(invader_picture_alt, (0, 0))
        else:
            self.image.blit(invader_picture, (0, 0))
    def retry(self):
        self.rect.x = size[0]/2-W/2 # center along bottom of display, bypassed offset
        self.rect.y = size[1]-H
# ---------------------

# outer walls (only left and right):
wall = Rectangle(0-1, 0, 1, size[1]) # need at least some thickness, moved walls outside display
# wall.image.fill(pygame.Color(1, 1, 1)) # windows
walls.add(wall)
wall = Rectangle(size[0]-1+1, 0, 1, size[1])
# wall.image.fill(pygame.Color(1, 1, 1)) # windows
walls.add(wall)
# no inner walls

x = size[0]/2+x_offset # position and offset "spaceship" sprite
y = size[1]-H
spaceship = Rectangle(x, y, W, H) # creates a "spaceship" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
spaceship.image.blit(spaceship_picture, (0, 0))
spaceships.add(spaceship)

for i in range(0, retries):
    retries_boxes.append(spaceship_picture_retries)

# for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "invader" sprites
while 50-len(invaders) > 0: # create and add fifty "invader" sprites
    x = random.randrange(0, size[0]+1-W/2, W/2) # position "invader" sprite, allow it to touch edge but not breach it
    y = random.randrange(0, size[1]+1-H/2-96, H/2) # "-96" leaves space at bottom of canvas and want "invader" sprites equally spaced, also mitigates overlap
    invader = Rectangle(x, y, W/2, H/2) # create a "invader" sprite
    invader.image.blit(invader_picture, (0, 0))
    pygame.sprite.spritecollide(invader, invaders, True) # remove any "invader" sprite in same position, essentially preventing "invader" sprites from taking same position and essentially preventing overlap, you cannot check if sprite is in group or belongs to group since each sprite is unique
    invaders.add(invader) # add "invader" sprite to list, no longer append

# we will create "laser" sprites later
first = True # but only first one

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
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
                if timer % 7 == 0: # some number not multiple of 5
                    laser = Rectangle(int(), int(), 10, 20) # create "laser" sprite
                    laser.image.fill(RED)
                    index = 0 # example, more randomized with random.randrange(0, len(invaders))
                    laser.rect.centerx = invaders.sprites()[index].rect.centerx # align its horizontal center with "invader" sprite's horizontal center
                    laser.rect.top = invaders.sprites()[index].rect.bottom # align its bottom with "invader" sprite's bottom
                    lasers_alt.add(laser)
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

    # if size[0]/2+x_offset < 0:
    #     x_offset = -size[0]/2 # prevent "spaceship" sprite from breaching left edge, solved for x_offset
    # elif size[0]/2+x_offset + W > size[0]:
    #     x_offset = size[0]/2 - W # simplified

    # spaceship.rect.x = size[0]/2+x_offset # position and offset "spaceship" sprite <- do earlier
    spaceship.rect.x += x_increment # offset directly
    hit = pygame.sprite.spritecollide(spaceship, walls, False) # DON'T remove a "wall" sprite, if "spaceship" sprite hits it, returns a list
    # instead...
    for wall in hit: # wall that spaceship hit
        if x_increment > 0: # moving rightward
            spaceship.rect.right = wall.rect.left
        else: # moving leftward, x_increment = 0 not hitting wall
            spaceship.rect.left = wall.rect.right # reverse

    # spaceship.rect.y = size[1]-H <- do earlier

    # removed = pygame.sprite.spritecollide(spaceship, invaders, True) # remove a "invader" sprite, if "spaceship" sprite collides with it
    for laser in lasers: # "laser" sprite was not created before WHILE loop, for any laser in lasers
        invader_removed = pygame.sprite.spritecollide(laser, invaders, True) # remove a "invader" sprite, if "laser" sprite collides with it
        # collisions.add(removed)
        if len(invader_removed) != 0: # or "for invader in removed:"
            lasers.remove(laser) # remove "laser" sprite, too
            score += 1
        elif laser.rect.bottom < 0:
            lasers.remove(laser) # otherwise, remove "laser" sprite if it exits screen
    for invader in invaders:
        # touched = pygame.sprite.spritecollide(invader, spaceships, True)
        # spaceships.remove(touched)
        pygame.sprite.spritecollide(invader, spaceships, True) # similar to pac-man ghosts
    for laser in lasers_alt:
        spaceship_removed = pygame.sprite.spritecollide(laser, spaceships, True)
        if len(spaceship_removed) != 0 and retries > 0:
            spaceships.add(spaceship_removed) # repositioning the spaceship
            spaceship.retry()
            lasers_alt.remove(laser)
            retries -= 1
            retries_boxes.pop()
        elif laser.rect.top > size[1]:
            lasers_alt.remove(laser)
    if timer != 0 and len(spaceships) != 0 and len(invaders) != 0:
        # score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2)
    # if len(spaceships) == 0 or len(invaders) == 0:
    else:
        lasers.update(0)
        lasers_alt.update(0)
    # --------------
    screen.fill(BLUE) # clear the display
    timer_text = style.render(str(timer), True, RED) # ("time remaining", anti-aliased, COLOR)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, pygame.Color("black"))
    you_win_text = style.render(None, True, GREEN)
    if timer == 0 or len(spaceships) == 0:
        # spaceship.image.fill(WHITE)
        pygame.draw.rect(spaceship.image, WHITE, (0, 0, W, H), width=0)
        for invader in invaders:
            pygame.draw.rect(invader.image, LIGHTGRAY, (0, 0, W/2, H/2), width=0)
        for laser in lasers:
            laser.image.fill(LIGHTGRAY)
        for laser in lasers_alt:
            laser.image.fill(LIGHTGRAY)
        screen.fill(GRAY)
        timer_text = style.render(str(timer), True, DARKGRAY)
        score_text = style.render(str(score), True, DARKGRAY)
        game_over_text = style.render("Game Over", True, pygame.Color("black"))
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", True, GREEN)
    # --- Drawing code
    walls.draw(screen) # draw sprites on screen using list
    invaders.draw(screen)
    lasers_alt.draw(screen)
    screen.blit(spaceship.image, (spaceship.rect.x, spaceship.rect.y)) # draw sprite on screen
    lasers.draw(screen)
    screen.blit(timer_text, (10, 10)) # copy image of text onto screen at (10, 10)
    for i in range(0, retries):
        screen.blit(retries_boxes[i], (100+i*W/2, 10))
        retries_boxes[i].set_colorkey(BLACK)
    screen.blit(score_text, (size[0]-score_text.get_width()-10, 10)) # near top-right corner
    screen.blit(game_over_text, game_over_text.get_rect(center = screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument (recall: positional args vs keyword args)
    # outside in: pair game_over_text with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    screen.blit(you_win_text, you_win_text.get_rect(center = screen.get_rect().center))
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
    if pygame.time.get_ticks() - ticks > 10000: # unless user stops playing for more than 10 seconds
        clock.tick(1) # in which case minimize the frame rate
