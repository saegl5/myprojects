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
W = 64 # "player" sprite width reference
H = 64 # "player" sprite height reference
blocks = pygame.sprite.Group() # create a list for "block" sprites, no longer blocks = [], Group() is class
collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
players = pygame.sprite.Group()
timer = 30 # set timer for 30 seconds
score = 0 # initialize score
style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
count = 0 # for lunging picture
ticks = int() # for saving energy
game_over_sound = pygame.mixer.Sound('Sounds/game_over.ogg') # Source: https://kenney.nl/assets/voiceover-pack
you_win_sound = pygame.mixer.Sound('Sounds/you_win.ogg') # Source: https://kenney.nl/assets/voiceover-pack
player_image = pygame.image.load('Images/ship.png').convert() # Edited from source: https://opengameart.org/content/pixel-space-invaders (changed black to (1, 1, 1), too)
player_image = pygame.transform.scale(player_image, (W, H))
# player_image.set_colorkey(BLACK)
block_image = pygame.image.load('Images/alien.png').convert() # Edited from source: https://opengameart.org/content/alien-sprite-sheet (changed black to (1, 1, 1), too)
# block_image.set_colorkey(BLACK)
block_image_alt = pygame.image.load('Images/alien_lunging.png').convert() # my image from alien.png
# block_image_alt.set_colorkey(BLACK)

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
        # self.image.blit(sprite_image, (0, 0))
        # self.image.set_colorkey(BLACK) # windows only
        self.rect = self.image.get_rect() # pair image with rectangle object, where (rect.x, rect.y) is located at rectangle object's top-left corner
        # sprite consists of image and rectangle object
        self.rect.x = x
        self.rect.y = y
    def update(self, px): # you cannot simply name another function/method
        self.rect.y += px # increase sprites' rect.y by px pixels
    def lunge(self): # calling with sprite, not group
        if count % 2 == 0: # could also have used timer, using count because did same in pac-man
            self.image.blit(block_image_alt, (0, 0))
        else:
            self.image.blit(block_image, (0, 0))
# ---------------------

# outer walls (only left and right):
wall = Rectangle(0-1, 0, 1, size[1]) # need at least some thickness, moved walls outside display
walls.add(wall)
wall = Rectangle(size[0]-1+1, 0, 1, size[1])
walls.add(wall)
# no inner walls

player = Rectangle(int(), int(), W, H) # creates a "player" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition
player.image.blit(player_image, (0, 0))
player.rect.x = size[0]/2+x_offset # position and offset "player" sprite
player.rect.y = size[1]-H
players.add(player)

# for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "block" sprites
while 50-len(blocks) > 0: # create and add fifty "block" sprites
    x = random.randrange(0, size[0]+1-W/2, W/2) # position "block" sprite, allow it to touch edge but not breach it
    y = random.randrange(0, size[1]+1-H/2-96, H/2) # "-96" leaves space at bottom of canvas and want "block" sprites equally spaced, also mitigates overlap
    block = Rectangle(x, y, W/2, H/2) # create a "block" sprite
    block.image.blit(block_image, (0, 0))
    pygame.sprite.spritecollide(block, blocks, True) # remove any "block" sprite in same position, essentially preventing "block" sprites from taking same position and essentially preventing overlap, you cannot check if sprite is in group or belongs to group since each sprite is unique
    blocks.add(block) # add "block" sprite to list, no longer append

