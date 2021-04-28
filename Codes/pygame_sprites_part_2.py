import pygame # import the pygame module
import sys # import the sys module
#### import random # import the random module

pygame.init() # initialize any submodules that require it

BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
#### YELLOW = pygame.Color("yellow")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
y_increment = 0
#### block_list = pygame.sprite.Group() # no longer block_list = []
sprites = pygame.sprite.Group() # create a list for sprites, no longer sprites = []
#### score = 0 # initialize score

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional

# --- Functions/Classes
# def draw_rect(display, x, y, W, H):
#     # Draw a rectangle
#     pygame.draw.rect(display, WHITE, (x, y, W, H), width=0)
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish it from a function
    def __init__(self, COLOR, W, H): # define a constructor (like init() but for classes), class accepts COLOR, width, and height parameters, "__" before and after "init" is a must, requires "self" (like a key to access class)
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (W, H) # define size of image, local variable
        self.image = pygame.Surface(size) # makes a blank image using Surface class
        #### # self.image.fill(WHITE) # background of foreground image
        #### # self.image.set_colorkey(WHITE) # makes background color transparent
        pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # draw on image, draw over entire image with (0, 0, W, H)
        self.rect = self.image.get_rect() # pair image with rectangle object, so we can give the image a position
# ---------------------

#### for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    #### block = Block(YELLOW, 20, 20) # creates a block
    #### block.rect.x = random.randrange(0, size[0]-20) # position of block image
    #### block.rect.y = random.randrange(0, size[1]-20)
    #### block_list.add(block) # no longer append
    #### sprites.add(block)

player = Rectangle(WHITE, 64, 64) # creates a "player" sprite, which will be your sprite to play with, don't need screen, will instead use it in drawing code, calling class, sans offsets
sprites.add(player)

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if action.key == pygame.K_RIGHT: # note "action.key"
                x_increment = 5 # "5" is optional
            elif action.key == pygame.K_LEFT:
                x_increment = -5
            elif action.key == pygame.K_DOWN:
                y_increment = 5 # note "y_increment," and recall that y increases going downward
            elif action.key == pygame.K_UP:
                y_increment = -5
        elif action.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
        # -------------------------
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    player.rect.x = size[0]/2+x_offset # position and offset "player" sprite/image
    player.rect.y = size[1]/2+y_offset
    #### if player.rect.x < 0:
        #### player.rect.x = 0 # prevent center point from passing left edge
    #### elif player.rect.x > size[0] - 64: # player block is larger
        #### player.rect.x = size[0] - 64
    #### if player.rect.y < 0:
        #### player.rect.y = 0 # prevent center point from passing top edge
    #### elif player.rect.y > size[1] - 64:
        #### player.rect.y = size[1] - 64
    #### blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True) # list block(s) the player block overlaps, then remove block(s) from block_list and sprites
    #### for block in blocks_hit_list: # FOR each block in the list
        #### score +=1 # increment score, resets each time
        #### print(score) # and print score to console
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # draw_rect(screen, size[0]/2+x_offset, size[1]/2+y_offset, 64, 64) # call function, input parameters, and rely on keyboard
    sprites.draw(screen) # draw sprites on screen
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
