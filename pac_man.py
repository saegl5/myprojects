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
x_increment_ghost = 1 # ghost moving rightward at launch
pellets = pygame.sprite.Group() # not pellets = [] <-- multiple sprites
collisions = pygame.sprite.Group()
walls = pygame.sprite.Group()
pacmen = pygame.sprite.Group()
timer = 30 # 30 seconds
score = 0
style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
game_over_sound = pygame.mixer.Sound('game_over.ogg')
you_win_sound = pygame.mixer.Sound('you_win.ogg')
pacman_picture = pygame.image.load('pac.png').convert()
pellet_picture = pygame.image.load('dot.png').convert() # need to scale down
ghost_picture = pygame.image.load('red_ghost.png').convert()
# pellet_picture = pygame.transform.scale(pellet_picture, (W_pellet, H_pellet))
#pellet_picture.set_colorkey(BLACK)
W_pacman = 64 # these variables are for images
H_pacman = 64
W_pellet = 32
H_pellet = 32
W_ghost = 64
H_ghost = 64
pellet_picture = pygame.transform.scale(pellet_picture, (W_pellet, H_pellet))
pacman_picture_alt = pygame.image.load('pac_chomp.png').convert()
count = 0
ticks = int()
angle = 0
retries = 2

pygame.display.set_caption("QUESTABOX's \"Pac-Man\" Game")
pygame.key.set_repeat(10) # repeat key press, and add 10 millisecond delay between repeated key press
pygame.time.set_timer(pygame.USEREVENT, 1000) # 1000 milliseconds = 1 second

# --- Functions/classes
# def draw_rect(display, x, y, W, H):
    # pygame.draw.rect(display, WHITE, (x, y, W, H), width=1)
class Rectangle(pygame.sprite.Sprite): # make class of same class as Sprites
    def __init__(self, W, H): # constructor, "self" is like a key for "pacman" sprite to access class
        super().__init__() # initialize your sprites, similar to init()
        size = (W, H) # local variable
        self.image = pygame.Surface(size) # blank image
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK) # removes background, needed for newer versions of python
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # drawing on image, not screen
        # self.image.blit(sprite_picture, (0, 0))
        self.rect = self.image.get_rect() # pair image with rectangle object, the rectangle object is your sprite
        # nutshell: drawing shape on an image, and you pair that image with a rectangle object, which is your sprite
    def update(self):
        # global timer
        # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
        self.rect.y += 32 # increase sprites' rect.y by 32 pixels
    def turn(self, angle):
        if count == 1:
            self.image.blit(pacman_picture_alt, (0, 0))
        if count == 5:
            self.image = pygame.transform.rotate(pacman_picture, angle)
        if count % 10 == 0:
            self.image.blit(pacman_picture_alt, (0, 0))
        if count % 20 == 0:
            self.image = pygame.transform.rotate(pacman_picture, angle)
        self.image.set_colorkey(BLACK)
    def retry(self):
        self.rect.x = size[0]/2 # restore pac-man, bypassed offset
        self.rect.y = size[1]/2
# ---------------------

# inner walls

# top
wall = Rectangle(size[0]-100-100, 10)
wall.rect.x = 100
wall.rect.y = 100
walls.add(wall)

# bottom
wall = Rectangle(size[0]-100-100, 10)
wall.rect.x = 100
wall.rect.y = size[1]-100-10
walls.add(wall)

# middle
wall = Rectangle(10, size[1]-100-100-10-10)
wall.rect.x = size[0]/2-10/2
wall.rect.y = 100+10
walls.add(wall)

# outer walls

# left
wall = Rectangle(1, size[1]) # 1px is minimum width, size[1] height of entire display
wall.rect.x = 0-1 # just subtract by 1 to move wall leftward
wall.rect.y = 0
walls.add(wall)

# right
wall = Rectangle(1, size[1])
wall.rect.x = size[0]-1+1
wall.rect.y = 0
walls.add(wall)

# top
wall = Rectangle(size[0]-2, 1)
wall.rect.x = 1
wall.rect.y = 0-1
walls.add(wall)

# bottom
wall = Rectangle(size[0]-2, 1)
wall.rect.x = 1
wall.rect.y = size[1]-1+1
walls.add(wall)

# needed for newer versions of python
for wall in walls:
    wall.image.fill(pygame.Color(1, 1, 1))

# pacman = Rectangle(WHITE, W_pacman, H_pacman)
# pacman = Rectangle(pacman_picture, W_pacman, H_pacman)
pacman = Rectangle(W_pacman, H_pacman)
pacman.image.blit(pacman_picture, (0, 0)) # was self.image.blit(sprite_picture, (0, 0))
pacman.rect.x = size[0]/2+x_offset
pacman.rect.y = size[1]/2+y_offset
pacmen.add(pacman)

