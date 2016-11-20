# https://gist.github.com/balachandrana/de389c3bd84f006ad4c8d5e3d1cd4a8d

import ui

images = [ui.Image.named(i) for i in 'Rabbit_Face|Mouse_Face|Cat_Face|Dog_Face|Octopus|Cow_Face'.split('|')]

def button_action(sender):
	def animation():
		cv = sender.superview['view1'].subviews[0]
		w = sender.superview['view1'].width
		if sender.title == '>':
			if cv.x > (-(len(images)-1)*w):
				cv.x = (cv.x-w)
		else:
			if cv.x < 0:
				cv.x = (cv.x+w)
	ui.animate(animation, duration=3)
	
v = ui.load_view()
x, y, w, h = v['view1'].frame
cv = ui.View(frame=(0, 0,len(images)*w, h))
v['view1'].add_subview(cv)
for i, img in enumerate(images):
	imgview = ui.ImageView(frame=(i*w,0,w,h))
	imgview.image = img
	cv.add_subview(imgview)
v.present('sheet')

