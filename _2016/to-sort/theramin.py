#!/bin/env python

# https://github.com/jsbain/theraminsim

"""pythonista therminsim - a simple theramin style simulator

y axis: frequency
x axis: volume

multitouch works, but best if ios gestures are disabled

in retrospect, should have one audio thread, and feed a list of freq/vols for the different fingers, rather than run multiple threads


Inspired by http://ptheremin.sourceforge.net, but completely rewritten for numpy/pythonista.
"""

import numpy
import threading
import time
import wave
import tempfile
import sound
import ui
import console
#set min and max frequencies (hz)
fmin=150.0
fmax=1600.0

class PlaybackThread(threading.Thread):
    """A thread that continually generates audio."""

    def __init__(self, name, dt):
        #self.name = name
        self.f={}
        self.vollist={}
        self.fs = 2*11050.0 # the sample frequency
        #self.ft = fmin # the tone frequency of the instrument
        self.vol = 1  #0-1

        # setup ping pong file/players
        self.filelist = [tempfile.NamedTemporaryFile(),
                         tempfile.NamedTemporaryFile()]
        #
        self.alive = True    

        self.dt = dt #update interval
        self.idx = 0 # which buffer are we writing to
        self.t = numpy.linspace(0,self.dt,numpy.round(self.dt*self.fs))  
        threading.Thread.__init__(self, name=name)
        
    def run(self):
        def tone_gen():            
            """Generate approximately dt's worth of tone.  attempts to Start/stop when signal is near zero, to avoid glitches.  this doesnt really work"""
            #foolish overoptimization
            f=self.f
            dt = self.dt
            fs = self.fs
            sin = numpy.sin
            floor=numpy.floor
            y=numpy.zeros_like(self.t)
            for ft,vol in f.values():
                y+=(vol*sin(2*numpy.pi*ft*self.t))
            #scale so we dont compress
            scaling=1.0/max([max(y), 1.0])
            return (128+127*y*scaling).astype('u1').tostring()
        def gen_file(file):
            tone=tone_gen()
            file.seek(0,0)
            wf=wave.open(file,'w')
            wf.setparams((1, 1, self.fs, 0, 'NONE', 'not compressed'))
            wf.writeframes(tone)
            wf.close()
        
        # to optimize loop performance, dereference everything ahead of time
        
        filelist = self.filelist
        playerlist = [None,None ]
        idx = self.idx
        dt = self.dt

        gen_file(filelist[idx])
        playerlist[idx] = sound.Player(filelist[idx].name)

        tic = time.time
        while self.alive:
            t0=tic()
            #1) play
            playerlist[idx].play()
            idx = (idx+1)%2
            #2) generate
            gen_file(filelist[idx])
            #3) load
            p=playerlist[idx] = sound.Player(filelist[idx].name)
            #4) sleep
            try:
               #we want to sleep just long enough to start next player
               # this is trial and error....
               time.sleep(0.99*(t0+dt-tic()))
               #time.sleep((p.duration-p.current_time)*0.5)
            except:
                pass
        self.cleanup()
    def addtone(self,key,f,vol):
        self.f[key]=f,vol
    def deltone(self,key):
        try:          
             del(self.f[key])
        except KeyError:
            pass
    def cleanup(self):
        try:
            [x.close() for x in self.filelist]
        except:
            pass
            
    def stop(self):
        self.alive = False

    def set_new_freq(self, freq, vol):
        """Updates the input frequency."""
        self.ft = freq
        self.vol = vol

    def get_wav_data(self):
        return self.recording

    def clear_wav_data(self):
        self.recording = []

class Theramin(ui.View):
    '''multitouch enabled realtime sound generation'''
    def __init__(self,dt):
        self.t={}   #threads
        self.dt=dt  #update interval
        self.t=PlaybackThread(name="test",dt=self.dt)
        self.t.start()
    def touch_began(self,touch):
        (x,y)=touch.location
        self.setfreq(touch.touch_id,y/self.height,x/self.width)
    def touch_moved(self,touch):
        (x,y)=touch.location
        self.setfreq(touch.touch_id,y/self.height,x/self.width)
    def touch_ended(self,touch):
        self.t.deltone(touch.touch_id)

    def setfreq(self,touch_id,freq,vol):
        freq=fmin+(fmax-fmin)*(1-freq)
        self.t.addtone(touch_id,freq,vol)
    def will_close(self):
        try:
                self.t.stop()
        except:
                pass
if __name__ == '__main__':
    v=Theramin(0.11)
    v.present()
    console.hud_alert('turn off ios gestures. use fingers to make sounds.pitch=vert, vol=horiz',duration=5.0)