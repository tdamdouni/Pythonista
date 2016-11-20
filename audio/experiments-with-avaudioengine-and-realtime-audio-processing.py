# https://gist.github.com/jsbain/2cf4998949f49b58ff284239784e1561

# https://forum.omz-software.com/topic/3265/experiments-with-avaudioengine-and-realtime-audio-processing

from objc_util import *
import ctypes
import numpy as np
import matplotlib.image
import io,ui
AVAudioEngine=ObjCClass('AVAudioEngine')
AVAudioSession=ObjCClass('AVAudioSession')
def setup():
	error=ctypes.c_void_p(0)
	session=AVAudioSession.sharedInstance()
	category=session.setCategory('AVAudioSessionCategoryPlayAndRecord',error=ctypes.pointer(error))
	if error:
		raise Exception('error setting up category')
	session.setActive(True, error=ctypes.pointer(error))
	if error:
		raise Exception('error setting up session active')
	engine=AVAudioEngine.new()
	return engine
	
class fftview(ui.View):
	def __init__(self,*args,**kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self.i=ui.ImageView()
		self.i.frame=self.bounds
		self.i.flex='wh'
		self.add_subview(self.i)
		self.fps=ui.Label()
		self.add_subview(self.fps)
		self.fps.text=''
	def update(self,im):
		self.i.image=im
	@ui.in_background
	def will_close(self):
		print('stopping engine')
		engine.pause()
v=fftview(frame=(0,0,500,500))

'''setup a tap block'''
buf=[] #for debugging
bIO=io.BytesIO()
lastt=0
def processBuffer(self,buffer,when, cmd):
	global buf, lastt
	buf=ObjCInstance(buffer )
	t=ObjCInstance(when).sampleTime()/44100.
	fps=1./(t-lastt)
	lastt=t
	v.fps.text='fps{}'.format(fps)
	A=np.ctypeslib.as_array(buf.floatChannelData()[0],(128,128))
	B=np.transpose(np.log10(np.fft.fftshift(abs(np.fft.fft(A,512)))))
	matplotlib.image.imsave(bIO,B,format='png',vmin=-3,vmax=1)
	v.update(ui.Image.from_data(bIO.getvalue()))
	bIO.seek(0)
process_block=ObjCBlock(processBuffer,restype=None,argtypes=[c_void_p,c_void_p,c_void_p,c_void_p])

'''set up audio engine, and install tap, and start'''
engine=setup()
engine.connect_to_format_(engine.inputNode(),
                                                                        engine.outputNode(),
                                                                        engine.inputNode().inputFormatForBus_(0))

engine.inputNode().installTapOnBus(0,
                                        bufferSize=64*256,
                                        format=None,
                                        block=process_block)

v.present('sheet')
engine.startAndReturnError_(None)

