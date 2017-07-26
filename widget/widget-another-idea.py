# https://forum.omz-software.com/topic/3869/unable-to-load-in-notification-center/6

import appex
import requests
import ui
from objc_util import ObjCClass

l = 0

device = ObjCClass('UIDevice').currentDevice()
device.setBatteryMonitoringEnabled_(True)
battery_percent = device.batteryLevel() * 100
device.setBatteryMonitoringEnabled_(False)
off = True
hum = 0
tem = 0
url = 'http://www.apple.com/#'  # Added url definition


# Do not worry about this, this changes my lights but will disable if I'm not
# at home
def button_tapped(sender):
	global l
	l += {'+': 10, '-': -10}.get(sender.name, 0)
	l = min(max(l, 0), 100)
	print('{}: {}'.format(l, requests.get(url + str(l)).text))
	
response = requests.get(url)
tem = response.text if response.status_code == 200 else '  -- '
info = html = response.text


def main():
	label = ui.View(frame=(0, 0, 320, 64))
	helv_15 = ('HelveticaNeue-Light', 15)
	# TEMPERATURE
	label.add_subview(ui.Label(frame=(1, 0, 100, 0), flex='wh', font=helv_15,
	text_color='white', alignment=ui.ALIGN_LEFT,
	text='Temperature:' + str(info)[3:7] + '°'))
	# HUMIDITY
	label.add_subview(ui.Label(frame=(1, 0, 150, 32), flex='wh', font=helv_15,
	text_color='white', alignment=ui.ALIGN_LEFT,
	text='Humidity:' + str(info)[11:13] + '%'))
	
	# LIVING ROOM LIGHTS
	monla_15 = ('Monla', 15)
	living_title = ui.Label(frame=(320 - 135, 0, 130, -20), flex='wh',
	font=monla_15, alignment=ui.ALIGN_RIGHT,
	text_color='white', text='Living Room Lights')
	
	# GREETING (WIP)
	greet = 'hi'
	
	# LIVING ROOM BUTTONS
	plus_btn = ui.Button(name='+', image=ui.Image('iow:ios7_plus_outline_32'),
	flex='hl', tint_color='#666', action=button_tapped)
	plus_btn.frame = (320 - 64, 0, 64, 64)
	
	minus_btn = ui.Button(name='-', image=ui.Image('iow:ios7_minus_outline_32'),
	flex='hl', tint_color='#666', action=button_tapped)
	minus_btn.frame = (320 - 64, 0, -64, 64)
	if tem != '  -- ':
		label.add_subview(minus_btn)
		label.add_subview(plus_btn)
		label.add_subview(living_title)
	else:
		# GREETING
		label.add_subview(ui.Label(frame=(320 - 135, 0, 130, -20), flex='wh',
		text_color='white', font=monla_15,
		alignment=ui.ALIGN_RIGHT, text=greet))
	# BATTERY
	if battery_percent >= 85:
		img = 'full'
	elif battery_percent >= 50:
		img = 'half'
	elif battery_percent >= 30:
		img = 'low'
	else:
		img = 'empty'
	bat = ui.Button(name='batteryl', flex='hl', tint_color='#00d500',
	image=ui.Image('iow:battery_{}_24'.format(img)),
	action=button_tapped)
	bat.frame = (320 - 30, 64, 32, 32)
	label.add_subview(bat)
	
	# BACKGROUND COLOR
	label.background_color = '#1a1a1a'
	
	# SETS WIDGET
	appex.set_widget_view(label)
	
if __name__ == '__main__':
	main()

