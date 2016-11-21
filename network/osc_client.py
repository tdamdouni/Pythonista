#!/usr/bin/env python

# http://shinybit.github.io/sending-osc-messages-from-pythonista/

# https://gist.github.com/shinybit/3d7e0fc7e62887ab48e931af1d4c0986

# Get pyOSC here: https://trac.v2.nl/wiki/pyOSC
# The GitHub-hosted version of pyOSC is for Python 3 which isn't supported by Pythonista at the moment
from OSC import OSCClient, OSCMessage

client = OSCClient()
client.connect(("192.168.43.120", 8000))

msg = OSCMessage("/msg/notes")
msg.append([50, 60])
client.send(msg)

msg.clearData();
msg.append(["C3", 127])
client.send(msg)

client.send(OSCMessage("/quit"))

