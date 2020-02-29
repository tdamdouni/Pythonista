from __future__ import print_function
# https://omz-forums.appspot.com/editorial/post/5842883206709248
# displaying image or matplotlib plot in a imageview ui element

#coding: utf-8

# wxtui
# A simple RGB color mixer with three sliders.

import ui
import clipboard
from random import random
from console import hud_alert
import os
#import re   # str.split(), str.partition(), and `in` replace re for plain text
import console
import matplotlib.pylab as plt
import sys  # for sys.exit()

global endTime, duration, wxt520Time, wxt520Data, nparm, parm

endTime=242
duration=120
wxt520Time=[]
wxt520Data=[]
# interactive wxt520 plot

def get_num(s):
	return float( ''.join( x for x in s if x.isdigit() or x == '.') )
	
def getWxt520Data():
	cwd = os.getcwd()
	print(cwd)
	
	local_files = os.listdir(cwd)  # using 'list' as a variable name is dangerous... 'time' also.
	print(local_files)
	
	# list comprehension, only file ending with '.wxt', case insensitive!
	files = [f for f in local_files if f.upper().endswith('.WXT')]
	if not files:  # deal with no .wxt files found
		sys.exit('No .WXT files found in "{}"!'.format(cwd))
	#for f in list:
	#    if re.match("WXT",f):
	#        files.append(f)
	#print files
	
	f = files[1]  # why the second .WXT file?  files[0] is the first .WXT file.
	#fn = open(f,"r")  # you are not closing this file which leak memory, etc.
	with open(f) as in_file:  # use `with open() as file_handle` which will automatically close()
		lines = in_file.readlines()
		
	date=[]
	time=[]
	count=[]
	data=[]
	for line in lines:
		parts = line.split()  # str.split() is more commonly used than re.split()
		date.append(parts[0])
		time.append(parts[1])
		count.append(parts[2])
		data.append(parts[3])
		
#create dictionary from data   key:index (location of element to plot)
	dict_index2parameter={}
	dict_parameter2index={}
	parts = data[0].split(',')  # str.split() is more commonly used than re.split()
	for i, part in enumerate(parts):  # enumerate counts and separates at the same time
		if '=' in part:  # `in` is more commonly used than re.search()
			q = part.split('=')  # str.partition() is also useful in this instance
			dict_parameter2index[q[0]]=i
			dict_index2parameter[i]=q[0]
			
	print(dict_parameter2index)
	print(dict_index2parameter)
	
# create decimal time
	dtime=[]
	for t in time:
		parts = t.split(':')
		d     = float( parts[0] ) + float( parts[1] )/60. + float( parts[2])/3600.   # decimal time
		dtime.append(d)
	return dtime,data,dict_index2parameter,dict_parameter2index
	
def extractWxt520Parm(data,nparm):

# extract data
#   nparm = 4   # parameter to display
	y = []
	for d in data:
		parts = d.split(',')
		y.append(get_num(parts[nparm]))
	return y
	
def extractWxt520Subinterval(endtime,duration,dtime,parm):
	iend = 60*endtime
	istart = iend - duration
	if istart <0:
		istart = 0;
		iend   = duration
	if iend > 1440:
		iend = 1439
		istart = iend - duration
	x=dtime[istart:iend]
	y=parm[istart:iend]
	return x,y
	
def pltwxt520(x,y):
	plt.grid()
	plt.plot(x,y)
	plt.save("wxt520.png",'PNG')   #??? save the file to disk
#   plt.show()

def button_action(sender):
	global wxt520Data, wxt520Time, nparm, parm
	# Get the root view:
	v = sender.superview
	parm = extractWxt520Parm(wxt520Data, nparm)
	v['label2'].text = 'fn = '+str(nparm)
	x,y = extractWxt520Subinterval(end, dur, wxt520Time, parm)
	pltwxt520(x, y)
	
def button1(sender):
	nparm = 7
	button_action(sender)
	
def button2(sender):
	nparm = 4
	button_action(sender)
	
def button3(sender):
	nparm = 9
	button_action(sender)
	
def slider_action(sender):
	global wxt520Data, wxt520Time,nparm,parm
	# Get the root view:
	v = sender.superview
	# Get the sliders:
	end = int( v['endtime'].value * 24 )
	dur = int ( v['duration'].value * 120 )
	# Create the new color from the slider values:
#   v['view1'].background_color = (r, r*0.1, r*0.23)
	v['label1'].text = 'End Time [h] = {}  Duration [m] = {}'.format(end, dur)  # str.format()
	v['label2'].text = 'fn = '+str(nparm)
#   print end, dur
	x,y = extractWxt520Subinterval(end,dur,wxt520Time,parm)
	pltwxt520(x,y)
#   img = image.load("wxt520.png")                            # ??? I am stuck here, at this point, I have image on console, image on disk but no image in my imageview1 ui element
#   v['imageview1'].image = img #.named("wxt520.png")
	v['imageview1'].image = ui.Image.named('wxt520.png')
	
def main():
	global wxt520Time, wxt520Data, nparm, parm
	
	time, data, dict1, dict2 = getWxt520Data()
	
	nparm=4
	parm = extractWxt520Parm(data,nparm)
	endTime = 24
	duration = 120
	wxt520Time = time
	wxt520Data = data
#   print wxt520Data

	x,y = extractWxt520Subinterval(endTime,duration,time,parm)
#   print x
#   print y
	v = ui.load_view('wxtuiplot')
	slider_action(v['endtime'])
	
	#if ui.get_screen_size()[1] >= 768:
	#    # iPad
	#    v.present('fullscreen')
	#else:
	#    # iPhone
	v.present()  # 'fullscreen' is the default
	
main()

