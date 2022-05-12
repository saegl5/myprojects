import pygame, random # import modules
import src.canvas as canvas

pygame.init() # initialize any submodules that require it
 
# BLUE = pygame.Color("blue") # example, redundant
WHITE = pygame.Color("white") # example

clock = pygame.time.Clock() # define "clock"
background_picture = pygame.image.load('images/north_pole.jpg') # background picture from https://pixy.org/430646/, see License.txt
snowflakes = [] # define a list
i = int() # optional, use range() to confine i to 0 or greater
r = 4 # circle radius

pygame.display.set_caption("QUESTABOX's Snowfall Animation") # title, example

for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, canvas.size[0]+1) # random number between 0 and, including, canvas.size[0]
    y = random.randrange(0, canvas.size[1]+1) # random number between 0 and, including, canvas.size[1]
    snowflakes.append((x, y)) # create a list of random points
    snowflakes[i] = list(snowflakes[i]) # convert each point to a list (lists within a list), "list" is a class

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
    # --- Game logic
    # --------------
    # canvas.screen.fill(BLUE) # clear the display, redundant
    # --- Drawing code
    canvas.screen.blit(background_picture, (0, 0)) # copy the background picture onto the screen starting at (0, 0)
    for i in range(0, len(snowflakes)): # FOR each index in the list, could also use range(0, 50)
        # pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=r, width=1)
        pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=r, width=0)
        # pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=1, width=1)
        snowflakes[i][1] += 1 # increase y by 1 pixel for each point, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
        if snowflakes[i][1] > canvas.size[1]+r: # IF snow flake has left the canvas, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic too
            # Recreate it
            # snowflakes[i][1] = random.randrange(0, canvas.size[1]+1)
            # Do so above the canvas
            snowflakes[i][1] = random.randrange(-50, -r) # -50 is optional
            # More randomness
            snowflakes[i][0] = random.randrange(0, canvas.size[0]+1)
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second