"""
Description
"""

import pygame
import src.canvas as canvas, src.efficiency as efficiency
# Other modules to import

pygame.display.set_caption("Title")

# Other initialization/constants/variables/settings

while True:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            canvas.close()
    
        # Keyboard events
        
        efficiency.snapshot(action) # optional
    
    # Game logic
    
    canvas.clean()

    # Drawing code

    canvas.show()
    efficiency.activate() # optional