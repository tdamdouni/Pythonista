# coding: utf-8

# https://gist.github.com/nriley/b96db3ac6baa452de45f9f4e0cc9086d

# https://twitter.com/nriley/status/759805009106243584

## Why?

# There's no easy way to trigger a HomeKit scene from a URL scheme.  You could build your own non-App Store iOS app, or decide it might be more fun to play with Pythonista, as I did.

## How to use

# You'll need [homebridge](https://github.com/nfarina/homebridge) and [homebridge-websocket](https://github.com/cflurin/homebridge-websocket) set up.

# I use the following in my `~/.homebridge/config.json`:

#```
#    "platforms": [
#[...]
#{
#            "platform": "websocket",
#            "name": "WebSockets",
#            "port": 4050
#        }
#    ]
#```

# Then install Pythonista 3, [StaSh](https://github.com/ywangd/stash) and `pip install websockets` (the asynchronous WebSockets library [here](https://websockets.readthedocs.io/)) from StaSh.

# Copy `switch.py` to Pythonista.  Change the hostname at the top.  Run it and you'll get prompted for the name of a switch to create. You can bind a separate action to the switch being turned on and off.

# Create a rule/action which triggers your scene whenever the fake switch is turned on or off.  Most advanced HomeKit apps will let you do this; Eve and Hesperus are the best free ones I've used.

# Then trigger your URL.  I use Launch Center Pro as follows:

# ``pythonista3://switch.py?action=run&argv=«switch name»&argv=«true/false/flip»&argv={{«URL to chain»}}``

# The 3rd argument gives you ``x-callback-url`` style behavior.

# You can also run the script from a Mac or other computer with Python 3.5 on it.

# Note that the action will only trigger when the switch "position" changes; if it's already on and you turn it on, nothing happens.  To work around this, you can pass `flip` instead of `true` or `false` and the switch will be turned off then immediately on; this should mean that your scene will always be triggered.

import asyncio
import json
import sys
import webbrowser
import websockets

def homebridge_websocket():
  return websockets.connect('ws://mary.local:4050')

async def add():
  async with homebridge_websocket() as websocket:
    name = input("Switch to create? ")
    request = dict(topic='add',
                   payload=dict(name=name, service='Switch'))
    await websocket.send(json.dumps(request))
    print("> {}".format(request))
    ack = await websocket.recv()
    print("< {}".format(ack))

async def get(name):
  async with homebridge_websocket() as websocket:
    request = dict(topic='get', payload=dict(name=name))
    await websocket.send(json.dumps(request))
    print("> {}".format(request))
    ack = await websocket.recv()
    print("< {}".format(ack))

async def setValue(name, value, callback_url=None):
  async with homebridge_websocket() as websocket:
    value = value.lower()
    if value == 'flip':
      await setValue(name, 'off')
      await setValue(name, 'on', callback_url)
      return
    value = value in ('on', 'true', '1')
    request = dict(topic='setValue',
                   payload=dict(name=name,
                                characteristic='On',
                                value=value))
    await websocket.send(json.dumps(request))
    print("> {}".format(request))
    try:
      error = await asyncio.wait_for(websocket.recv(),
                                     timeout=0.1)
    except:
      # there's no ack on success (seriously!)
      # so we have to use a timeout instead
      if callback_url:
        webbrowser.open(callback_url)
    else:
      print("< {}".format(ack))

if __name__ == '__main__':
  if len(sys.argv) == 1:
    action = add
  elif len(sys.argv) == 2:
    action = lambda: get(sys.argv[1])
  elif len(sys.argv) in (3, 4):
    action = lambda: setValue(*sys.argv[1:])
  else:
    print('Wrong number of arguments', file=sys.stderr)
    sys.exit(1)

  event_loop = asyncio.get_event_loop()
  event_loop.run_until_complete(action())
