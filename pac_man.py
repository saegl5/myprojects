import pygame
import sys
import random

pygame.init()

BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")
BLACK = pygame.Color("black")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
LIGHTGRAY = pygame.Color("light gray")
GRAY = pygame.Color("gray")
DARKGRAY = pygame.Color("dark gray")

size = (704, 512)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
x_offset = 0
y_offset = 0
x_increment = 0
y_increment = 0
pellets = pygame.sprite.Group() # not pellets = [] <-- multiple sprites
collisions = pygame.sprite.Group()
timer = 30 # 30 seconds
score = 0
style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
game_over_sound = pygame.mixer.Sound('game_over.ogg')
you_win_sound = pygame.mixer.Sound('you_win.ogg')
pacman_image = pygame.image.load('pac.png').convert()
pellet_image = pygame.image.load('dot.png').convert() # need to scale down
# pellet_image = pygame.transform.scale(pellet_image, (W_pellet, H_pellet))
#pellet_image.set_colorkey(BLACK)
W_pacman = 64
H_pacman = 64
W_pellet = 32
H_pellet = 32
pellet_image = pygame.transform.scale(pellet_image, (W_pellet, H_pellet))
pacman_image_alt = pygame.image.load('pac_chomp.png').convert()
count = 0
ticks = int()
angle = 0

pygame.display.set_caption("QUESTABOX's Cool Game")
pygame.key.set_repeat(10) # repeat key press, and add 10 millisecond delay between repeated key press
pygame.time.set_timer(pygame.USEREVENT, 1000) # 1000 milliseconds = 1 second

# --- Functions/classes
# def draw_rect(display, x, y, W, H):
    # pygame.draw.rect(display, WHITE, (x, y, W, H), width=1)
class Rectangle(pygame.sprite.Sprite): # make class of same class as Sprites
    def __init__(self, sprite_image, W, H): # constructor, "self" is like a key for "pacman" sprite to access class
        super().__init__() # initialize your sprites, similar to init()
        size = (W, H) # local variable
        self.image = pygame.Surface(size) # blank image
        self.image.fill(BLACK)
        # self.image.set_colorkey(BLACK) # removes background
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # drawing on image, not screen
        self.image.blit(sprite_image, (0, 0))
        self.rect = self.image.get_rect() # pair image with rectangle object, the rectangle object is your sprite
        # nutshell: drawing shape on an image, and you pair that image with a rectangle object, which is your sprite
    def update(self):
        # global timer
        # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
        self.rect.y += 32 # increase sprites' rect.y by 32 pixels
    def turn(self, angle):
        if count == 1:
            self.image.blit(pacman_image_alt, (0, 0))
        if count % 5 == 0:
            self.image.blit(pacman_image_alt, (0, 0))
        if count % 10 == 0:
            self.image = pygame.transform.rotate(pacman_image, angle)
        self.image.set_colorkey(BLACK)
# ---------------------

# pacman = Rectangle(WHITE, W_pacman, H_pacman)
pacman = Rectangle(pacman_image, W_pacman, H_pacman)

# for i in range(0, 50): # create and add fifty pellets
while 50-len(pellets) > 0:
    # pellet = Rectangle(YELLOW, W_pellet, H_pellet)
    pellet = Rectangle(pellet_image, W_pellet, H_pellet)
    # pellet.rect.x = random.randrange(0, size[0]+1-W_pellet) # allow pellet to touch edge but not breach it
    pellet.rect.x = random.randrange(0, size[0]-W_pellet, W_pellet) # includes max, but prone to off-by-one error
    pellet.rect.y = random.randrange(0, size[1]+1-H_pellet, H_pellet)
    pygame.sprite.spritecollide(pellet, pellets, True) # remove any "pellet" sprite in same position
    pellets.add(pellet) # not pellets.append(pellet) <-- multiple sprites

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        elif action.type == pygame.USEREVENT:
            # timer -= 1 # same as timer = timer - 1, count down by 1 each second
            # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
                # pellets.update()
            if timer == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # disable timer
                game_over_sound.play()
            elif len(pellets) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else:
                timer -= 1
        # --- Keyboard events
        elif action.type == pygame.KEYDOWN:
            if timer != 0 and len(pellets) != 0:
                if action.key == pygame.K_RIGHT:
                    x_increment = 5 # speed
                    angle = 0
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                elif action.key == pygame.K_DOWN:
                    y_increment = 5
                    angle = 270
                elif action.key == pygame.K_UP:
                    y_increment = -5
                    angle = 90
                pacman.turn(angle)
                count += 1
            else:
                x_increment = 0
                y_increment = 0
        elif action.type == pygame.KEYUP:
            x_increment = 0
            y_increment = 0
            count = 0
            pacman.turn(angle)
            ticks = pygame.time.get_ticks()
        # -------------------
    # --- Game logic
    x_offset += x_increment
    y_offset += y_increment
    if size[0]/2+x_offset < 0: # left edge
        x_offset = -size[0]/2
    elif size[0]/2+x_offset + W_pacman > size[0]: # right edge
        x_offset = size[0]/2 - W_pacman
    if size[1]/2+y_offset < 0: # top edge
        y_offset = -size[1]/2
    elif size[1]/2+y_offset + H_pacman > size[1]: # bottom edge
        y_offset = size[1]/2 - H_pacman
    pacman.rect.x = size[0]/2+x_offset
    pacman.rect.y = size[1]/2+y_offset
    # pellet.rect.x = random.randrange(0, size[0]+1-W_pellet) # allow pellet to touch edge but not breach it
    # pellet.rect.y = random.randrange(0, size[1]+1-H_pellet) # problem is that recalculates each loop
    removed = pygame.sprite.spritecollide(pacman, pellets, True) # "True" to remove a "pellet" sprite, if "pacman" sprites collides with it
    collisions.add(removed) # when "pellet" sprite is removed from pellets list, add it to collisions list
    if timer != 0: # not equal to/is not
        score = len(collisions)
    # --------------
    screen.fill(BLUE)
    timer_text = style.render(str(timer), True, RED) # True for anti-aliased, "string" --> str(timer)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, BLACK)
    you_win_text = style.render(None, True, BLACK)
    if timer == 0:
        for pellet in pellets:
            pellet.image.fill(LIGHTGRAY)
        pacman.image.fill(WHITE)
        screen.fill(GRAY)
        timer_text = style.render(str(timer), True, DARKGRAY) # True for anti-aliased, "string" --> str(timer)
        score_text = style.render(str(score), True, DARKGRAY)
        game_over_text = style.render("Game Over", True, BLACK)
    if len(pellets) == 0:
        you_win_text = style.render("WINNER!", True, BLACK)
    # --- Drawing code
    # draw_rect(screen, size[0]/2+x_offset, size[1]/2+y_offset, W_pacman, H_pacman)
    # screen.blit(pacman.image, pacman.rect) # draw ONE sprite on screen
    # screen.blit(text, (x, y)) unit 1
    screen.blit(pacman.image, (pacman.rect.x, pacman.rect.y))
    pellets.draw(screen) # draw sprite on screen <-- multiple sprites
    # style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
    screen.blit(timer_text, (10, 10)) # copy image of text onto screen at (10, 10)
    screen.blit(score_text, (size[0]-score_text.get_width()-10, 10))
    screen.blit(game_over_text, game_over_text.get_rect(center = screen.get_rect().center))
    screen.blit(you_win_text, you_win_text.get_rect(center = screen.get_rect().center))
    # ----------------
    pygame.display.flip()
    clock.tick(60)
    if pygame.time.get_ticks() - ticks > 10000:
        clock.tick(1)
