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
# y_offset = 0
x_increment = 0
# y_increment = 0
invaders = pygame.sprite.Group() # not invaders = [] <-- multiple sprites
collisions = pygame.sprite.Group()
lasers = pygame.sprite.Group()
lasers_alt = pygame.sprite.Group()
vehicles = pygame.sprite.Group()
walls = pygame.sprite.Group()
timer = 30 # 10 seconds
score = 0
first = True
game_over_sound = pygame.mixer.Sound('game_over.ogg')
you_win_sound = pygame.mixer.Sound('you_win.ogg')
style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
vehicle_image = pygame.image.load('ship.png').convert()
#vehicle_image = pygame.transform.scale(vehicle_image, (64, 64))
invader_image = pygame.image.load('alien.png').convert()
invader_image_alt = pygame.image.load('alien_lunging.png').convert()
ticks = int() # some integer, clock sound
W_vehicle = 64 # these variables are for images
H_vehicle = 64
W_invader = 32
H_invader = 32
vehicle_image = pygame.transform.scale(vehicle_image, (W_vehicle, H_vehicle))
count = 0
retries = 2

pygame.display.set_caption("QUESTABOX's \"Space Invaders\" Game")
pygame.key.set_repeat(10) # repeat key press, and add 10 millisecond delay between repeated key press
pygame.time.set_timer(pygame.USEREVENT, 1000) # 1000 milliseconds = 1 second

# --- Functions/classes
# def draw_rect(display, x, y, W, H):
    # pygame.draw.rect(display, WHITE, (x, y, W, H), width=1)
class Rectangle(pygame.sprite.Sprite): # make class of same class as Sprites
    def __init__(self, W, H): # constructor, "self" is like a key for "vehicle" sprite to access class
        super().__init__() # initialize your sprites, similar to init()
        size = (W, H) # local variable
        self.image = pygame.Surface(size) # blank image
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK) # removes background, needed for newer versions of python
        # pygame.draw.rect(self.image, COLOR, (0, 0, W, H), width=0) # drawing on image, not screen
        # self.image.blit(sprite_image, (0, 0))
        self.rect = self.image.get_rect() # pair image with rectangle object, the rectangle object is your sprite
        # nutshell: drawing shape on an image, and you pair that image with a rectangle object, which is your sprite
    def update(self, px): # cannot give function/method just any name
        # global timer
        # if timer % 5 == 0: # every 5 seconds, % modulu operator that computes remainder
        self.rect.y += px # increase sprites' rect.y by 32 pixels
    def lunge(self):
        if count % 2 == 0: # could also have used timer
            self.image.blit(invader_image_alt, (0, 0)) # change picture
        else:
            self.image.blit(invader_image, (0, 0)) # revert
    def retry(self):
        self.rect.x = size[0]/2-W_vehicle/2
        self.rect.y = size[1]-H_vehicle
# ---------------------

wall = Rectangle(1, size[1])
wall.rect.x = 0-1
wall.rect.y = 0
walls.add(wall)

wall = Rectangle(1, size[1])
wall.rect.x = size[0]-1+1
wall.rect.y = 0
walls.add(wall)

for wall in walls:
    wall.image.fill(pygame.Color(1, 1, 1))

vehicle = Rectangle(W_vehicle, H_vehicle)
vehicle.image.blit(vehicle_image, (0, 0))
vehicle.rect.x = size[0]/2+x_offset
vehicle.rect.y = size[1] - H_vehicle
vehicles.add(vehicle)

# for i in range(0, 50): # create and add fifty invaders
while 50-len(invaders) > 0:
    invader = Rectangle(W_invader, H_invader)
    invader.image.blit(invader_image, (0, 0))
    invader.rect.x = random.randrange(0, size[0]+1-W_invader, W_invader) # allow invader to touch edge but not breach it
    invader.rect.y = random.randrange(0, size[1]+1-H_invader-100, H_invader) # "-100" space at canvas bottom
    pygame.sprite.spritecollide(invader, invaders, True) # remove any "invader" sprite in same position
    invaders.add(invader) # not invaders.append(invader) <-- multiple sprites

