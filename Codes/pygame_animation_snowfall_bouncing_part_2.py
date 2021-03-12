import pygame, random # import libraries
pygame.init() # initialize the game engine
 
BLUE = pygame.Color("blue") # example, redundant
# can also choose your own color
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels, made size of background image match (could also do opposite)
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# background_image = pygame.image.load("north-pole.jpg") # background image from https://pixy.org/430646/, see License.txt
snowflakes = [] # define a list
# increment = []
x_increment = []
y_increment = []
i = int() # optional, use range() to confine i to 0 or greater
r = 4 # circle radius

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, size[0]+1) # random number between 0 and, including, size[0]
    # y = random.randrange(-size[1], size[1]+1) # random number between 0 and, including, size[1], changed minimum to -size[1] to fill gap that would otherwise develop in animation
    y = random.randrange(0, size[1]+1) # random number between 0 and, including, size[1], changed minimum to -size[1] to fill gap that would otherwise develop in animation, reverted
    snowflakes.append((x, y)) # create a list of random points
    snowflakes[i] = list(snowflakes[i]) # convert each point to a list (lists within a list), "list" is a class
    # increment.append(1) # for initially increasing y by 1 pixel for each point
    x_increment.append(random.randrange(0, 1+1))
    y_increment.append(random.randrange(0, 1+1))

while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the screen, redundant
    # --- Drawing code
    # screen.blit(background_image, (0, 0)) # copy the background image onto the screen starting at (0, 0)
    for i in range(0, len(snowflakes)): # FOR each index in the list, could also use range(0, 50)
        # pygame.draw.circle(screen, WHITE, snowflakes[i], radius=r, width=1)
        # pygame.draw.circle(screen, WHITE, snowflakes[i], radius=r, width=0)
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=r, width=1) # outline but do not fill to see centerpoint
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=1, width=1) # draws centerpoint
        # snowflakes[i][1] += 1 # increase y by 1 pixel for each point, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
        # snowflakes[i][1] += increment[i] # increase y for each point, where each point may have a different increment
        snowflakes[i][0] += x_increment[i]
        snowflakes[i][1] += y_increment[i]
        # if snowflakes[i][1] > size[1]+r: # IF snow flake has left the canvas, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic too
        # if snowflakes[i][1] == size[1]-r: # IF snow flake has reached the canvas' bottom
        # if snowflakes[i][1] == size[1]-r: # IF snowflake has reached the canvas' bottom        
        if snowflakes[i][1] == size[1]-r or snowflakes[i][1] == r: # IF snowflake has reached the canvas' bottom or top
            # Recreate it
            # snowflakes[i][1] = random.randrange(0, size[1]+1)
            # Do so above the canvas
            # snowflakes[i][1] = random.randrange(-50, -r) # -50 is optional
            # More randomness
            # snowflakes[i][0] = random.randrange(0, size[0]+1)
            # Make snowflakes bounce
            # increment[i] *= -1 # same as increment[i] = increment[i] * -1, reverses direction of movement
            x_increment[i] *= -1
            y_increment[i] *= -1
        # elif increment[i] == -1 and snowflakes[i][1] == r: # IF snowflake has already bounced and has reached the canvas' top
        if snowflakes[i][0] == r or snowflakes[i][0] == size[0]-r: # IF snowflake has reached the canvas' left or right edge
            # increment[i] *= -1 # reverses direction of movement, again
            x_increment[i] *= -1
            y_increment[i] *= -1
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
pygame.quit() # formality