# coding: utf-8
import sk
import ui

class ShaderScene (sk.Scene):
	def __init__(self):
		w, h = self.size
		img = ui.Image.named('gradient.png')
		self.sprite = sk.SpriteNode(sk.Texture(img))
		self.sprite.position = w/2, h/2
		self.sprite.size = w, h
		with open('SimplexNoise.fsh') as f:
			shader = sk.Shader(f.read())
		self.sprite.shader = shader
		self.add_child(self.sprite)
	
	def did_change_size(self, old_size):
		self.sprite.size = self.size
		self.sprite.position = self.size[0]/2, self.size[1]/2

def main():
	scene = ShaderScene()
	scene_view = sk.View()
	scene_view.run_scene(scene)
	scene_view.present()

if __name__ == '__main__':
	main()