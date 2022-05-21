import pygame, random, canvas

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

clock = pygame.time.Clock()
x_offset = 0
# y_offset = 0
x_increment = 0
# y_increment = 0
invaders = pygame.sprite.Group() # not invaders = [] <-- multiple sprites
collisions = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
spaceships = pygame.sprite.Group()
barriers = pygame.sprite.Group()
walls = pygame.sprite.Group()
timer = 30 # 10 seconds
score = 0
first = True
game_over_sound = pygame.mixer.Sound('game_over.ogg')
you_win_sound = pygame.mixer.Sound('you_win.ogg')
spaceship_laser_sound = pygame.mixer.Sound('laserLarge.ogg')
spaceship_explosion_sound = pygame.mixer.Sound('explosionCrunch.ogg')
invader_laser_sound = pygame.mixer.Sound('laserSmall.ogg')
invader_explosion_sound = pygame.mixer.Sound('lowFrequency_explosion.ogg')
style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
style_header = pygame.font.Font(None, 30)
style_header.set_italic(True)
spaceship_picture = pygame.image.load('ship.png').convert()
#spaceship_picture = pygame.transform.scale(spaceship_picture, (64, 64))
invader_picture = pygame.image.load('alien.png').convert()
invader_picture_alt = pygame.image.load('alien_lunging.png').convert()
ticks = int() # some integer, clock sound
W_spaceship = 64 # these variables are for images
H_spaceship = 64
W_invader = 32
H_invader = 32
spaceship_picture = pygame.transform.scale(spaceship_picture, (W_spaceship, H_spaceship))
spaceship_picture_retries = pygame.transform.scale(spaceship_picture, (W_spaceship/2, H_spaceship/2))
count = 0
retries = 2
p = 5 # chop up each barrier into 5 pieces

pygame.display.set_caption("QUESTABOX's \"Space Invaders\" Game")
pygame.key.set_repeat(10) # repeat key press, and add 10 millisecond delay between repeated key press
pygame.time.set_timer(pygame.USEREVENT, 1000) # 1000 milliseconds = 1 second

# --- Functions/classes
# def draw_rect(display, x, y, W, H):
    # pygame.draw.rect(display, WHITE, (x, y, W, H), width=1)
class Rectangle(pygame.sprite.Sprite): # make class of same class as Sprites
    def __init__(self, W, H): # constructor, "self" is like a key for "spaceship" sprite to access class
        super().__init__() # initialize your sprites, similar to init()
        size = (W, H) # local variable
        self.image = pygame.Surface(size) # blank image
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK) # removes background, needed for newer versions of python
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # drawing on image, not screen
        # self.image.blit(sprite_picture, (0, 0))
        self.rect = self.image.get_rect() # pair image with rectangle object, the rectangle object is your sprite
        # nutshell: drawing shape on an image, and you pair that image with a rectangle object, which is your sprite
    def update(self, px): # cannot give function/method just any name
        # global timer
        # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
        self.rect.y += px # increase sprites' rect.y by 32 pixels
    def lunge(self):
        if count % 2 == 0: # could also have used timer
            self.image.blit(invader_picture_alt, (0, 0)) # change picture
        else:
            self.image.blit(invader_picture, (0, 0)) # revert
    def retry(self):
        self.rect.centerx = canvas.screen.get_rect().centerx
        self.rect.y = canvas.size[1]-H_spaceship
    def return_fire(self, index):
        self.image.fill(RED)
        self.rect.centerx = invaders.sprites()[index].rect.centerx # 0 is index, range 0-49
        self.rect.top = invaders.sprites()[index].rect.bottom
        lasers_alt.add(self)
        invader_laser_sound.play()
# ---------------------

wall = Rectangle(1, canvas.size[1])
wall.rect.x = 0-1
wall.rect.y = 0
walls.add(wall)

wall = Rectangle(1, canvas.size[1])
wall.rect.x = canvas.size[0]-1+1
wall.rect.y = 0
walls.add(wall)

# for wall in walls:
#     wall.image.fill(pygame.Color(1, 1, 1))

# left barrier
for i in range(0, p): # i = 0, 1, 2, 3, ..., p-1
    barrier = Rectangle(250/p, 25)
    barrier.rect.x = 50+i*250/p
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

# right barrier
for i in range(0, p): # i = 0, 1, 2, 3, ..., p-1
    barrier = Rectangle(250/p, 25)
    barrier.rect.x = canvas.size[0]-250-50+i*250/p
    barrier.rect.y = 400
    barrier.image.fill(WHITE)
    barriers.add(barrier)

spaceship = Rectangle(W_spaceship, H_spaceship)
spaceship.image.blit(spaceship_picture, (0, 0))
spaceship.rect.centerx = canvas.screen.get_rect().centerx
spaceship.rect.y = canvas.size[1] - H_spaceship
spaceships.add(spaceship)

