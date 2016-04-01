from visual.text import *

print("""
This early 3D text machinery is limited to rather crude uppercase letters.
It has been superceded by the text object introduced in Visual 5.3.
""")

# Display extruded text (uppercase only at present)
# By default, display text along x axis, with letters pointing up parallel to y axis
# Bruce Sherwood, Carnegie Mellon University, begun March 2000

# Example with default values:
#  text(pos=(0,0,0), axis=(1,0,0), string='ABC',
#    height=1, depth=0, width=1,
#    color=currentdisplay.foreground, up=(0,1,0.3))
# axis is direction along which text advances
# if width not specified, it is the same as height
# depth is measured forward from pos
# Only numbers and uppercase letters at present: others display as '*'

scene.title = "3D Text"
scene.fov = 0.001
scene.range = 7
text(pos=(0,3,0), string='ABC', color=color.red, depth=0.3, justify='center')
text(pos=(0,-3,0), string='DEF', color=color.blue, depth=0.3, justify='center')
message = text(pos=(0,0,0), string='CLICK TO CHANGE THIS', justify='center',
               color=color.yellow, axis=(1,0,1),
                depth=0.3, up=(0,1,-0.3))
scene.mouse.getclick()
message.reshape(color=color.cyan, height=2)
