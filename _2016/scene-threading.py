# https://gist.github.com/jsbain/4ea25e2c88579efd030319e920466a0b

# https://forum.omz-software.com/topic/3702/return-from-run-scene/2

import ui,scene,threading
e=threading.Event()
class SceneContainer(ui.View):
	def __init__(self,scn,*args,**kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self.sv=scene.SceneView()
		self.sv.scene=scn
		self.scene=scn
		self.scene.error=False
		self.add_subview(self.sv)
	def will_close(self):
		#since scene.stop is not called!!!
		self.sv.scene.stop()
		e.set()
class MyScene(scene.Scene):
	def setup(self):
		self.l=scene.LabelNode()
	
		self.add_child(self.l)
		self.l.text='Hello'
		self.l.position=(100,100)
		self.till=0
		self.simtime=0
		self.running=False
		self.error=False
	def update(self):
		try:
			if not self.view.on_screen:
				raise Exception('scene was closed')
			if self.running:
				self.simtime += self.dt
				if self.simtime <= self.till:
					self.l.text='%2f'%(self.simtime)
				else:
					e.set()
					self.running=False
					self.starttime=-1
		except:
			self.error=True
			self.running=False
			e.set()
			raise
	def pause(self):
		print('pausing')
		self.running=False
		self.error=True
		e.set()
	def stop(self):
		print('stopping')
		self.running=False
		self.error=True
		e.set()
v=SceneContainer(MyScene(),frame=(0,0,500,500))
v.present('sheet')

def burpscene(till):
	if v.scene.error:
		raise Exception('scene was stopped')
	if v.on_screen:
		v.scene.till=till
		v.scene.running=True
		e.wait()
		print('scene now at ',till)
		e.clear()
	else:
		raise Exception('scene was stopped')


#example
burpscene(2)
v.scene.l.color=(1,1,0)
burpscene(4)
v.scene.l.color=(1,0,0)
burpscene(6)
