# coding: utf-8

# https://forum.omz-software.com/topic/3222/range-error

import socket
import subprocess
import sys
from datetime import datetime

# Ask for input
remoteServer = raw_input("Enter a remote host to scan:")
remoteServerIP = socket.gethostbyname(remoteServer)

# Print a nice banner
print "-" * 60
print "Please wait, scanning host",remoteServerIP
print "-" * 60

# Check what time scan started
t1 = datetime.now()

# Using range function to specify ports
for port in range(): (range(1,1025))
sock = socket.socket(socket.AF_INET, SOCK_STREAM)
result = sock.connect_EX((remoteServerIP,port))
if result == 0:
	print "port {}: Open".format(port)
sock.close()

# Checking time again
t2 = datetime.now()

# Calculate time difference
total = t2 - t1

# printing
print 'Scanning Completed in', total

# --------------------

for port in range(1, 1025)

# --------------------