# we will create "laser" sprites later
first = True # but only first one

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        elif action.type == pygame.USEREVENT:
            if timer == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # stop timer, "block" sprites stop moving too
                game_over_sound.play()
            elif len(blocks) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            elif len(players) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                game_over_sound.play()
            else: # after one second
                timer -= 1 # decrement timer
                if timer % 5 == 0: # every 5 seconds
                    blocks.update(32) # move "block" sprites downward
                for block in blocks:
                    block.lunge()
                count += 1
                if (timer % 7 == 0) or (timer % 8 == 0): # some number not multiple of 5
                    laser = Rectangle(int(), int(), 6, 10) # create "laser" sprite
                    laser.image.fill(RED)
                    index = random.randrange(0, len(blocks))
                    laser.rect.centerx = blocks.sprites()[index].rect.centerx # align it with "player" sprite's horizontal center
                    laser.rect.bottom = blocks.sprites()[index].rect.bottom # align its bottom with "player" sprite's top, "+ 10" because update() is called before "laser" sprites are drawn
                    lasers_alt.add(laser)
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0 and len(blocks) != 0 and len(players) != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                elif action.key == pygame.K_SPACE: # fire laser
                    laser = Rectangle(int(), int(), 4, 20) # create "laser" sprite
                    laser.image.fill(CYAN)
                    laser.rect.centerx = player.rect.centerx # align it with "player" sprite's horizontal center
                    laser.rect.bottom = player.rect.top + 10 # align its bottom with "player" sprite's top, "+ 10" because update() is called before "laser" sprites are drawn
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
    player.rect.x += x_increment # offset directly

    hit = pygame.sprite.spritecollide(player, walls, False) # DON'T remove a "wall" sprite, if "player" sprite hits it, returns a list
    # instead...
    for wall in hit: # wall that player hit
        if x_increment > 0: # moving rightward
            player.rect.right = wall.rect.left
        else: # moving leftward, x_increment = 0 not hitting wall
            player.rect.left = wall.rect.right # reverse

    # if size[0]/2+x_offset < 0:
    #     x_offset = -size[0]/2 # prevent "player" sprite from breaching left edge, solved for x_offset
    # elif size[0]/2+x_offset + W > size[0]:
    #     x_offset = size[0]/2 - W # simplified
    # player.rect.x = size[0]/2+x_offset # position and offset "player" sprite <- do earlier
    # player.rect.y = size[1]-H <- do earlier
    # removed = pygame.sprite.spritecollide(player, blocks, True) # remove a "block" sprite, if "player" sprite collides with it
    for laser in lasers: # "laser" sprite was not created before WHILE loop, for any laser in lasers
        removed = pygame.sprite.spritecollide(laser, blocks, True) # remove a "block" sprite, if "laser" sprite collides with it
        collisions.add(removed)
        if removed:
            lasers.remove(laser) # remove "laser" sprite, too
        elif laser.rect.y < -20:
            lasers.remove(laser) # otherwise, remove "laser" sprite if it exits screen
    for block in blocks:
        # touched = pygame.sprite.spritecollide(block, players, True)
        # players.remove(touched)
        pygame.sprite.spritecollide(block, players, True)
    if timer != 0:
        score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2)
    # --------------
    screen.fill(BLUE) # clear the display
    timer_text = style.render(str(timer), True, RED) # ("time remaining", anti-aliased, COLOR)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, pygame.Color("black"))
    you_win_text = style.render(None, True, GREEN)
    if timer == 0 or len(players) == 0:
        player.image.fill(WHITE)
        for block in blocks:
            pygame.draw.rect(block.image, LIGHTGRAY, (0, 0, W/2, H/2), width=0)
        for laser in lasers:
            pygame.draw.rect(laser.image, LIGHTGRAY, (0, 0, W/2, H/2), width=0)
        screen.fill(GRAY)
        timer_text = style.render(str(timer), True, DARKGRAY)
        score_text = style.render(str(score), True, DARKGRAY)
        game_over_text = style.render("Game Over", True, pygame.Color("black"))
    if len(blocks) == 0:
        you_win_text = style.render("WINNER!", True, GREEN)
    # --- Drawing code
    screen.blit(player.image, (player.rect.x, player.rect.y)) # draw sprite on screen
    walls.draw(screen) # draw sprites on screen using list
    blocks.draw(screen)
    lasers.draw(screen)
    lasers_alt.draw(screen)
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
        clock.tick(1) # in which case minimize the frame rate
