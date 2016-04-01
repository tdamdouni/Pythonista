'''Multi-touch particle generator'''

import sk

texture = sk.Texture('shp:Spark')
# The birth rate determines how many particles are emitted per second - if the animation stutters on your device, try reducing this number, on the latest-generation hardware, you may be able to increase it:
birth_rate = 750

# Load the emitter 'template' from the scene file:
emitter_tpl = sk.load('ParticlePaint.pysk')['emitter'][0]
emitter_tpl.p_birth_rate = 0

class ParticleScene (sk.Scene):
	def __init__(self):
		self.emitters = {}
		self.instructions = sk.LabelNode()
		self.instructions.text = 'Touch to create particles.'
		self.instructions.font_size = 30
		self.instructions_visible = True
		self.add_child(self.instructions)
		self.did_change_size(None)
	
	def did_change_size(self, old_size):
		self.instructions.position = self.size.w/2, self.size.h/2
	
	def touch_began(self, node, touch):
		if self.instructions_visible:
			self.instructions.run_action(sk.fade_out(2.0))
			self.instructions_visible = False
		e = emitter_tpl.__copy__()
		e.target_node = self
		e.position = touch.location
		self.emitters[touch.touch_id] = e
		# To keep the framerate consistent with multiple touches, divide the total particle birthrate by the number of active emitters (i.e. touches):
		for i in self.emitters.values():
			i.p_birth_rate = birth_rate / len(self.emitters)
		self.add_child(e)
	
	def touch_moved(self, node, touch):
		e = self.emitters.get(touch.touch_id)
		e.position = touch.location
	
	def touch_ended(self, node, touch):
		e = self.emitters.get(touch.touch_id)
		e.p_birth_rate = 0
		e.run_action(sk.sequence([sk.wait(5), sk.call(e.remove_from_parent)]))
		del self.emitters[touch.touch_id]

def main():
	game = ParticleScene()
	scene_view = sk.View(game)
	scene_view.shows_fps = True
	scene_view.shows_node_count = True
	scene_view.present()

if __name__ == '__main__':
	main()