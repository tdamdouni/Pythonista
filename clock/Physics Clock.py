# slightly modified from original sample code to set gravity from motion data (see did_start, did_stop, update methods)

# https://gist.github.com/omz/5396a323d0c443a446f6

'''A digital clock as a simple physics simulation -- The numbers fall down and collide with the floor (and each other)'''

import sk
import ui
import time
import motion

s = 80 if max(ui.get_screen_size()) >= 768 else 36

class ClockScene (sk.Scene):
	def __init__(self):
		self.dropped_sprites = set()
		# Initialize the floor collision body:
		w = self.size[0]
		self.physics_body = sk.PhysicsBody.edge_loop_rect(0, -100, w, 100)
		# Draw and cache textures for all numbers:
		self.textures = {}
		for n in '0123456789:':
			w, h = s*2+10, s*2
			with ui.ImageContext(w, h) as ctx:
				ui.draw_string(n, font=('AvenirNext-Regular', h*0.94), rect=(0, 0, w, h), color='white', alignment=ui.ALIGN_CENTER)
				img = ctx.get_image()
				self.textures[n] = sk.Texture(img)
		margin = (self.size[0] - 7 * s) / 2
		self.clock_nodes = []
		self.time_str = time.strftime('%H:%M:%S')
		# Create a sprite node for every character in the time string:
		for i, c in enumerate(self.time_str):
			sprite = sk.SpriteNode(self.textures[c])
			sprite.position = i * s + margin, self.size[1] - 200
			self.add_child(sprite)
			self.clock_nodes.append(sprite)
			
	def did_start(self):
		motion.start_updates()
		
	def did_stop(self):
		motion.stop_updates()
		
	def update(self):
		gx, gy = motion.get_gravity()[:2]
		self.physics_gravity = (gx*10, gy*10)
		
		time_str = time.strftime('%H:%M:%S')
		if time_str == self.time_str:
			return
		for i, c in enumerate(time_str):
			if c != self.time_str[i]:
				# Digit has changed, replace it with a new sprite...
				old = self.clock_nodes[i]
				sprite = sk.SpriteNode(self.textures[c])
				sprite.position += old.position.x, old.position.y + s*2
				sprite.alpha = 0.0
				sprite.run_action(sk.Action.fade_in(0.7))
				move = sk.Action.move_by(0, -s*2, 0.85)
				move.timing_mode = sk.TIMING_EASE_OUT
				sprite.run_action(move)
				self.clock_nodes[i] = sprite
				self.add_child(sprite)
				# Make the old sprite drop by assigning a physics body:
				b = sk.PhysicsBody.from_texture(old.texture)
				b.restitution = 0.25
				old.physics_body = b
				self.dropped_sprites.add(old)
				# Remove sprites that are no longer visible:
				offscreen = {s for s in self.dropped_sprites if s.position[1] < 0}
				map(sk.Node.remove_from_parent, offscreen)
				self.dropped_sprites -= offscreen
		self.time_str = time_str
		
def main():
	scene = ClockScene()
	scene_view = sk.View()
	scene_view.run_scene(scene)
	scene_view.present(orientations=['portrait'])
	
if __name__ == '__main__':
	main()

