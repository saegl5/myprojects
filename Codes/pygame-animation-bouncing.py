import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

LIGHTGRAY = (211, 211, 211) # example
# (Red, Green, Blue) = (0-255, 0-255, 0-255)
# 0-255 is amount of color
# the amount of color is additive
# can also choose your own color
# parentheses of numbers (e.g., (211, 211, 211)) is called a tuple
BLACK = (0, 0, 0) # example

size = (700, 500) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
rect_x = 50 # initialize starting x position of the rectangle
rect_y = 50 # initialize starting y position of the rectangle
rect_change_x = 1
rect_change_y = 5 
# lower number moves rectangle slower, higher moves it faster
# # negative number changes direction

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own
 
while not done: # meaning while true, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit While loop on next loop, loop will not run while false
    screen.fill(LIGHTGRAY) # clear the screen
    # --- Drawing code
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, 60, 50), width=0)
    # pygame.draw.rect(screen, LIGHTGRAY, (rect_x + 10, rect_y + 10, 40, 30))
    rect_x += rect_change_x
    rect_y += rect_change_y
    if rect_y > 450 or rect_y < 0:
        rect_change_y = rect_change_y * -1 # bounce off bottom or top edges
    if rect_x > 640 or rect_x < 0:
        rect_change_x = rect_change_x * -1 # bounce off left or right edges
    # ----------------
    pygame.display.flip() # update the screen
    clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through While loop each second)
pygame.quit() # formality