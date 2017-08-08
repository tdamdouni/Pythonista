# Sending OSC messages from Pythonista with pyOSC

_Captured: 2016-11-20 at 23:34 from [shinybit.github.io](http://shinybit.github.io/sending-osc-messages-from-pythonista/)_

**[Open Sound Control** (OSC)](https://en.wikipedia.org/wiki/Open_Sound_Control) is a protocol for communication among computers, electronic music instruments, and various music performance controllers. OSC is optimized for modern networking technologies and is often used as an alternative to [MIDI](https://en.wikipedia.org/wiki/MIDI).

In this post, I'm going to quickly show you how to send OSC messages from **[Pythonista**](http://itunes.apple.com/app/pythonista/id528579881).

## Required modules

The only module we need is **[pyOSC**](https://trac.v2.nl/wiki/pyOSC). It hasn't been updated in years but seems to work fine. You must get it from <https://trac.v2.nl/wiki/pyOSC> because [the one hosted at GitHub](https://github.com/ptone/pyosc) is for Python 3 which isn't supported by Pythonista yet.

Since **pyOSC** consists of a single python file, you can just copy the source code and paste it into a new empty script named `OSC.py`. Better place the script into `site-packages`.

## How to use

Here's a very simple OSC client I wrote in Pythonista and an OSC server running on my desktop computer and listening on port 8000:

Be sure to read `OSC.py` if you want to understand what `addMsgHandler` and `serve_forever` actually do - it's well documented.
