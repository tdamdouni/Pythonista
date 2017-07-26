# https://forum.omz-software.com/topic/3869/unable-to-load-in-notification-center/6

import urllib.request,ui,appex
l=0
from objc_util import *
UIDevice = ObjCClass('UIDevice')
device = UIDevice.currentDevice()
device.setBatteryMonitoringEnabled_(True)
battery_percent = device.batteryLevel() * 100
off=True
hum=0
tem=0
url = 'http://www.apple.com/#'  # Added url definition
#Do not worry about this, this changes my lights but will disable if I'm not at home
def button_tapped(sender):
	global l
	if sender.name =='+':
		l+=10
	if sender.name =='-':
		l+=-10
	with urllib.request.urlopen(url + str(l) ) as response:  # Added use of url
		if l>100:
			l=100
		if l<0:
			l=0
		print(str(l))
		
# Checks if I'm at home, still doesn't work if I take this out
req = urllib.request.Request(url)  # Added use of url
try: urllib.request.urlopen(req)
except urllib.error.URLError :
	tem = '  -- '
	
with urllib.request.urlopen(url) as response:  # Added use of url
	html = response.read()
	info = html
	
	
	
def main():
	label = ui.View(frame=(0, 0, 320, 64))
	# TEMPERATURE
	t = ui.Label(frame=(1, 0, 100, 0), flex='wh',text_color='white', font=('HelveticaNeue-Light', 15), alignment=ui.ALIGN_LEFT, text = 'Temperature:' + str(info)[3:7] + 'Â°')
	label.add_subview(t)
	# HUMIDITY
	h = ui.Label(frame=(1,0,150,32),flex='wh', text_color='white',font=('HelveticaNeue-Light',15), alignment=ui.ALIGN_LEFT, text = 'Humidity:'+str(info)[11:13] + '%')
	label.add_subview(h)
	
	# LIVING ROOM LIGHTS
	living_title = ui.Label(frame=(320-135,0,130,-20),flex='wh',text_color='white', font=('Monla',15), alignment=ui.ALIGN_RIGHT, text = 'Living Room Lights')
	
	# GREETING (WIP)
	greet='hi'
	
	
	# LIVING ROOM BUTTONS
	plus_btn = ui.Button(name='+', image=ui.Image('iow:ios7_plus_outline_32'), flex='hl', tint_color='#666', action=button_tapped)
	plus_btn.frame = (320-64, 0, 64, 64)
	
	minus_btn = ui.Button(name='-',         image=ui.Image('iow:ios7_minus_outline_32'), flex='hl', tint_color='#666', action=button_tapped)
	minus_btn.frame = (320-64 ,0, -64,64)
	if tem!='  -- ':
		label.add_subview(minus_btn)
		label.add_subview(plus_btn)
		label.add_subview(living_title)
	else:
		# GREETING
		greeting = ui.Label(frame=(320-135,0,130,-20),flex='wh',text_color='white', font=('Monla',15), alignment=ui.ALIGN_RIGHT, text = greet)
		#label.add_subview(greeting)
		
	# BATTERY
	if battery_percent>=85:
		img='iow:battery_full_24'
	if battery_percent<85 and battery_percent>=50:
		img='iow:battery_half_24'
	if battery_percent<50 and battery_percent>=30:
		img='iow:battery_low_24'
	elif battery_percent<30:
		img='iow:battery_empty_24'
	bat = ui.Button(name='batteryl', image=ui.Image(img),flex='hl',tint_color='#00d500',action=button_tapped)
	bat.frame = (320-30,64,32,32)
	label.add_subview(bat)
	
	
	# BACKGROUND COLOR
	label.background_color = '#1a1a1a'
	
	# SETS WIDGET
	appex.set_widget_view(label)
	
if __name__ == '__main__':
	main()