# for i in range(0, 50): # create and add fifty invaders
while 50-len(invaders) > 0:
    invader = Rectangle(W_invader, H_invader)
    invader.image.blit(invader_picture, (0, 0))
    invader.rect.x = random.randrange(0, canvas.size[0]+1-W_invader, W_invader) # allow invader to touch edge but not breach it
    invader.rect.y = random.randrange(0, canvas.size[1]+1-H_invader-200, H_invader) # "-100" space at canvas bottom
    pygame.sprite.spritecollide(invader, invaders, True) # remove any "invader" sprite in same position
    invaders.add(invader) # not invaders.append(invader) <-- multiple sprites

# we will create "laser" sprites later

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
        elif action.type == pygame.USEREVENT:
            #timer -= 1 # same as timer = timer - 1, count down by 1 each second
            #if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
                #invaders.update(32)
            if timer == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0) # disable timer
                game_over_sound.play()
            elif len(invaders) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                you_win_sound.play()
            elif len(spaceships) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                game_over_sound.play()
            else: # after one second
                timer -= 1
                if timer % 5 == 0:
                    invaders.update(32)
                for invader in invaders:
                    invader.lunge() # all invaders lunge
                count += 1
                if timer % 4 == 0 and len(invaders) > 0: # 7 is optional
                    laser = Rectangle(10, 20) # 6 and 10 also optional
                    laser.return_fire(0)
                if timer % 7 == 0 and len(invaders) > 1: # 7 is optional
                    laser = Rectangle(10, 20) # 6 and 10 also optional
                    laser.return_fire(1)
                if timer % 11 == 0 and len(invaders) > 2: # 7 is optional
                    laser = Rectangle(10, 20) # 6 and 10 also optional
                    laser.return_fire(2)
        # --- Keyboard events
        elif action.type == pygame.KEYDOWN:
            if timer != 0 and len(invaders) != 0 and len(spaceships) != 0: # "and" or "or" depends
                if action.key == pygame.K_RIGHT:
                    x_increment = 5 # speed
                elif action.key == pygame.K_LEFT:
                    x_increment = -5
                # elif action.key == pygame.K_DOWN:
                    # y_increment = 5
                # elif action.key == pygame.K_UP:
                    # y_increment = -5
                elif action.key == pygame.K_SPACE:
                    laser = Rectangle(10, 20)
                    # laser.rect.x = spaceship.rect.x + 64/2 - 10/2
                    # laser.rect.x = spaceship.rect.centerx - 10/2 # last week, delete
                    laser.rect.centerx = spaceship.rect.centerx # correction
                    # laser.rect.y = spaceship.rect.y - 20 + 10 # "+10" because update() called before "laser" sprites drawn
                    laser.rect.bottom = spaceship.rect.top + 10
                    laser.image.fill(YELLOW)
                    if first == True:
                        lasers.add(laser)
                        spaceship_laser_sound.play()
                        first = False
            else:
                x_increment = 0 # make sure "spaceship" sprite stop moving
        elif action.type == pygame.KEYUP:
            if action.key == pygame.K_RIGHT or action.key == pygame.K_LEFT:
                x_increment = 0
            elif action.key == pygame.K_SPACE:
                first = True
            # y_increment = 0
            ticks = pygame.time.get_ticks()
        # -------------------
    # --- Game logic
    # x_offset += x_increment
    # y_offset += y_increment
    # if size[0]/2+x_offset < 0: # left edge
    #     x_offset = -size[0]/2
    # elif size[0]/2+x_offset + W_spaceship > size[0]: # right edge
    #     x_offset = size[0]/2 - W_spaceship
    # if size[1]/2+y_offset < 0: # top edge
        # y_offset = -size[1]/2
    # elif size[1]/2+y_offset + 64 > size[1]: # bottom edge
        # y_offset = size[1]/2 - 64
    # spaceship.rect.x = size[0]/2+x_offset
    spaceship.rect.x += x_increment

    hit = pygame.sprite.spritecollide(spaceship, walls, False)
    for wall in hit: # wall that spaceship hit
        if x_increment > 0:
            spaceship.rect.right = wall.rect.left
        else:
            spaceship.rect.left = wall.rect.right

    # spaceship.rect.y = size[1] - H_spaceship # was size[1]/2+y_offset
    # invader.rect.x = random.randrange(0, size[0]+1-32) # allow invader to touch edge but not breach it
    # invader.rect.y = random.randrange(0, size[1]+1-32) # problem is that recalculates each loop

    # removed = pygame.sprite.spritecollide(spaceship, invaders, True) # "True" to remove a "invader" sprite, if "spaceship" sprites collides with it
    for laser in lasers:
        invader_removed = pygame.sprite.spritecollide(laser, invaders, True)
        collisions.add(invader_removed) # when "invader" sprite is removed from invaders list, add it to collisions list
        if invader_removed != []: # why not put removed == True? 
            lasers.remove(laser)
            invader_explosion_sound.play()
        # elif laser.rect.y < -20: # "laser" sprites leaves canvas
        elif laser.rect.bottom < 0: # "laser" sprites leaves canvas
            lasers.remove(laser)
    if timer != 0 and len(spaceships) != 0 and len(invaders) != 0: # not equal to/is not
        score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2) # 2 is optional
    # if len(spaceships) == 0:
    else: # stops lasers from moving when game over or win game
        lasers.update(0)
        lasers_alt.update(0)
    for invader in invaders:
        spaceship_removed = pygame.sprite.spritecollide(invader, spaceships, True)
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed) # will reposition the spaceship
            # for spaceship in spaceships:
            spaceship.retry()
            retries -= 1
    for laser in lasers_alt:
        spaceship_removed = pygame.sprite.spritecollide(laser, spaceships, True)
        if spaceship_removed != []:
            spaceship_explosion_sound.play()
        if spaceship_removed != [] and retries > 0:
            spaceships.add(spaceship_removed) # will reposition the spaceship
            # for spaceship in spaceships:
            spaceship.retry()
            retries -= 1
            lasers_alt.remove(laser)
        elif laser.rect.top > canvas.size[1]:
            lasers_alt.remove(laser)
    if retries == 2:
        spaceship_retries_box_1 = spaceship_picture_retries
        spaceship_retries_box_2 = spaceship_picture_retries
    elif retries == 1:
        spaceship_retries_box_1 = spaceship_picture_retries
        spaceship_retries_box_2 = pygame.Surface((0, 0))
    else:
        spaceship_retries_box_1 = pygame.Surface((0, 0))
        spaceship_retries_box_2 = pygame.Surface((0, 0))
    spaceship_retries_box_1.set_colorkey(BLACK)
    spaceship_retries_box_2.set_colorkey(BLACK)
    for laser in lasers_alt:
        barrier_removed = pygame.sprite.spritecollide(laser, barriers, True)
        if barrier_removed != []:
            lasers_alt.remove(laser)
    # --------------
    canvas.screen.fill(BLUE)
    # style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
    timer_header = style_header.render("Time Left", False, RED)
    timer_text = style.render(str(timer), False, RED) # True for anti-aliased, "string" --> str(timer)
    score_header = style_header.render("Score", False, GREEN)
    score_text = style.render(str(score), False, GREEN)
    game_over_text = style.render(None, False, BLACK)
    you_win_text = style.render(None, False, GREEN)
    if timer == 0 or len(spaceships) == 0:
        for invader in invaders:
            invader.image.fill(LIGHTGRAY) # similar to self.image.fill(COLOR)
        for laser in lasers:
            laser.image.fill(LIGHTGRAY)
        for laser in lasers_alt:
            laser.image.fill(LIGHTGRAY)
        spaceship.image.fill(WHITE)
        canvas.screen.fill(GRAY)
        timer_text = style.render(str(timer), False, DARKGRAY)
        score_text = style.render(str(score), False, DARKGRAY)
        game_over_text = style.render("Game Over", False, BLACK)
        timer_header = style_header.render("Time Left", False, DARKGRAY)
        score_header = style_header.render("Score", False, DARKGRAY)
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", False, GREEN)
    if timer == 0:
        pygame.draw.rect(spaceship_picture_retries, WHITE, (0, 0, W_spaceship/2, H_spaceship/2), width=0)
    # --- Drawing code
    # draw_rect(screen, size[0]/2+x_offset, size[1]/2+y_offset, 64, 64)
    # screen.blit(spaceship.image, spaceship.rect) # draw ONE sprite on screen
    # screen.blit(text, (x, y)) unit 1
    walls.draw(canvas.screen)
    barriers.draw(canvas.screen)
    invaders.draw(canvas.screen) # draw sprite on screen <-- multiple sprites
    lasers_alt.draw(canvas.screen)
    canvas.screen.blit(spaceship.image, (spaceship.rect.x, spaceship.rect.y)) # so you can see block, otherwise can just use spaceships.draw(screen)
    lasers.draw(canvas.screen)
    canvas.screen.blit(timer_header, (10, 10))
    canvas.screen.blit(timer_text, (10, 30)) # copy image of text onto screen at (10, 10)
    canvas.screen.blit(spaceship_retries_box_1, (100, 10))
    canvas.screen.blit(spaceship_retries_box_2, (100+W_spaceship/2, 10))
    canvas.screen.blit(score_header, (canvas.size[0]-score_header.get_width()-10, 10))
    canvas.screen.blit(score_text, (canvas.size[0]-score_text.get_width()-10, 30))
    canvas.screen.blit(game_over_text, game_over_text.get_rect(center = canvas.screen.get_rect().center))
    canvas.screen.blit(you_win_text, you_win_text.get_rect(center = canvas.screen.get_rect().center))
    # ----------------
    pygame.display.flip()
    clock.tick(60)
    if pygame.time.get_ticks() - ticks > 10000:
        clock.tick(1)
