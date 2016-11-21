# https://gist.github.com/jsbain/33d90edb232d8e825a8461c7aba23b95

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
import time

'''setup a tap block'''
buf=[] #for debugging
bIO=io.BytesIO()
lastt=0
timing=np.zeros((100))

def processBuffer(self,buffer,when, cmd):
	try:
		global lastt
		global timing
		#global buf
		timing[0]=time.time()
		buf=ObjCInstance(buffer )
		t=ObjCInstance(when).sampleTime()/44100.
		timing[1]=time.time()
		fps=1./(t-lastt)
		lastt=t	
		v.fps.text='fps{}'.format(fps)
		timing[2]=time.time()
		A=np.ctypeslib.as_array(buf.floatChannelData()[0],(4,4096))
		timing[3]=time.time()
		A=A-A.mean()
		#B=np.transpose(np.log10(np.fft.fftshift(abs(np.fft.fft(A,32)))))
		timing[4]=time.time()
		matplotlib.image.imsave(bIO,A+1,format='png',
							cmap=(matplotlib.image.cm.get_cmap('gray',256)), 
							vmax=2.,vmin=0.)
		timing[5]=time.time()
		#v.update(ui.Image.from_data(bIO.getvalue()))
		m.update_data(ui.Image.from_data(bIO.getvalue()))
		timing[6]=time.time()
		bIO.seek(0)
		#buf.autorelease()
	except:
		engine.pause()
		raise

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

#v.present('sheet')
engine.prepare()

from scene import *
''' 16384 samples/44100 samp/sec=0.3715 sec per window
due to tex suze limits of 4096, we size as a 4x4096

if we scale u and t such that they are both 1 at max, 
then scale by screen width as W*x+(1-W)*t, we get an offset
into the texture.

We then convert this into a u,v coords by multiplying by number of rows, then taking mod and fract

'''
ripple_shader = '''
precision highp float;
varying vec2 v_tex_coord;
// These uniforms are set automatically:
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
// This uniform is set in response to touch events:
uniform float u_oldtime;
uniform sampler2D u_data;
void main(void) {
	vec2 uv=v_tex_coord.xy;
	float t = (u_time - u_oldtime)/0.371519/1.;
	float W=0.2;//fraction of total buffer to show on screen at once,
	float N=4.;//num rows in texture
	float shft =N*(W*uv.x + (1.-W)*t);
	float u = mod(shft ,1.);
	float v =  floor(shft)+1./N;
	float y = texture2D(u_data, vec2(u,v)).x;
	float dy=1./67.;
	float col = smoothstep(-dy,0.,uv.y-y)-smoothstep(0.,dy,uv.y-y);
    gl_FragColor = vec4(col/2.,col,col/2.,1.);
}
'''


class MyScene (Scene):
	def setup(self):
			b=io.BytesIO()
			matplotlib.image.imsave(b,(np.zeros((320,768),float)),format='png')
			self.sprite=SpriteNode(Texture(ui.Image.from_data(b.getvalue())),
							parent=self)
			self.sprite.shader = Shader(ripple_shader)
			self.did_change_size()
	def stop(self):
		engine.pause()
	def update(self):
		pass
	def did_change_size(self):
			# Center the image:
			self.sprite.position = self.size/2
	
	def update_data(self,i):
		txt=Texture(i)
		self.sprite.shader.set_uniform('u_data',txt)
		oldtime=self.sprite.shader.get_uniform('u_time')
		self.sprite.shader.set_uniform('u_oldtime',oldtime)

m=MyScene()

run(m,show_fps=True,frame_interval=2,anti_alias=True)
engine.startAndReturnError_(None)
