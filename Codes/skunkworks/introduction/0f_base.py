"""
Base Module
"""

import pygame
import src.canvas as canvas
import custom.classes as c # sprites only
# Other modules to import

pygame.display.set_caption("Canvas")

# Other initialization/constants/variables/settings

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
    
        # Mouse/trackpad or keyboard events
            
    # Game logic
    
    canvas.clean()

    # Drawing code

    canvas.show()