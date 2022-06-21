import pygame, random # import modules
import src.canvas as canvas

pygame.init() # initialize any submodules that require it

# BLUE = pygame.Color("blue") # example, redundant
WHITE = pygame.Color("white") # example

clock = pygame.time.Clock() # define "clock"
background_picture = pygame.image.load('images/north_pole.jpeg') # background picture from https://pixy.org/430646/, see License.txt
background_picture = pygame.transform.scale(background_picture, canvas.size)
snowflakes = [] # define a list
# increment = []
# x_increment = []
# y_increment = []
i = int() # optional, use range() to confine i to 0 or greater
r = 4 # circle radius

pygame.display.set_caption("QUESTABOX's Snowfall Animation") # title, example
# snowflakes.append((10, 10)) # append center point, could also extend this and rest
# snowflakes.append((500, 10))
# snowflakes.append((100, 100))
# snowflakes.append((380, 100))
# snowflakes.append((5, 250))
# snowflakes.append((300, 250))
# snowflakes.append((500, 250))
# snowflakes.append((10, 400))
# snowflakes.append((200, 400))
# snowflakes.append((500, 400))
for i in range(0, 50): # FOR fifty indices (i.e., each index between 0 and, but not including, 50)
    x = random.randrange(0, canvas.size[0]+1) # random number between 0 and, including, size[0]
    # y = random.randrange(-size[1], size[1]+1) # random number between 0 and, including, size[1], changed minimum to -size[1] to fill gap that would otherwise develop in animation
    y = random.randrange(0, canvas.size[1]+1) # random number between 0 and, including, size[1], changed minimum to -size[1] to fill gap that would otherwise develop in animation, reverted
    snowflakes.append((x, y)) # create a list of random points
    snowflakes[i] = list(snowflakes[i]) # convert each point to a list (lists within a list), "list" is a class
    # # increment.append(1) # for initially increasing y by 1 pixel for each point
    # x_increment.append(random.randrange(0, 1+1))
    # y_increment.append(random.randrange(0, 1+1))

while True: # keeps display open
    for action in pygame.event.get(): # check for user input when open display
        if action.type == pygame.QUIT: # user clicked close button
            canvas.close()
    # --- Game logic
    # --------------
    # canvas.screen.fill(BLUE) # clear the display, redundant
    # --- Drawing code
    canvas.screen.blit(background_picture, (0, 0)) # copy the background picture onto the screen starting at (0, 0)
    # for center_point in snowflakes: # FOR each item in the list
    for i in range(0, len(snowflakes)): # FOR each index in the list, could also use range(0, 50)
        # highlight one ~~point~~ circle, so we can track it
        # pygame.draw.circle(screen, WHITE, snowflakes[i], radius=r, width=1)
        # pygame.draw.circle(screen, WHITE, center_point, radius=3, width=0)
        # pygame.draw.circle(screen, WHITE, center_point, radius=5, width=1)
        # pygame.draw.circle(screen, BLACK, snowflakes[i], radius=r, width=1) # was width=0
        # pygame.draw.circle(screen, BLACK, snowflakes[i], radius=1, width=1) # optional
        # pygame.draw.circle(screen, WHITE, snowflakes[0], radius=r, width=1)
        # pygame.draw.circle(screen, WHITE, snowflakes[0], radius=1, width=1) # optional        
        # pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=r, width=1) # was width=0,  # outline but do not fill to see centerpoint
        pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=r, width=0) # r was 5
        # pygame.draw.circle(screen, WHITE, center_point, radius=1, width=1)
        # pygame.draw.circle(canvas.screen, WHITE, snowflakes[i], radius=1, width=1) # draws centerpoint
        snowflakes[i][1] += 1 # increase y by 1 pixel for each point, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
        # # snowflakes[i][1] += increment[i] # increase y for each point, where each point may have a different increment
        # snowflakes[i][0] += x_increment[i]
        # snowflakes[i][1] += y_increment[i]
        # if snowflakes[i][1] > size[1]+r: # IF snow flake has left the canvas, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic too
        # if snowflakes[i][1] == size[1]-r: # IF snow flake has reached the canvas' bottom
        # if snowflakes[i][1] == size[1]-r: # IF snowflake has reached the canvas' bottom
        # if snowflakes[i][1] == canvas.size[1]-r or snowflakes[i][1] == r: # IF snowflake has reached the canvas' bottom or top
        if snowflakes[i][1] > canvas.size[1]+r: # IF snow flake has left the canvas, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic too
            # Recreate it
            # snowflakes[i][1] = random.randrange(0, size[1]+1)
            # Do so above the canvas
            snowflakes[i][1] = random.randrange(-50, -r) # -50 is optional
            # More randomness
            snowflakes[i][0] = random.randrange(0, canvas.size[0]+1)
        #     # Make snowflakes bounce
        #     # increment[i] *= -1 # same as increment[i] = increment[i]*-1, reverses direction of movement
        #     x_increment[i] *= -1
        #     y_increment[i] *= -1
        # # elif increment[i] == -1 and snowflakes[i][1] == r: # IF snowflake has already bounced and has reached the canvas' top
        # if snowflakes[i][0] == r or snowflakes[i][0] == size[0]-r: # IF snowflake has reached the canvas' left or right edge
        #     # increment[i] *= -1 # reverses direction of movement, again
        #     x_increment[i] *= -1
        #     y_increment[i] *= -1
    # ----------------
    pygame.display.flip() # update the display
    clock.tick(60) # maximum 60 frames per second