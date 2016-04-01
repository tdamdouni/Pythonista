# coding: utf-8

# https://gist.github.com/jsbain/d81f771068229f2e0f9e

import numpy as N
import wave, sound, os, ui

def get_signal_data(frequency=440, duration=1, volume=32767, samplerate=44100):
    """Outputs a numpy array of intensities"""
    samples = duration * samplerate
    period = samplerate / float(frequency)
    omega = N.pi * 2 / period
    t = N.arange(samples, dtype=N.float)
    y = volume * N.sin(t * omega)
    return y

def numpy2string(y):
    """Expects a numpy vector of numbers, outputs a string"""
    signal = "".join((wave.struct.pack('h', item) for item in y))
    # this formats data for wave library, 'h' means data are formatted
    # as short ints
    return signal

class SoundFile:
    '''
    class representing a sound file which will be written'''
    def  __init__(self, signal, filename, duration=1, samplerate=44100):
        self.file = wave.open(filename, 'wb')
        self.signal = signal
        self.sr = samplerate
        self.duration = duration
  
    def write(self):
        self.file.setparams((1, 2, self.sr, self.sr*self.duration, 'NONE', 'noncompressed'))
        # setparams takes a tuple of:
        # nchannels, sampwidth, framerate, nframes, comptype, compname
        self.file.writeframes(self.signal)
        self.file.close()

def playSound(sender,cached=True):
    '''button callback
    interpret button title as frequency. create wav, if cached does not exist
    then play the wav of this note.
    set cached=false to turn off file caching'''
    f=float(sender.title)
    duration=0.5
    samplerate=8000
    file=(os.path.join('notes','{}_{}_{}.wav'.format(sender.title,duration,samplerate) )) if cached else 'note.wav'
    
    if not cached or not os.path.isfile(file): # note caching
        data = get_signal_data(f, duration, samplerate=samplerate)
        signal = numpy2string(data)
        sf = SoundFile(signal, file, duration, samplerate=samplerate)
        sf.write()
    sound.play_effect(file)
    
class GridView(ui.View):
    ''' a class that adds a subview to the end of the existing bounding box
    dir==0  horizontal
    dir==1  verical'''
    def __init__(self,padding=2,dir=0):
        self.padding=padding
        self.dir=dir if dir<2 else 0
    def boundingBox(self):
        '''return bounding box of subviews'''
        try:
            maxx=max([sv.x+sv.width for sv in v.subviews])
            minx=min([sv.x for sv in v.subviews])
        
            maxy=max([sv.y+sv.height for sv in v.subviews])
            miny=min([sv.y for sv in v.subviews])
            return (minx, miny, maxx-minx, maxy-miny)
        except ValueError:
            return (0,0,0,0)
    def addToEnd(self, sv):
        '''add subview sv to right or below existing boundingbox, depending in self.dir'''
        bb=self.boundingBox()

        offset=bb[0+self.dir]+bb[2+self.dir]+self.padding
        if self.dir==0:
            sv.x=offset
        else:
            sv.y=offset
        self.add_subview(sv)

        
def createButt(f,c=0,cached=True):
    '''create a piano button, for frequency f
    c is color, w for white, 1 for black
    black keys are half height'''
    from functools import partial
    colors=[(.9 ,.9, .9), (0,0,0)]
    b=ui.Button()
    b.title='{:3.3f}'.format(f)
    b.width=30
    b.height=150+150*(1-c)
    b.action=partial(playSound,cached=cached)
    b.background_color=b.tint_color=colors[c]
    b.border_color=(1,0,0)
    return b
    
c=[0,1,0,1,0,0,1,0,1,0,1,0] # keycolor index.. starting with C

if __name__ == '__main__':
    import ui,os
    cached=True #i think sound is actually caching anyway, setting to false doesnt work
    if not os.path.isdir('notes'):
        os.mkdir('notes')
    v=GridView(dir=0)
    a=pow(2.0,1.0/12.0)
    f0=440.0
    for n in range(-7,24-7,1): #number of half steps from A440.  start at -7==C
        b=createButt(f0*pow(a,n),c[(7+n)%12],cached)
        v.addToEnd(b)

    v.size_to_fit()
    v.present('panel')