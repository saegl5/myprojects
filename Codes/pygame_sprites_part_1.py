import pygame # import modules
import sys
import random

pygame.init() # initialize any submodules that require it
 
BLUE = pygame.Color("blue") # example
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
# no offsets
x_increment = 0
y_increment = 0
block_list = pygame.sprite.Group() # no longer block_list = []
all_sprites_list = pygame.sprite.Group() # no longer all_sprites_list = []
score = 0 # initialize score

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example

# --- Functions/Classes
# def draw_circle(screen, x_offset, y_offset):
#     # Draw a circle
#     pygame.draw.circle(screen, WHITE, (0+x_offset, 0+y_offset), radius=25, width=1)
#     pygame.draw.circle(screen, WHITE, (0+x_offset, 0+y_offset), radius=1, width=1)
class Block(pygame.sprite.Sprite): # make a Block class of same class as Sprites
    def __init__(self, color, width, height): # called a "constructor," Block class accepts color, width, and height parameters for building objects
        super().__init__() # call the parent (Sprite) class constructor to initialize sprites
        self.image = pygame.Surface((width, height)) # foreground image using Surface class (makes a blank image like an embedded canvas), could also be loaded from the disk
        # self.image.fill(WHITE) # background of foreground image
        # self.image.set_colorkey(WHITE) # makes background color transparent
        pygame.draw.rect(self.image, color, (0, 0, width, height), width=0) # foreground of foreground image, no longer put screen, this might be redundant for rectangles
        self.rect = self.image.get_rect() # pair image with rectangle object (like a middle man), so we can give the image a position
# ---------------------

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    block = Block(WHITE, 20, 20) # creates a block
    block.rect.x = random.randrange(0, size[0]-20) # position of block image
    block.rect.y = random.randrange(0, size[1]-20)
    block_list.add(block) # no longer append
    all_sprites_list.add(block)

player = Block(YELLOW, 40, 40) # creates a "player" block
player.rect.x = 0 # initial position of player image
player.rect.y = 0
all_sprites_list.add(player)

while True: # keeps display open
    for event in pygame.event.get(): # check for user input when open display
        if event.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit WHILE loop
        # --- Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # note "event.key"
                x_increment = -7
            elif event.key == pygame.K_RIGHT:
                x_increment = 7
            elif event.key == pygame.K_UP: # recall that y increases going downward
                y_increment = -7 # note "y_increment"
            elif event.key == pygame.K_DOWN:
                y_increment = 7
            else:
                None # continue
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_increment = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_increment = 0
            else:
                None # continue
        else:
            None # continue
    # --- Game logic
    player.rect.x += x_increment # was x_offset
    player.rect.y += y_increment # was y_offset
    if player.rect.x < 0:
        player.rect.x = 0 # prevent center point from passing left edge
    elif player.rect.x > size[0]-40: # player block is larger
        player.rect.x = size[0]-40
    else:
        None # continue
    if player.rect.y < 0:
        player.rect.y = 0 # prevent center point from passing top edge
    elif player.rect.y > size[1]-40:
        player.rect.y = size[1]-40
    else:
        None # continue
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True) # list block(s) the player block overlaps, then remove block(s) from block_list and all_sprites_list
    for block in blocks_hit_list: # FOR each block in the list
        score +=1 # increment score, resets each time
        print(score) # and print score to console
    # --------------
    screen.fill(BLUE) # clear the display
    # --- Drawing code
    # draw_circle(screen, 10, 10) # numbers are offsets
    # draw_circle(screen, x_offset, y_offset) # rely on keyboard
    all_sprites_list.draw(screen) # draw all blocks on screen
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second