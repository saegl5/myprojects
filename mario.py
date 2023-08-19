"""
"Mario" Game
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle # includes update()
from custom.energy import time_stamp, save_energy
from custom.functions import walk, stand
# Other modules to import

pygame.display.set_caption("QUESTABOX's \"Mario\" Game")
pygame.key.set_repeat(10) # 10 millisecond delay between repeated key presses, smooths out movement
# Other settings

BLACK = pygame.Color("black") # transparent background
W_mario = 75 # default, used ratio 3:4
W_goomba = 64
H_mario = 100 # default
H_goomba = 56
GH = 50 # ground height
PH = GH # platform height
V = 5 # example
x_inc_mario = 0 # short for "increment"
y_inc_mario = V/10
x_inc_goomba = V/5
y_inc_goomba = V/10
x_inc_platform = V/5
x_bg = 0
first = True # hopping
halt = True # walking
on = True # ground, platform or goomba
l_mario = canvas.SIZE[0]/2 # where world starts moving, measured from left
l_platform = 400 # let third platform move only 400 pixels, in either direction
mario_frames = pygame.image.load('images/mario_spritesheet.png').convert_alpha()
mario_frames = pygame.transform.scale(mario_frames, (W_mario*9, H_mario*3)) # sprite sheet has 9 columns, 3 rows
goomba_frames = pygame.image.load('images/goomba_spritesheet.png').convert_alpha()
count1 = 0 # mario walk
count2 = 0 # goomba walk
facing_left = False
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.125) # optional
stomped = pygame.sprite.Group()
ground_middle = pygame.image.load('images/dirt_middle.png').convert_alpha()
W_scaled_ground = round(ground_middle.get_width()*GH/ground_middle.get_height())
ground_middle = pygame.transform.scale(ground_middle, (W_scaled_ground, GH))
platform_middle = pygame.image.load('images/grass_middle.png').convert_alpha()
W_scaled_platform = round(platform_middle.get_width()*PH/platform_middle.get_height())
platform_middle = pygame.transform.scale(platform_middle, (W_scaled_platform, PH))
background = pygame.image.load('images/grasslands.png').convert_alpha()
# Other constants and variables

# six blocks, (x, y, w, h) each, additional blocks to right of screen
# not changing y and h, changing x and w, adding horizontal gaps
blocks1 = [ (0,                   canvas.SIZE[1]-GH, canvas.SIZE[0], GH),  # w0 = canvas.SIZE[0],   C0 = 100 (gap size),    x0 = 0
            (canvas.SIZE[0]+100,  canvas.SIZE[1]-GH, 300,            GH),  # w1 = 300,              C1 = 100,               x1 = 0 + canvas.SIZE[0] + 100
            (canvas.SIZE[0]+500,  canvas.SIZE[1]-GH, 600,            GH),  # w2 = 600,              C2 = 400,               x2 = canvas.SIZE[0]+100 + 300 + 100
            (canvas.SIZE[0]+1500, canvas.SIZE[1]-GH, 400,            GH),  # w3 = 400,              C3 = 100,               x3 = canvas.SIZE[0]+500 + 600 + 400
            (canvas.SIZE[0]+2000, canvas.SIZE[1]-GH, 200,            GH),  # w4 = 200,              C4 = 100,               x4 = canvas.SIZE[0]+1500 + 400 + 100
            (canvas.SIZE[0]+2300, canvas.SIZE[1]-GH, 700,            GH) ] # w5 = 700,              C5 = 0 (no gap),        x5 = canvas.SIZE[0]+2000 + 200 + 100
                                                                           #                                                xN = xN-1 + wN-1 + CN-1
grounds = pygame.sprite.Group()
for block in blocks1: # each block
    ground = Rectangle(block[2], block[3]) # see classes.py
    ground.rect.x = block[0]
    ground.rect.y = block[1]
    for i in range(0, block[2], W_scaled_ground): # again block[2] is ground width, W_scaled_ground pixels is step size which is width of each ground image
        ground.image.blit(ground_middle, (i, 0))
    grounds.add(ground)

frame1 = [ (10,           13,           W_mario-17, H_mario-13), 
           (4*W_mario+2,  H_mario+9,    W_mario-10, H_mario-9), 
           (5*W_mario,    H_mario+15,   W_mario,    H_mario-15),
           (3*W_mario+10, 2*H_mario+14, W_mario-12, H_mario-14) ]
# first mario frame is for standing still, second and third for walking/chopping, and fourth for jumping
# will not loop frame list, so to call any parameter use two indices
mario = Rectangle(frame1[0][2], frame1[0][3])
# change W to align mario's right, change H to align mario's bottom
mario.rect.x = 50
mario.rect.y = canvas.SIZE[1]-GH-H_mario
mario.image.blit(mario_frames, (0, 0), (frame1[0][0], frame1[0][1], W_mario, H_mario))
# for (frame[0][0], frame[0][1], W, H), it's x, y, width and height of frame
# change x to align mario's left, change y to align mario's top
# mario.image.set_colorkey(YELLOW) # make background visible temporarily

frame2 = [  (0,          0,          W_goomba, H_goomba),
            (W_goomba,   0,          W_goomba, H_goomba),
            (2*W_goomba, H_goomba/2, W_goomba, H_goomba/2)  ]
clones = [  (600,                         canvas.SIZE[1]-GH-H_goomba, W_goomba, H_goomba),
            (blocks1[2][0]+blocks1[2][2], canvas.SIZE[1]-GH-H_goomba, W_goomba, H_goomba),
            (blocks1[5][0]+blocks1[5][2], canvas.SIZE[1]-GH-H_goomba, W_goomba, H_goomba)  ]
            # keep y, width and height, only change x
            # first goomba sprite starts out near end of first ground sprite            
            # second goomba sprite will start out to right edge of third ground sprite            
            # third goomba sprite will start out to right edge of last ground sprite
goombas = pygame.sprite.Group()
for clone in clones: # each clone
    goomba = Rectangle(clone[2], clone[3])
    goomba.rect.x = clone[0]
    goomba.rect.y = clone[1]
    goomba.image.blit(goomba_frames, (0, 0), (frame2[0][0], frame2[0][1], W_goomba, H_goomba))
    goombas.add(goomba)

# six blocks, (x, y, w, h) each
# not changing w and h, changing x and y, adding horizontal gaps
blocks2 = [ (400,  300, 200, PH),  # y0 = 300,    C0 = 200 (gap size),   x0 = 400
            (800,  250, 200, PH),  # y1 = 250,    C1 = 300,              x1 = 400 + 200 + 200
            (1300, 100, 200, PH),  # y2 = 100,    C2 = 100,              x2 = 800 + 200 + 300
            (1600, 100, 200, PH),  # y3 = 100,    C3 = 500,              x3 = 1300 + 200 + 100
            (2300, 300, 200, PH),  # y4 = 300,    C4 = 200,              x4 = 1600 + 200 + 500
            (2700, 150, 200, PH) ] # y5 = 150,    C5 = 0 (no gap),       x5 = 2300 + 200 + 200
                                   #                                     xN = xN-1 + wN-1 + CN-1, same equation
platforms = pygame.sprite.Group()
for block in blocks2:
    platform = Rectangle(block[2], block[3])
    platform.rect.x = block[0] # reverted to x
    platform.rect.y = block[1] # low enough for mario to jump over
    for j in range(0, block[2], W_scaled_platform):
        platform.image.blit(platform_middle, (j, 0))
    platforms.add(platform)

sprites = pygame.sprite.Group() # all sprites
sprites.add(grounds, platforms, goombas, mario) # displays mario in front of grounds, platforms, and goomba (order matters)
# Other sprites

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            canvas.close()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_inc_mario = V
                halt = False
                facing_left = False
            if event.key == pygame.K_LEFT:
                x_inc_mario = -V
                halt = False
                facing_left = True
            if event.key == pygame.K_SPACE and first == True and on == True:
                y_inc_mario = -2.5*V # y decreases going upward
                first = False
                on = False
                count1 = 0 # display walking frames evenly
                jump_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                first = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                halt = True
                count1 = 0 # display walking frames evenly
        # Other keyboard or mouse/trackpad events

        time_stamp(event)

    mario.rect.x += x_inc_mario
    hit_ground_x = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_x = pygame.sprite.spritecollide(mario, platforms, False)
    if hit_ground_x != []:
        for ground in hit_ground_x:
            if x_inc_mario > 0: # mario moving rightward
                mario.rect.right = ground.rect.left
            elif x_inc_mario < 0:
                mario.rect.left = ground.rect.right
    elif hit_platform_x != []:
        for platform in hit_platform_x:
            if x_inc_mario > 0:
                mario.rect.right = platform.rect.left
            elif x_inc_mario < 0:
                mario.rect.left = platform.rect.right
        if halt == True:
            x_inc_mario = 0
    diff = abs(mario.rect.x - l_mario) # not interested in sign
    if mario.rect.x >= l_mario: # move world leftward
        for ground in grounds:
            ground.rect.x -= diff
        for platform in platforms:
            platform.rect.x -= diff
        for goomba in goombas:
            goomba.rect.x -= diff
        for goomba in stomped:
            goomba.rect.x -= diff
        x_bg -= diff/V
        mario.rect.x = l_mario # keep mario still
    elif mario.rect.x < l_mario: # move world back
        if grounds.sprites()[0].rect.x < 0: # retains initial positions, ground sprites were not randomly positioned
            if grounds.sprites()[0].rect.x + diff > 0: # check gap
                gap = grounds.sprites()[0].rect.x + diff # if any gap, compute its width
                for ground in grounds:
                    ground.rect.x += diff - gap # remove the gap
                for platform in platforms:
                    platform.rect.x += diff - gap # remove the gap
                for goomba in goombas:
                    goomba.rect.x += diff - gap # remove the gap
                for goomba in stomped:
                    goomba.rect.x += diff - gap # remove the gap
                x_bg += diff/V - gap # remove the gap
            else:
                for ground in grounds:
                    ground.rect.x += diff
                for platform in platforms:
                    platform.rect.x += diff
                for goomba in goombas:
                    goomba.rect.x += diff
                for goomba in stomped:
                    goomba.rect.x += diff
                x_bg += diff/V
            mario.rect.x = l_mario
        if mario.rect.x < 0: # left boundary
            mario.rect.x = 0

    # mario.rect.y += y_inc_mario # mario.rect.y truncates decimal part, but okay, simply causes delay
    mario.rect.y = round(mario.rect.y + y_inc_mario) # removes delay, example: round(213 + 0.5) = round(213.5) = 214
    mario_hit_ground_y = pygame.sprite.spritecollide(mario, grounds, False)
    hit_platform_y = pygame.sprite.spritecollide(mario, platforms, False)
    hit_goomba_y = pygame.sprite.spritecollide(mario, goombas, False) # don't want to remove goomba until after showing him squeezed
    if mario_hit_ground_y != []:
        for ground in mario_hit_ground_y:
            mario.rect.bottom = ground.rect.top
        y_inc_mario = V/10 # logical
        on = True
        if halt == True:
            x_inc_mario = 0
            stand(mario, mario_frames, frame1, W_mario, H_mario, facing_left)
        else:
            count1 += 1 # don't just display first step
            walk(count1, mario, mario_frames, frame1, W_mario, H_mario, facing_left)
    elif hit_platform_y != []:
        for platform in hit_platform_y:
            if y_inc_mario < 0: # in jump
                mario.rect.top = platform.rect.bottom # hits his head
            else: # falling or plateaued
                mario.rect.bottom = platform.rect.top
                on = True
            if platform == platforms.sprites()[2]:
                mario.rect.x -= x_inc_platform # takes into account sign, keep inertia effect
        y_inc_mario = V/10 # unsticks mario from below, and in case mario walks off platform
        if halt == True and on == True:
            x_inc_mario = 0
            stand(mario, mario_frames, frame1, W_mario, H_mario, facing_left)
        if halt == False and on == True:
            count1 += 1 # don't just display first step
            walk(count1, mario, mario_frames, frame1, W_mario, H_mario, facing_left)
    elif hit_goomba_y != []:
        for goomba in hit_goomba_y: # not for goomba in goombas
            goomba.rect.y = canvas.SIZE[1]-GH-H_goomba/2
            goomba.image = pygame.Surface((frame2[2][2], frame2[2][3]), pygame.SRCALPHA)
            goomba.image.blit(goomba_frames, (0, 0), (frame2[2][0], frame2[2][1], W_goomba, H_goomba/2))
            count2 = 0 # reset for consistent pause
            y_inc_mario = -1.5*V # short hop
            goombas.remove(goomba) # let goomba rest
            stomped.add(goomba)
            on = True # if want to jump higher
    else: # cycles, fewer for higher values of gravity
        y_inc_mario += V/10 # gravity, place here otherwise increment will keep running
        on = False
        mario.rect.w = frame1[0][2] # using standing width to remove stutter step at left edge of platform sprites
        mario.image = pygame.Surface((frame1[3][2], frame1[3][3]), pygame.SRCALPHA)
        mario.image.blit(mario_frames, (0, 0), (frame1[3][0], frame1[3][1], W_mario, H_mario))
        mario.image = pygame.transform.flip(mario.image, flip_x=not(facing_left), flip_y=False)

    count2 += 1
    for goomba in goombas: # not stomped on
        if mario.rect.x + canvas.SIZE[0] >= goomba.rect.x:
            goomba.rect.x -= x_inc_goomba # move if mario is close to goomba
            if count2 % 20 == 0:
                goomba.image = pygame.Surface((frame2[1][2], frame2[1][3]), pygame.SRCALPHA)
                goomba.image.blit(goomba_frames, (0, 0), (frame2[1][0], frame2[1][1], W_goomba, H_goomba))
                # didn't start with first index 0 because first frame is already displayed
            if count2 % 40 == 0:
                goomba.image = pygame.Surface((frame2[0][2], frame2[0][3]), pygame.SRCALPHA)
                goomba.image.blit(goomba_frames, (0, 0), (frame2[0][0], frame2[0][1], W_goomba, H_goomba))
    for goomba in stomped:
        if count2 % 120 == 0: # pause
            sprites.remove(goomba)

    for goomba in goombas:
        if mario.rect.x + canvas.SIZE[0] >= goomba.rect.x:
            goomba.rect.y += y_inc_goomba # this alone won't move goomba because goomba.rect.y truncates decimal
            goomba_hit_ground_y = pygame.sprite.spritecollide(goomba, grounds, False)
            if goomba_hit_ground_y != []:
                for ground in goomba_hit_ground_y:
                    goomba.rect.bottom = ground.rect.top
            elif goomba.rect.top > canvas.SIZE[1]:
                y_inc_goomba = V/10 # reset
                goombas.remove(goomba) # otherwise increment will keep resetting
                sprites.remove(goomba) # no sense in displaying goomba that is down pit
            else:
                y_inc_goomba += V/10 # gravity

    if l_platform > 0:
        platforms.sprites()[2].rect.x -= x_inc_platform # recall space invaders return fire
        l_platform -= 1
    else:
        x_inc_platform *= -1 # recall pac-man ghosts
        l_platform = 400 # reset
    # Other game logic

    canvas.clean()

    for j in range(2): # use larger range, if necessary
        canvas.screen.blit(background, (x_bg + background.get_width()*j, 0)) # background isn't a sprite
        # j = 0, canvas.screen.blit(background, (x_bg + 1024*0, 0))
        # j = 1, canvas.screen.blit(background, (x_bg + 1024*1, 0))
    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()