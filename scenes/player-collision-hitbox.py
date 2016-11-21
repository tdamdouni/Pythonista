# https://forum.omz-software.com/topic/3471/player-collision-hitbox/12

#update(self):
        #if self.frame.intersects(bullet.frame):
                #exit('Player has died of rapid onset lead poisoning!!!')
# --------------------
from scene import *
import ui

class MyScene (Scene):
	def setup(self):
		sprite = SpriteNode('plf:HudPlayer_yellow')
		self.player = ShapeNode(parent=self, path=ui.Path.rect(*sprite.frame),
		position=self.size/2, fill_color='clear', stroke_color='red')
		self.player.add_child(sprite)
		
if __name__ == '__main__':
	run(MyScene(), show_fps=False)
# --------------------
		#x, _= touch.location
		#_, y = self.player.position
	#       move_action = Action.move_to(x,y,2,TIMING_SINODIAL)
		#self.player.run_action(move_action)
		#if (x,_ > 0.05):
																#self.player.x_scale = cmp(touch.location.x -
																#self.player.position.x, 0)
																#x = self.player.position.x
# --------------------
import scene
import ui

class MyScene (scene.Scene):
	def setup(self):
		img = ui.Image.named('plf:HudPlayer_yellow')
		w, h = img.size
		with ui.ImageContext(w, h) as ctx:
			img.draw(0,0,w,h)
			path = ui.Path.rect(0, 0, w,h)
			ui.set_color('red')
			path.stroke()
			img1 = ctx.get_image()
		self.sprite_node = scene.SpriteNode(scene.Texture(img1), position=self.size/2, parent=self)
		# use img for regular game and img1 for debugging purpose
		#self.sprite_node = scene.SpriteNode(scene.Texture(img), position=self.size/2, parent=self)
		
if __name__ == '__main__':
	scene.run(MyScene(), show_fps=False)
# --------------------
class Rock(SpriteNode):
 def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'IMG_1726.GIF', **kwargs)
		
def update (self):

 self.spawn_rock



class Rock(SpriteNode):
 def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'IMG_1726.GIF', **kwargs)
# --------------------

