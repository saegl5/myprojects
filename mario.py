"""
"Mario" Game
"""

import pygame
import src.canvas as canvas # still processes pygame.init()
from custom.classes import Rectangle # includes update()
from custom.energy import time_stamp, save_energy
from custom.functions import left_wall, walk, stand
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
y_inc_platform = V/5
x_inc_cloud = V/15
x_bg = 0
x_cd = 0
first = True # hopping
halt = True # walking
on = True # ground, platform or goomba
l_mario = canvas.SIZE[0]/2 # where world starts moving, measured from left
l_third_platform = 400 # let third platform move only 400 pixels, in either direction
l_sixth_platform = 150
mario_frames = pygame.image.load('images/mario_spritesheet.png').convert_alpha()
mario_frames = pygame.transform.scale(mario_frames, (W_mario*9, H_mario*3)) # sprite sheet has 9 columns, 3 rows
goomba_frames = pygame.image.load('images/goomba_spritesheet.png').convert_alpha()
count1 = 0 # mario walk
count2 = 0 # goomba walk
facing_left = False
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(0.125) # optional
stomped = pygame.sprite.Group()
ground_left = pygame.image.load('images/dirt_left.png').convert_alpha()
ground_middle = pygame.image.load('images/dirt_middle.png').convert_alpha()
ground_right = pygame.image.load('images/dirt_right.png').convert_alpha()
W_scaled_ground = round(ground_middle.get_width()*GH/ground_middle.get_height())
ground_left = pygame.transform.scale(ground_left, (W_scaled_ground, GH))
ground_middle = pygame.transform.scale(ground_middle, (W_scaled_ground, GH))
ground_right = pygame.transform.scale(ground_right, (W_scaled_ground, GH))
platform_left = pygame.image.load('images/grass_left.png').convert_alpha()
platform_middle = pygame.image.load('images/grass_middle.png').convert_alpha()
platform_right = pygame.image.load('images/grass_right.png').convert_alpha()
W_scaled_platform = round(platform_middle.get_width()*PH/platform_middle.get_height())
platform_left = pygame.transform.scale(platform_left, (W_scaled_platform, PH))
platform_middle = pygame.transform.scale(platform_middle, (W_scaled_platform, PH))
platform_right = pygame.transform.scale(platform_right, (W_scaled_platform, PH))
background = pygame.image.load('images/grasslands.png').convert_alpha()
plant_picture = pygame.image.load('images/plant.png').convert_alpha()
cloud_picture = pygame.image.load('images/cloud.png').convert_alpha()
cloud_picture = pygame.transform.scale(cloud_picture, (cloud_picture.get_width()*3, cloud_picture.get_height()*3))
# Other constants and variables

# six blocks, (x, y, w, h) each, additional blocks to right of screen
# not changing y and h, changing x and w, adding horizontal gaps
blocks1 = [ (0,    canvas.SIZE[1]-GH, 693, GH),  # w0 = 693,   C0 = 100 (gap size),   x0 = 0
            (793,  canvas.SIZE[1]-GH, 297, GH),  # w1 = 297,   C1 = 100,              x1 = 0 + 693 + 100
            (1190, canvas.SIZE[1]-GH, 594, GH),  # w2 = 594,   C2 = 400,              x2 = 800 + 297 + 100
            (2184, canvas.SIZE[1]-GH, 396, GH),  # w3 = 396,   C3 = 100,              x3 = 1180 + 594 + 400
            (2680, canvas.SIZE[1]-GH, 198, GH),  # w4 = 198,   C4 = 100,              x4 = 2140 + 396 + 100
            (2978, canvas.SIZE[1]-GH, 693, GH) ] # w5 = 693,   C5 = 0 (no gap),       x5 = 2590 + 198 + 100
                                                 #                                    xN = xN-1 + wN-1 + CN-1
grounds = pygame.sprite.Group()
for block in blocks1: # each block
    ground = Rectangle(block[2], block[3]) # see classes.py
    ground.rect.x = block[0]
    ground.rect.y = block[1]
    ground.image.blit(ground_left, (0, 0))
    for i in range(W_scaled_ground, block[2]-W_scaled_ground, W_scaled_ground): # again block[2] is ground width, W_scaled_ground pixels is step size which is width of each ground image
        ground.image.blit(ground_middle, (i, 0))
    ground.image.blit(ground_right, (block[2]-W_scaled_ground, 0))
    grounds.add(ground)

frame1 = [  (10,         13,         W_mario-17, H_mario-13), 
            (3,          H_mario+12, W_mario-7,  H_mario-12),
            (W_mario+12, H_mario+10, W_mario-23, H_mario-10),
            (W_mario+4,  9,          W_mario-8,  H_mario-9)  ]
