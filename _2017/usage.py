# https://gist.github.com/zrzka/8b83d3f8cb998e185c482b3d5b116267

import external_screen as es
import ui
import logging

red_view = ui.View()
red_view.background_color = 'red'

def connected():
	print('Screen connected, lets display red_view again')
	es.present(red_view)

def disconnected():
	print('Ouch, screen disconnected')

es.init(log_level=logging.DEBUG)
es.present(red_view)
es.register_connected_handler(connected)
es.register_disconnected_handler(disconnected)

try:
	while True:
		pass
except KeyboardInterrupt:
	es.terminate()
	pass
