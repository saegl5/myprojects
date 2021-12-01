"""
Description
"""

import pygame
import src.frame as frame
import src.canvas as canvas
import src.efficiency as efficiency
# Other imports

pygame.display.set_caption("Title")

# Other constants/variables/settings

while True:
    for action in pygame.event.get():
        frame.open(action)
    
        # Keyboard events
        
        efficiency.snapshot(action) # optional
    
    # Game logic
    
    canvas.clean()

    # Drawing code

    canvas.show()
    efficiency.activate() # optional