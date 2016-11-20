# https://forum.omz-software.com/topic/3482/share-running-code-from-clipboard

import clipboard
import runpy

# Every line of the copied script
cliplines = clipboard.get().split('\n')

# Some scripts contain the 'if __name__ == "__main__":' statement
# We can't have that since we need the script to run when it's imported
try:
	cliplines[cliplines.index("if __name__ == '__main__':")] = "if __name__ != '__main__':"
except ValueError:
	pass
	
	
# @Phuket2 keeps importing editor without using it
# Since editor is not supported in the app extension...
# We try to remove it and see if it still works
for i in range(len(cliplines)):
	cliplines[i] = (cliplines[i].replace('import editor', '').replace(', editor', '') + '\n').encode()
	
# Writing the new script to the .py file
with open('TheScript.py', 'wb') as f:
	f.writelines(cliplines)
	
# Run the script
runpy.run_path('TheScript.py')

import clipboard
import runpy

# Every line of the copied script
cliplines = clipboard.get().split('\n')

# Some scripts contain the 'if __name__ == "__main__":' statement
# We can't have that since we need the script to run when it's imported
try:
	cliplines[cliplines.index("if __name__ == '__main__':")] = "if __name__ != '__main__':"
except ValueError:
	pass
	
	
# @Phuket2 keeps importing editor without using it
# Since editor is not supported in the app extension...
# We try to remove it and see if it still works
for i in range(len(cliplines)):
	cliplines[i] = (cliplines[i].replace('import editor', '').replace(', editor', '') + '\n').encode()
	
# Writing the new script to the .py file
with open('TheScript.py', 'wb') as f:
	f.writelines(cliplines)
	
# Run the script
runpy.run_path('TheScript.py')

# --------------------

# Here's some random code to test it on

from math import pi
from ui import View, TextView


# Just a pointless function
def changeText(sender, text):
	sender.text = text
	
v = View()
v.bg_color = 'white'
v.frame = (0, 0, 400, 100)

l = TextView()
l.alignment = 1
l.editable = False
l.frame = (0, 0, len(str(pi)) * 20, 96)
l.font = ('CourierNewPSMT', 32)

changeText(l, 'Pi\n' + str(pi))

if __name__ == '__main__':
	v.present('sheet')
	
l.x = v.width/2 - l.width/2
l.y = v.height/2 - l.height/2
v.add_subview(l)

