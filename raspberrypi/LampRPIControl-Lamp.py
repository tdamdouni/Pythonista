# coding: utf-8
# Samuel LIU (hitwaterfish@gmail.com)
# 20140730
# lamp control client run on iPhone
import ui
import socket   #for sockets
import sys  #for exit
from console import hud_alert

def lampon_action(sender):
#Send some data to remote server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('192.168.1.200' , 8888))
	message = "led1 on"
	s.sendall(message)
	s.close()
	#print 'Message send successfully'	
	hud_alert('Turned On')

def lampoff_action(sender):
#Send some data to remote server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('192.168.1.200' , 8888))
	message = "led1 off"
	s.sendall(message)
	s.close()
	#print 'Message send successfully'	
	hud_alert('Turned Off')

v = ui.load_view('lamp')
if ui.get_screen_size()[1] >= 768:
# iPad
	v.present('popover')
else:
# iPhone
	v.present()