ghost = Rectangle(W_ghost, H_ghost)
ghost.image.blit(ghost_picture, (0, 0))
ghost.rect.x = 200
ghost.rect.y = 300

# for i in range(0, 50): # create and add fifty pellets
while 50-len(pellets) > 0:
    # pellet = Rectangle(YELLOW, W_pellet, H_pellet)
    # pellet = Rectangle(pellet_picture, W_pellet, H_pellet)
    pellet = Rectangle(W_pellet, H_pellet)
    pellet.image.blit(pellet_picture, (0, 0)) # was self.image.blit(sprite_picture, (0, 0))
    # pellet.rect.x = random.randrange(0, size[0]+1-W_pellet) # allow pellet to touch edge but not breach it
    pellet.rect.x = random.randrange(0, size[0]+1-W_pellet, W_pellet) # includes max, but prone to off-by-one error
    pellet.rect.y = random.randrange(0, size[1]+1-H_pellet, H_pellet)
    pygame.sprite.spritecollide(pellet, pellets, True) # remove any "pellet" sprite in same position
    pellets.add(pellet) # not pellets.append(pellet) <-- multiple sprites
    for wall in walls:
        pygame.sprite.spritecollide(wall, pellets, True)

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        elif action.type == pygame.USEREVENT:
            # timer -= 1 # same as timer = timer - 1, count down by 1 each second
            # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
                # pellets.update()
            if timer == 0 or len(pacmen) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # disable timer
                game_over_sound.play()
            elif len(pellets) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            else:
                timer -= 1
        # --- Keyboard events
        elif action.type == pygame.KEYDOWN:
            if timer != 0 and len(pellets) != 0 and len(pacmen) != 0:
                if action.key == pygame.K_RIGHT:
                    x_increment = 5 # speed
                    angle = 0
                    pacman.turn(angle)
                    count += 1
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                    angle = 180
                    pacman.turn(angle)
                    count += 1
                elif action.key == pygame.K_DOWN:
                    y_increment = 5
                    angle = 270
                    pacman.turn(angle)
                    count += 1
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
    #x_offset += x_increment
    #y_offset += y_increment
    # if size[0]/2+x_offset < 0: # left edge
    #     x_offset = -size[0]/2
    # elif size[0]/2+x_offset + W_pacman > size[0]: # right edge
    #     x_offset = size[0]/2 - W_pacman
    # if size[1]/2+y_offset < 0: # top edge
    #     y_offset = -size[1]/2
    # elif size[1]/2+y_offset + H_pacman > size[1]: # bottom edge
    #     y_offset = size[1]/2 - H_pacman

    # pacman.rect.x = size[0]/2+x_offset
    pacman.rect.x += x_increment
    hit = pygame.sprite.spritecollide(pacman, walls, False) # don't remove wall
    for wall in hit:
        if x_increment > 0:
            pacman.rect.right = wall.rect.left
        else: # x_increment = 0 not hitting a wall
            pacman.rect.left = wall.rect.right
    
    # pacman.rect.y = size[1]/2+y_offset
    pacman.rect.y += y_increment
    hit = pygame.sprite.spritecollide(pacman, walls, False) # don't remove wall
    for wall in hit:
        if y_increment > 0:
            pacman.rect.bottom = wall.rect.top
        else: # y_increment = 0 not hitting a wall
            pacman.rect.top = wall.rect.bottom

    # pellet.rect.x = random.randrange(0, size[0]+1-W_pellet) # allow pellet to touch edge but not breach it
    # pellet.rect.y = random.randrange(0, size[1]+1-H_pellet) # problem is that recalculates each loop
    removed = pygame.sprite.spritecollide(pacman, pellets, True) # "True" to remove a "pellet" sprite, if "pacman" sprites collides with it
    collisions.add(removed) # when "pellet" sprite is removed from pellets list, add it to collisions list
    if timer != 0: # not equal to/is not
        score = len(collisions)

    ghost.rect.x += x_increment_ghost # could also decrement
    hit = pygame.sprite.spritecollide(ghost, walls, False)
    if hit:
        x_increment_ghost *= -1 # multiply x_increment_ghost by -1, same as x_increment_ghost = x_increment_ghost * -1
    removed = pygame.sprite.spritecollide(ghost, pacmen, True)
    if removed and retries > 0:
        pacmen.add(removed) # will reposition pac-man
        pacman.retry()
        retries -= 1
    # --------------
    screen.fill(BLUE)
    timer_text = style.render(str(timer), True, RED) # True for anti-aliased, "string" --> str(timer)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, BLACK)
    you_win_text = style.render(None, True, BLACK)
    if timer == 0 or len(pacmen) == 0:
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
    walls.draw(screen)
    pellets.draw(screen) # draw sprite on screen <-- multiple sprites
    screen.blit(ghost.image, (ghost.rect.x, ghost.rect.y))
    screen.blit(pacman.image, (pacman.rect.x, pacman.rect.y))
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
