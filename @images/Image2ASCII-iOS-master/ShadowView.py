# coding: utf-8
import ui, io
def pil_to_ui(image):
	with io.BytesIO() as b:
		image.save(b, 'PNG')
		return ui.Image.from_data(b.getvalue())

class ShadowView(ui.View):
	'''A class for a ui.View that has a shadow behind it.

	This is accomplished by:
	1. Draw the background
	2. Redraw with a shadow, but set clipping so only the edge of the shadow
	shows. This prevents the part of the shadow that's under the background 
	from showing.
	
	'''
	def draw(self):
		
		'1'
		#Setup path of window shape
		path = ui.Path.rect(0, 0, self.width-10, self.height-10)
		
		#Draw background
		ui.set_color((0.95,0.95,0.95,0.5))
		path.fill()
		

		'2'
		#Setup mask by creating image
		from PIL import ImageDraw, Image
		i = Image.new('RGBA',(520,290), (255,255,255,0))
		draw = ImageDraw.Draw(i)
		draw.rectangle((self.width-10, 0, self.width, self.height),fill=(0,0,0,255))
		draw.rectangle((0, self.height-10, self.width, self.height),fill=(0,0,0,255))
		
		#Convert to UI, apply the mask, and draw shadow!
		i = pil_to_ui(i)
		i.clip_to_mask()
		ui.set_color((1,1,1,1))
		ui.set_shadow("black",-2,-2,10)
		path.fill()
	
		
