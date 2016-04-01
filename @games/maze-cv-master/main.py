from CV import *
from pathfinding import *
from sys import platform

if platform == 'iphoneos':
	#Script is running in Pythonista
	from App import App
else:
	#Script is running on desktop
	from PIL import Image
	img = Image.open('Test Images/photo2.jpg')
	mazeGen.finalScan(img.resize((320,240))).resize((500,500)).show()
