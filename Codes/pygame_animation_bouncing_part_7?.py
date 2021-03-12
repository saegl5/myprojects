import pygame # import the Pygame library of functions
pygame.init() # initialize the game engine

BLUE = pygame.Color("blue") # example
# can also choose your own color
WHITE = pygame.Color("white") # example

size = (704, 512) # (width, height) in pixels
screen = pygame.display.set_mode(size) # set screen size
done = False # define "done"
clock = pygame.time.Clock() # define "clock"
# offset = 0 # initialize offset earlier
y_offset = 0 # initialize offset earlier
    # x_offset = 0 # keep starting position at 10
# increment = 64 # initialize increment early
y_increment = 64
    # x_increment = 64/2
y_0 = 0+y_offset
v_0 = y_increment
t = 0 # initialize
g = 9.80665
# rect_x = 50 # initialize starting x position of the rectangle
# rect_y = 50 # initialize starting y position of the rectangle
# rect_change_x = 1
# rect_change_y = 5 
# # lower number moves rectangle slower, higher moves it faster
# # # negative number changes direction

pygame.display.set_caption("QUESTABOX's Cool Animation") # title, or choose your own
 
while not done: # meaning WHILE True, loop keeps window open
    for event in pygame.event.get(): # check for user input when open window
        if event.type == pygame.QUIT: # user clicked close button
            done = True # change "done" to exit WHILE loop on next loop, loop will not run WHILE False
        else:
            None # continue
    # --- Game logic
    # --------------
    screen.fill(BLUE) # clear the screen
    # offset = 0 # initialize offset
    # while offset <= 448: # loop until offset = 448 (inclusive)
    #     pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # added one offset to one y-coordinate
    #     offset += 64 # offset = offset + 64, if outside loop and relies on mouse, trackpad or keyboard input becomes game logic
    # pygame.draw.rect(screen, WHITE, (0, 0+offset, 64, 64), width=1) # untab
    # pygame.draw.rect(screen, WHITE, (0+x_offset, 0+y_offset, 64, 64), width=1)
    pygame.draw.rect(screen, WHITE, (0, 0+y_offset, 64, 64), width=1)
    pygame.draw.ellipse(screen, WHITE, (0, 0+y_offset, 64, 64), width=1)
    # offset += 64 # untab, if relies on mouse, trackpad or keyboard input becomes game logic
    # offset += increment # allow the increment to change
    # y_offset += y_increment
        # t += 1
        # y_offset = y_0 + v_0*t + 1/2*g*t*t # 0+y_offset = y_offset
        # x_offset += x_increment
    # # if 0+offset + 64 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == size[1]:
    #     # increment *= -1 # increment = increment*-1, that is change the increment's sign
    #     y_increment *= -1
    # # if 0+offset == 0: # if rectangle at top edge
    # if 0+y_offset == 0:
    #     # increment *= -1 # change the increment's sign back
    #     y_increment *= -1
        # if 0+offset + 64 == size[1]: # if rectangle at bottom edge
    # if 0+y_offset + 64 == size[1] or 0+y_offset == 0:
    print(y_offset, y_0, v_0, t)
    if 0+y_offset + 64 >= size[1] and v_0 > 0:# or 0+y_offset == y_0+g*t*t:# or 0+y_offset == 0:
        # y_increment *= -1
        y_0 = 0+y_offset # reset it
        v_0 *= -1 #-1/2*g*t # something wrong!!! (made my own)
        t = 0 # reset it
        y_offset = y_0 + v_0*t + 1/2*g*t*t # 0+y_offset = y_offset
    elif 0+y_offset == y_0+g*t*t and t > 0:
        y_0 = 0+y_offset # reset it
        v_0 *= -1 #-1/2*g*t # something wrong!!! (made my own)
        t = 0 # reset it
        y_offset = y_0 + v_0*t + 1/2*g*t*t # 0+y_offset = y_offset
    else:
        t += 1
        y_offset = y_0 + v_0*t + 1/2*g*t*t # 0+y_offset = y_offset
    
    # if 0+x_offset + 64 == size[0]:
    #     x_increment *= -1
    # if 0+x_offset == 0:
    #     x_increment *= -1
        # if 0+x_offset + 64 == size[0] or 0+x_offset == 0:
        #     x_increment *= -1
        # x_offset += x_increment


    # if increment >= 0:
    #     increment *= 1.25
    # if increment < 0:
    #     increment /= 1.25
    # # if increment == 0:
    #     # increment = 0
    # offset += increment # allow the increment to change
    # # if 0+offset + 64 >= size[1]: # if rectangle at bottom edge
    # #     increment *= -1 # increment = increment*-1, that is change the increment's sign
    # # # if 0+offset == 0: # if rectangle at top edge
    # # if 0+offset <= 0: # if rectangle at top edge
    # #     increment *= -1 # change the increment's sign back
    # if 0+offset + 64 >= size[1] and increment > 0: # if rectangle at bottom edge
    #     increment *= -1 # increment = increment*-1, that is change the increment's sign
    # # if 0+offset == 0: # if rectangle at top edge
    # if 0+offset <= 0 and increment <= 0: if rectangle at top edge
    #     increment *= -1 # change the increment's sign back
    # print("offset=",offset,"increment=",increment)


    # pygame.draw.rect(screen, WHITE, (rect_x, rect_y, 64, 64), width=1)
    # rect_x += rect_change_x
    # rect_y += rect_change_y
    # if rect_y > 448 or rect_y < 0:
    #     rect_change_y = rect_change_y * -1 # bounce off bottom or top edges
    # if rect_x > 640 or rect_x < 0:
    #     rect_change_x = rect_change_x * -1 # bounce off left or right edges
    # ----------------
    pygame.display.flip() # update the screen
    # clock.tick(60) # maximum 60 frames per second (i.e., no more than 60 times through WHILE loop each second)
    clock.tick(10) # so can see rectangle moving
pygame.quit() # formality