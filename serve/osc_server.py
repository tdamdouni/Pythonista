#!/usr/bin/env python

# https://gist.github.com/shinybit/3d7e0fc7e62887ab48e931af1d4c0986#file-osc_client-py

# http://shinybit.github.io/sending-osc-messages-from-pythonista/

# Get pyOSC here: https://trac.v2.nl/wiki/pyOSC
# The GitHub-hosted version of pyOSC is for Python 3 which isn't supported by Pythonista at the moment

from __future__ import print_function
from OSC import OSCServer

server = OSCServer(("192.168.43.120", 8000))
server.timeout = 0

print("OSC Sever started. Press Ctrl-C to stop.")


def handler(addr, tags, data, client_address):
	s = "Message '%s' from %s: " % (addr, client_address) + str(data)
	print(s)
	
	
def quit_handler(addr, tags, data, client_address):
	print("OSC Server quit.")
	server.close()
	
server.addMsgHandler('/msg/notes', handler)
server.addMsgHandler('/quit', quit_handler)
server.serve_forever()

