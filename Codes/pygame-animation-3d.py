# Import Blender Game Engine (WIP)
import bge
 
# Get a reference to the blue object
cont = bge.logic.getCurrentController()
blue_object = cont.owner
 
# Print the x,y coordinates where the blue object is
print(blue_object.position[0], blue_object.position[1] )
 
# Change x,y coordinates according to x_change and
# y_change. x_change and y_change are game properties
# associated with the blue object.
blue_object.position[0] += blue_object["x_change"]
blue_object.position[1] += blue_object["y_change"]
 
# Check to see of the object has gone to the edge.
# If so reverse direction. Do so with all 4 edges.
if blue_object.position[0] > 6 and blue_object["x_change"] > 0:
    blue_object["x_change"] *= -1
 
elif blue_object.position[0] < -6 and blue_object["x_change"] < 0:
    blue_object["x_change"] *= -1
 
elif blue_object.position[1] > 6 and blue_object["y_change"] > 0:
    blue_object["y_change"] *= -1
 
elif blue_object.position[1] < -6 and blue_object["y_change"] < 0:
    blue_object["y_change"] *= -1