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

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
# y_offset = 0
x_increment = 0
# y_increment = 0
blocks = pygame.sprite.Group() # create a list for "block" sprites, no longer blocks = [], Group() is class
collisions = pygame.sprite.Group()
lasers = pygame.sprite.Group()
timer = 10 # set timer for 10 seconds
score = 0 # initialize score

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, COLOR, W, H): # define a constructor, class accepts COLOR, width, and height parameters, must type "__" before and after "init," requires "self"
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (W, H) # define size of image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # draw shape on image, draw over entire image with (0, 0, W, H), where (0, 0) is located at image's top-left corner
        self.rect = self.image.get_rect() # pair image with rectangle object, where (rect.x, rect.y) is located at rectangle object's top-left corner
        # sprite consists of image and rectangle object
    def update(self, px): # you cannot simply name another function/method
        self.rect.y += px # increase sprites' rect.y by px pixels
# ---------------------

player = Rectangle(WHITE, 64, 64) # creates a "player" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "block" sprites
    block = Rectangle(YELLOW, 32, 32) # create a "block" sprite
    block.rect.x = random.randrange(0, size[0]+1-32) # position "block" sprite, allow block to touch edge but not breach it
    block.rect.y = random.randrange(0, size[1]+1-32-100) # want lots of blocks, but if we use a larger step_size, many blocks may overlap, "-100" leaves space at bottom of canvas
    blocks.add(block) # add "block" sprite to list, no longer append

# we will create "laser" sprites later
first = True # but only first one

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        elif action.type == pygame.USEREVENT:
            timer -= 1 # decrement timer
            if timer % 5 == 0: # every 5 seconds
                blocks.update(32) # move "block" sprites downward
            if timer == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # stop timer, "block" sprites stop moving too
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                elif action.key == pygame.K_SPACE: # fire laser
                    laser = Rectangle(CYAN, 5, 20) # create "laser" sprite 
                    laser.rect.centerx = player.rect.centerx # align it with "player" sprite's horizontal center 
                    laser.rect.bottom = player.rect.top + 10 # align its bottom with "player" sprite's top, "+ 10" because update() is called before "laser" sprites are drawn
                    if first == True:
                        lasers.add(laser)
                        first = False
        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                x_increment = 0
            elif action.key == pygame.K_SPACE:
                first = True
        # -------------------------
    # --- Game logic
    x_offset += x_increment
    if size[0]/2+x_offset < 0:
        x_offset = -size[0]/2 # prevent "player" sprite from breaching left edge, solved for x_offset
    elif size[0]/2+x_offset + 64 > size[0]:
        x_offset = size[0]/2 - 64 # simplified
    player.rect.x = size[0]/2+x_offset # position and offset "player" sprite
    player.rect.y = size[1]-64
    # removed = pygame.sprite.spritecollide(player, blocks, True) # remove a "block" sprite, if "player" sprite collides with it
    for laser in lasers: # "laser" sprite was not created before WHILE loop, for any laser in lasers
        removed = pygame.sprite.spritecollide(laser, blocks, True) # remove a "block" sprite, if "laser" sprite collides with it
        collisions.add(removed)
        if removed:
            lasers.remove(laser) # remove "laser" sprite, too
        if laser.rect.y < -20:
            lasers.remove(laser) # otherwise, remove "laser" sprite if it exits screen
    if timer != 0:
        score = len(collisions)
        lasers.update(-10)
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    screen.blit(player.image, (player.rect.x, player.rect.y)) # draw sprite on screen
    blocks.draw(screen) # draw sprites on screen using list
    lasers.draw(screen)
    style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
    text_timer = style.render(str(timer), True, RED) # ("time remaining", anti-aliased, COLOR)
    text_score = style.render(str(score), True, GREEN)
    screen.blit(text_timer, (10, 10)) # copy image of text onto screen at (10, 10)
    screen.blit(text_score, (size[0]-85, 10)) # near top-right corner
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
