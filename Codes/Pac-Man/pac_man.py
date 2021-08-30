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
y_increment = 0
W = 64 # "player" sprite width reference
H = 64 # "player" sprite height reference
blocks = pygame.sprite.Group() # create a list for "block" sprites, no longer blocks = [], Group() is class
collisions = pygame.sprite.Group()
timer = 30 # set timer for 30 seconds
score = 0 # initialize score
style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
count = 0 # for chomp picture
ticks = int() # for saving energy
# angle = 0 # redundant
game_over_sound = pygame.mixer.Sound('Sounds/game_over.ogg') # Source: https://kenney.nl/assets/voiceover-pack
you_win_sound = pygame.mixer.Sound('Sounds/you_win.ogg') # Source: https://kenney.nl/assets/voiceover-pack
player_image = pygame.image.load('Images/pac.png').convert() # Edited from source: https://opengameart.org/content/pacman-tiles
# player_image.set_colorkey(BLACK)
player_image_alt = pygame.image.load('Images/pac_chomp.png').convert() # my image from pac.png
# player_image_alt.set_colorkey(BLUE)
block_image = pygame.image.load('Images/dot.png').convert() # Edited from source: https://opengameart.org/content/pacman-tiles (changed black to (1, 1, 1), too)
block_image = pygame.transform.scale(block_image, (int(W/2), int(H/2))) # int() addresses "TypeError: integer argument expected, got float"
# block_image.set_colorkey(BLACK)

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, sprite_image, W, H): # define a constructor, class accepts COLOR, width, and height parameters, must type "__" before and after "init," requires "self"
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (W, H) # define size of image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # draw shape on image, draw over entire image with (0, 0, W, H), where (0, 0) is located at image's top-left corner
        self.image.blit(sprite_image, (0, 0))
        self.image.set_colorkey(BLACK) # windows only
        self.rect = self.image.get_rect() # pair image with rectangle object, where (rect.x, rect.y) is located at rectangle object's top-left corner
        # sprite consists of image and rectangle object
    def update(self):
        self.rect.y += 32 # increase sprites' rect.y by 32 pixels
    def turn(self, angle): # calling with sprite, not group
        if count == 1: # in case there is a quick KEYDOWN and KEYUP event
            self.image.blit(player_image_alt, (0, 0))
        if count % 5 == 0:
            self.image.blit(player_image_alt, (0, 0))
        if count % 10 == 0:
            self.image = pygame.transform.rotate(player_image, angle)         
        self.image.set_colorkey(BLACK)
# ---------------------

player = Rectangle(player_image, W, H) # creates a "player" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "block" sprites
    block = Rectangle(block_image, W/2, H/2) # create a "block" sprite
    block.rect.x = random.randrange(0, size[0]+1-W/2, W/2) # position "block" sprite, allow it to touch edge but not breach it
    block.rect.y = random.randrange(0, size[1]+1-H/2, H/2) #  want "block" sprites equally spaced, also mitigates overlap
    pygame.sprite.spritecollide(block, blocks, True) # remove any "block" sprite in same position, essentially preventing "block" sprites from taking same position and essentially preventing overlap, you cannot check if sprite is in group or belongs to group since each sprite is unique
    blocks.add(block) # add "block" sprite to list, no longer append

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
            else:
                timer -= 1 # decrement timer
            # if timer % 5 == 0: # every 5 seconds
                # blocks.update() # move "block" sprites downward
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0 and len(blocks) != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                    angle = 0
                elif action.key == pygame.K_UP:
                    y_increment = -5
                    angle = 90
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                elif action.key == pygame.K_DOWN:
                    y_increment = 5 # note "y_increment," and recall that y increases going downward
                    angle = 270
                player.turn(angle)
                count += 1
            else: # without "else," do nothing
                x_increment = 0
                y_increment = 0
        elif action.type == pygame.KEYUP:
            ticks = pygame.time.get_ticks()
            x_increment = 0
            y_increment = 0
            count = 0
            player.turn(angle)
            # if action.key == pygame.K_RIGHT: 
            # player.image.blit(player_image, (0, 0))

        # -------------------------
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    if size[0]/2+x_offset < 0:
        x_offset = -size[0]/2 # prevent "player" sprite from breaching left edge, solved for x_offset
    elif size[0]/2+x_offset + W > size[0]:
        x_offset = size[0]/2 - W # simplified
    if size[1]/2+y_offset < 0: # note "if"
        y_offset = -size[1]/2 # prevent "player" sprite from breaching top edge, solved for y_offset
    elif size[1]/2+y_offset + H > size[1]:
        y_offset = size[1]/2 - H # simplified
    player.rect.x = size[0]/2+x_offset # position and offset "player" sprite
    player.rect.y = size[1]/2+y_offset
    # pygame.sprite.spritecollide(player, blocks, True) # remove a "block" sprite, if "player" sprite collides with it
    removed = pygame.sprite.spritecollide(player, blocks, True) # remove a "block" sprite, if "player" sprite collides with it
    collisions.add(removed)
    if timer != 0:
        score = len(collisions)
    # --------------
    screen.fill(BLUE) # clear the display
    timer_text = style.render(str(timer), True, RED) # ("time remaining", anti-aliased, COLOR)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, BLACK)
    you_win_text = style.render(None, True, GREEN)
    if timer == 0:
        player.image.fill(WHITE)
        for block in blocks:
            pygame.draw.rect(block.image, LIGHTGRAY, (0, 0, W/2, H/2), width=0)
        screen.fill(GRAY)
        timer_text = style.render(str(timer), True, DARKGRAY)
        score_text = style.render(str(score), True, DARKGRAY)
        game_over_text = style.render("Game Over", True, BLACK)
    if len(blocks) == 0:
        you_win_text = style.render("WINNER!", True, GREEN)
    # --- Drawing code
    screen.blit(player.image, (player.rect.x, player.rect.y)) # draw sprite on screen
    blocks.draw(screen) # draw sprites on screen using list
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
