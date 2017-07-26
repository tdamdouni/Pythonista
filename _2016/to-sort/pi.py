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


