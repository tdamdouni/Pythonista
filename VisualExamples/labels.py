from visual import *

x = arrow( color=color.red)

tip = label( text="tip", space=0.2, pos=(1,0), opacity=0.5)
tail = label( text="tail", xoffset=20, yoffset=10, opacity=0.5)
midp = label( text="a\nmidpoint", xoffset=10, yoffset=20, pos=(.5,0), opacity=0.5)

print("""You should see a single arrow with three labels attached to it.
Each label is translucent. The one at the tip should be centered at
the tip. The head and tail labels have a single line of text.
The midpoint label has two.""")