# first mario frame is for standing still, second and third for walking, and fourth for jumping
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
blocks2 = [ (400,  300, 200, PH),  # y0 = 300,    C0 = 193 (gap size),   x0 = 400
            (793,  250, 200, PH),  # y1 = 250,    C1 = 300,              x1 = 400 + 200 + 193
            (1293, 100, 200, PH),  # y2 = 100,    C2 = 100,              x2 = 793 + 200 + 300
            (1593, 100, 200, PH),  # y3 = 100,    C3 = 500,              x3 = 1293 + 200 + 100
            (2293, 300, 200, PH),  # y4 = 300,    C4 = 187,              x4 = 1593 + 200 + 500
            (2680, 150, 200, PH) ] # y5 = 150,    C5 = 0 (no gap),       x5 = 2293 + 200 + 187
                                   #                                     xN = xN-1 + wN-1 + CN-1, same equation
platforms = pygame.sprite.Group()
for block in blocks2:
    platform = Rectangle(block[2], block[3])
    platform.rect.x = block[0] # reverted to x
    platform.rect.y = block[1] # low enough for mario to jump over
    platform.image.blit(platform_left, (0, 0))
    for j in range(W_scaled_platform, block[2]-W_scaled_platform, W_scaled_platform):
        platform.image.blit(platform_middle, (j, 0))
    platform.image.blit(platform_right, (block[2]-W_scaled_platform, 0))
    platforms.add(platform)

plant_locations = [ (blocks1[0][0]),
                    (blocks1[1][0]+200),
                    (blocks1[2][0]+100),
                    (blocks1[3][0]),
                    (blocks1[4][0]+50),
                    (blocks1[5][0]+400) ]

plants = pygame.sprite.Group()
for _ in range(0, len(plant_locations)):
    plant = Rectangle(plant_picture.get_width(), plant_picture.get_height())
    plant.rect.x = plant_locations[_]
    plant.rect.y = canvas.SIZE[1]-GH-plant_picture.get_height()
    plant.image.blit(plant_picture, (0, 0)) # should crop
    plants.add(plant)

walls = pygame.sprite.Group()
walls.add(left_wall()) # outer wall

sprites = pygame.sprite.Group() # all sprites
sprites.add(walls, plants, grounds, platforms, goombas, mario) # displays mario in front of grounds, platforms, goomba, and plants (order matters)
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

    x_inc_platform, l_third_platform = platforms.sprites()[2].update(x_inc_platform, 0, l_third_platform) # y_inc_platform = 0

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
        for plant in plants:
            plant.rect.x -= diff
        x_cd -= 2*diff/V
        mario.rect.x = l_mario # keep mario still
    elif mario.rect.x < l_mario: # move world back
        if grounds.sprites()[0].rect.x <= left_wall().rect.x: # retains initial positions, ground sprites were not randomly positioned
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
                for plant in plants:
                    plant.rect.x += diff - gap # remove the gap
                x_cd += 2*diff/V - gap
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
                for plant in plants:
                    plant.rect.x += diff
                x_cd += 2*diff/V
            mario.rect.x = l_mario
        hit_wall = pygame.sprite.spritecollide(mario, walls, False) # acts as left boundary
        for wall in hit_wall:
            mario.rect.left = wall.rect.right # currently only one wall

    y_inc_platform, l_sixth_platform = platforms.sprites()[5].update(0, y_inc_platform, l_sixth_platform) # x_inc_platform = 0

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
            y_inc_mario = V/10 # unsticks mario from below, and in case mario walks off platform
            if platform == platforms.sprites()[2]:
                mario.rect.x -= x_inc_platform # takes into account sign, keep inertia effect
            elif platform == platforms.sprites()[5] and mario.rect.bottom == platform.rect.top:
                y_inc_mario += 3*V/10 # add inertia (like drafting)
            elif platform == platforms.sprites()[5] and mario.rect.top == platform.rect.bottom:
                y_inc_mario += V/10 # nudge mario downward
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
        mario.image = pygame.transform.flip(mario.image, flip_x=facing_left, flip_y=False)

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

    x_cd -= x_inc_cloud
    # Other game logic

    canvas.clean()

    for j in range(2): # use larger range, if necessary
        canvas.screen.blit(background, (x_bg + background.get_width()*j, 0)) # background isn't a sprite
        # j = 0, canvas.screen.blit(background, (x_bg + 1024*0, 0))
        # j = 1, canvas.screen.blit(background, (x_bg + 1024*1, 0))

    canvas.screen.blit(cloud_picture, (x_cd + 500, 100)) # clouds also aren't sprites
    canvas.screen.blit(cloud_picture, (x_cd + 1000, 200))
    canvas.screen.blit(cloud_picture, (x_cd + 1200, 150))
    canvas.screen.blit(cloud_picture, (x_cd + 1800, 225))

    sprites.draw(canvas.screen)
    # Other copying, drawing or font codes

    canvas.show()

    save_energy()