# we will create "laser" sprites later

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
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
            elif len(vehicles) == 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                game_over_sound.play()
            else: # after one second
                timer -= 1
                if timer % 5 == 0:
                    invaders.update(32)
                for invader in invaders:
                    invader.lunge() # all invaders lunge
                count += 1
                if timer % 7 == 0: # 7 is optional
                    laser = Rectangle(10, 20) # 6 and 10 also optional
                    laser.image.fill(RED)
                    laser.rect.centerx = invaders.sprites()[0].rect.centerx # 0 is index, range 0-49
                    laser.rect.top = invaders.sprites()[0].rect.bottom
                    lasers_alt.add(laser)
        # --- Keyboard events
        elif action.type == pygame.KEYDOWN:
            if timer != 0 and len(invaders) != 0 and len(vehicles) != 0: # "and" or "or" depends
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
                    # laser.rect.x = vehicle.rect.x + 64/2 - 10/2
                    # laser.rect.x = vehicle.rect.centerx - 10/2 # last week, delete
                    laser.rect.centerx = vehicle.rect.centerx # correction
                    # laser.rect.y = vehicle.rect.y - 20 + 10 # "+10" because update() called before "laser" sprites drawn
                    laser.rect.bottom = vehicle.rect.top + 10
                    laser.image.fill(YELLOW)
                    if first == True:
                        lasers.add(laser)
                        first = False
            else:
                x_increment = 0 # make sure "vehicle" sprite stop moving
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
    if size[0]/2+x_offset < 0: # left edge
        x_offset = -size[0]/2
    elif size[0]/2+x_offset + W_vehicle > size[0]: # right edge
        x_offset = size[0]/2 - W_vehicle
    # if size[1]/2+y_offset < 0: # top edge
        # y_offset = -size[1]/2
    # elif size[1]/2+y_offset + 64 > size[1]: # bottom edge
        # y_offset = size[1]/2 - 64
    # vehicle.rect.x = size[0]/2+x_offset
    vehicle.rect.x += x_increment

    hit = pygame.sprite.spritecollide(vehicle, walls, False)
    for wall in hit: # wall that vehicle hit
        if x_increment > 0:
            vehicle.rect.right = wall.rect.left
        else:
            vehicle.rect.left = wall.rect.right

    # vehicle.rect.y = size[1] - H_vehicle # was size[1]/2+y_offset
    # invader.rect.x = random.randrange(0, size[0]+1-32) # allow invader to touch edge but not breach it
    # invader.rect.y = random.randrange(0, size[1]+1-32) # problem is that recalculates each loop

    # removed = pygame.sprite.spritecollide(vehicle, invaders, True) # "True" to remove a "invader" sprite, if "vehicle" sprites collides with it
    for laser in lasers:
        removed = pygame.sprite.spritecollide(laser, invaders, True)
        collisions.add(removed) # when "invader" sprite is removed from invaders list, add it to collisions list
        if removed: # why not put removed == True? 
            lasers.remove(laser)
        elif laser.rect.y < -20: # "laser" sprites leaves canvas
            lasers.remove(laser)
    if timer != 0 and len(vehicles) != 0: # not equal to/is not
        score = len(collisions)
        lasers.update(-10)
        lasers_alt.update(2) # 2 is optional
    for invader in invaders:
        pygame.sprite.spritecollide(invader, vehicles, True)
    for laser in lasers_alt:
        removed = pygame.sprite.spritecollide(laser, vehicles, True)
        if removed and retries > 0:
            vehicles.add(removed) # will reposition the vehicle
            # for vehicle in vehicles:
            vehicle.retry()
            retries -= 1
    if len(vehicles) == 0:
        lasers_alt.update(0)
    # --------------
    screen.fill(BLUE)
    # style = pygame.font.Font(None, 100) # used to be SysFont() from Unit I, but Font() is FASTER! "None" default font, 100 font size
    timer_text = style.render(str(timer), True, RED) # True for anti-aliased, "string" --> str(timer)
    score_text = style.render(str(score), True, GREEN)
    game_over_text = style.render(None, True, BLACK)
    you_win_text = style.render(None, True, GREEN)
    if timer == 0 or len(vehicles) == 0:
        for invader in invaders:
            invader.image.fill(LIGHTGRAY) # similar to self.image.fill(COLOR)
        for laser in lasers:
            laser.image.fill(LIGHTGRAY)
        for laser in lasers_alt:
            laser.image.fill(LIGHTGRAY)
        vehicle.image.fill(WHITE)
        screen.fill(GRAY)
        timer_text = style.render(str(timer), True, DARKGRAY)
        score_text = style.render(str(score), True, DARKGRAY)
        game_over_text = style.render("Game Over", True, BLACK)
    if len(invaders) == 0:
        you_win_text = style.render("WINNER!", True, GREEN)
    # --- Drawing code
    # draw_rect(screen, size[0]/2+x_offset, size[1]/2+y_offset, 64, 64)
    # screen.blit(vehicle.image, vehicle.rect) # draw ONE sprite on screen
    # screen.blit(text, (x, y)) unit 1
    walls.draw(screen)
    invaders.draw(screen) # draw sprite on screen <-- multiple sprites
    lasers_alt.draw(screen)
    screen.blit(vehicle.image, (vehicle.rect.x, vehicle.rect.y))
    lasers.draw(screen)
    screen.blit(timer_text, (10, 10)) # copy image of text onto screen at (10, 10)
    screen.blit(score_text, (size[0]-score_text.get_width()-10, 10))
    screen.blit(game_over_text, game_over_text.get_rect(center = screen.get_rect().center))
    screen.blit(you_win_text, you_win_text.get_rect(center = screen.get_rect().center))
    # ----------------
    pygame.display.flip()
    clock.tick(60)
    if pygame.time.get_ticks() - ticks > 10000:
        clock.tick(1)
