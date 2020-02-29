#!python2
# coding: utf-8

# http://pastebin.com/vGUaaQfX

# https://forum.omz-software.com/topic/1031/dead-reckoning-script

"""The MIT License (MIT)

Copyright (c) 2014 Andrew Luo luo_andrew a|t yahoo.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""
from __future__ import print_function

def navigate():
	import _motion as motion
	from numpy import zeros, divide
	from math import cos
	from operator import add, sub
	from console import clear
	m = motion.MotionManager()
	m.stop()
	m.start()
	import time
	print("\nStarting motion update, please wait 10 seconds for the values to stabilize. During this time, please avoid touching the phone")
	"""First we start updating, we allow a 5 second time out because there is a significant amount of drift initially present"""
	time.sleep(10)
	print("\nStarting calibration in 10 seconds. Please keep the device UTTERLY still in an position that you expect it to be most commonly in during the measurements later.")
	time.sleep(6)
	print("\nCalibration starting in 5 seconds.")
	time.sleep(5)
	print("\nCalibration starting...")
	caliacc = zeros(3)
	caliangle = zeros(3)
	cali=1
	for u in xrange(300):
		caliacc = caliacc + m.user_acceleration
		caliangle = caliangle + m.rotation_rate
	zeroingacc= divide(caliacc, 300)
	zeroingang=divide(caliangle, 300)
	print("\nCalibration ended, you may start to move in 5 seconds.")
	time.sleep(5)
	zeroingacc0=zeroingacc[0]
	zeroingacc1=zeroingacc[1]
	zeroingacc2=zeroingacc[2]
	zeroingang0=zeroingang[0]
	zeroingang1=zeroingang[1]
	zeroingang2=zeroingang[2]
	speed0=0
	speed1=0
	speed2=0
	angle0=0
	angle1=0
	angle2=0
	movement0=0
	movement1=0
	movement2=0
	time2=0.083 #You need to change this number to make it work on your device, just replace the while loop and timeit
	time1=time2*9.83
	"""Apparently for small lists, direct assignment is twice as fast as map and lists! Very unexpected!"""
	while 1:
		cos0=cos(angle0)
		cos1=cos(angle1)
		cos2=cos(angle2)
		speed0 += (-zeroingacc0 + m.user_acceleration[0]) * time1*cos0*cos2
		speed1 += (-zeroingacc1 + m.user_acceleration[1]) * time1*cos1*cos2
		speed2 += (-zeroingacc2 + m.user_acceleration[2]) * time1*cos0*cos1
		angle0 += (m.rotation_rate[0]-zeroingang0) * time2
		angle1 += (m.rotation_rate[1]-zeroingang1)* time2
		angle2 += (m.rotation_rate[2]-zeroingang2)* time2
		movement0 = movement0+speed0*time2*cos0*cos2
		movement1 = movement1+speed1*time2*cos1*cos2
		movement2 = movement2+speed2*time2*cos0*cos1
		#speed = map(lambda x, y: time*add(x, y), speed, map(sub, list(m.user_acceleration), zeroingacc))
		#angle = map(add, angle, list(m.rotation_rate))
		#movement = map(lambda x,y: time*add(x,y), movement, map(lambda l, o: l*o, map(cos, angle), speed))
		print(movement0, movement1, movement2)
		clear()
navigate()

