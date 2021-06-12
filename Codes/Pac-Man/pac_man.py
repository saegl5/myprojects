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

size = (704, 512) # (width, height) in pixels, example
screen = pygame.display.set_mode(size) # set up display
clock = pygame.time.Clock() # define "clock"
x_offset = 0 # reordered
y_offset = 0
x_increment = 0
y_increment = 0
pellets = pygame.sprite.Group() # create a list for "pellet" sprites, no longer pellets = [], Group() is class
collisions = pygame.sprite.Group()
timer = 10 # set timer for 10 seconds
score = 0 # initialize score
counter = 0 # for swapping images
ticks = int() # for saving energy
angle = 0
game_over_sound = pygame.mixer.Sound("Sounds/game_over.ogg")

pygame.display.set_caption("QUESTABOX's Cool Game") # title, example
pygame.key.set_repeat(10) # 10 millisecond delay between repeats, optional
pygame.time.set_timer(pygame.USEREVENT, 1000) # count every 1000 milliseconds (i.e., 1 second)

pac_man = pygame.image.load('Images/pac.png') # edited
pac_man.set_colorkey(BLACK)
pac_man_chomp = pygame.image.load('Images/pacb.png') # my image
pac_man_chomp.set_colorkey(BLUE)
dot = pygame.image.load('Images/dot.png').convert()
dot = pygame.transform.scale(dot, (32, 32))
dot.set_colorkey(BLACK)

# --- Functions/Classes
class Rectangle(pygame.sprite.Sprite): # make Rectangle class of same class as sprites, use sentence case to distinguish class from a function
    def __init__(self, COLOR, W, H, image): # define a constructor, class accepts COLOR, width, and height parameters, must type "__" before and after "init," requires "self"
        super().__init__() # initialize your sprites by calling the constructor of the parent (sprite) class
        size = (W, H) # define size of image, local variable
        self.image = pygame.Surface(size) # creates a blank image using Surface class
        self.image.fill(BLACK) # useful if run module on macOS
        self.image.blit(image, (0, 0))
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # draw shape on image, draw over entire image with (0, 0, W, H), where (0, 0) is located at image's top-left corner
        self.rect = self.image.get_rect() # pair image with rectangle object, where (rect.x, rect.y) is located at rectangle object's top-left corner
        # sprite consists of image and rectangle object
    def update(self):
        self.rect.y += 32 # increase sprites' rect.y by 32 pixels
    def swap_image(self, angle):
        if counter % 2 == 0:
            self.image = pygame.transform.rotate(pac_man, angle)
        else:
            self.image.blit(pac_man_chomp, (0, 0))
# ---------------------

player = Rectangle(WHITE, 64, 64, pac_man) # creates a "player" sprite, which will be your sprite to play with, calling class, don't need screen, will instead use it in drawing code, will use original/starting position and offsets in game logic, specified boundary thickness in class definition

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50), create and add fifty "pellet" sprites
    pellet = Rectangle(YELLOW, 32, 32, dot) # create a "pellet" sprite
    pellet.rect.x = random.randrange(0, size[0]+1, 32) # position "pellet" sprite, allow it to touch edge but not breach it
    pellet.rect.y = random.randrange(0, size[1]+1, 32) # want lots of pellets, but if we use a larger step_size, many pellets may overlap
    pellets.add(pellet) # add "pellet" sprite to list, no longer append

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            pygame.quit() # needed if run module through IDLE
            sys.exit() # exit entire process
        elif action.type == pygame.USEREVENT:
            timer -= 1 # decrement timer
            # if timer % 5 == 0: # every 5 seconds
                # pellets.update() # move "pellet" sprites downward
            if timer == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # stop timer, "pellet" sprites stop moving too
                game_over_sound.play()
        # --- Mouse/keyboard events
        elif action.type == pygame.KEYDOWN: # "elif" means else if
            if timer != 0:
                if action.key == pygame.K_RIGHT: # note "action.key"
                    x_increment = 5 # "5" is optional
                    angle = 0
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                elif action.key == pygame.K_DOWN:
                    y_increment = 5 # note "y_increment," and recall that y increases going downward
                    angle = 270
                elif action.key == pygame.K_UP:
                    y_increment = -5
                    angle = 90
                player.swap_image(angle)
                counter += 1
            else:
                x_increment = 0
                y_increment = 0
        elif action.type == pygame.KEYUP:
            ticks = pygame.time.get_ticks()
            x_increment = 0
            y_increment = 0
            counter = 0
            player.swap_image(angle)
            # if action.key == pygame.K_RIGHT: 
            # player.image.blit(pac_man, (0, 0))

        # -------------------------
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    if size[0]/2+x_offset < 0:
        x_offset = -size[0]/2 # prevent "player" sprite from breaching left edge, solved for x_offset
    elif size[0]/2+x_offset + 64 > size[0]:
        x_offset = size[0]/2 - 64 # simplified
    if size[1]/2+y_offset < 0: # note "if"
        y_offset = -size[1]/2 # prevent "player" sprite from breaching top edge, solved for y_offset
    elif size[1]/2+y_offset + 64 > size[1]:
        y_offset = size[1]/2 - 64 # simplified
    player.rect.x = size[0]/2+x_offset # position and offset "player" sprite
    player.rect.y = size[1]/2+y_offset
    # pygame.sprite.spritecollide(player, pellets, True) # remove a "pellet" sprite, if "player" sprite collides with it
    removed = pygame.sprite.spritecollide(player, pellets, True) # remove a "pellet" sprite, if "player" sprite collides with it
    collisions.add(removed)
    if timer != 0:
        score = len(collisions)
    # --------------
    screen.fill(BLUE) # clear the display
    style = pygame.font.Font(None, 100) # faster than SysFont! (filename/object, font size in pixels), "None" utilizes default font (i.e., freesansbold.ttf)
    text_timer = style.render(str(timer), True, RED) # ("time remaining", anti-aliased, COLOR)
    text_score = style.render(str(score), True, GREEN)
    game_over = style.render(None, True, pygame.Color("black"))
    if timer == 0:
        player.image.fill(pygame.Color("white"))
        for pellet in pellets:
            pellet.image.fill(pygame.Color("light gray"))
        screen.fill(pygame.Color("gray"))
        text_timer = style.render(str(timer), True, pygame.Color("dark gray"))
        text_score = style.render(str(score), True, pygame.Color("dark gray"))
        game_over = style.render("Game Over", True, pygame.Color("black"))
    # --- Drawing code
    screen.blit(player.image, (player.rect.x, player.rect.y)) # draw sprite on screen
    pellets.draw(screen) # draw sprites on screen using list
    screen.blit(text_timer, (10, 10)) # copy image of text onto screen at (10, 10)
    screen.blit(text_score, (size[0]-text_score.get_width()-10, 10)) # near top-right corner
    screen.blit(game_over, game_over.get_rect(center = screen.get_rect().center))
    # inside out: pair screen with rectangle object, get object's center, outer get_rect() input requires keyword argument (recall: positional args vs keyword args)
    # outside in: pair game_over with rectangle object whose center is the screen's rectangle object's center...that is, both rectangle objects have the same center
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second
    if pygame.time.get_ticks() - ticks > 10000: # unless user stops playing for more than 10 seconds
        clock.tick(1) # in which case minimize the frame rate
