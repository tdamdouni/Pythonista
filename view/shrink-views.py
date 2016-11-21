# https://gist.github.com/jsbain/d7dbf8bfa6ace92b38430e6f8b80e995

# https://forum.omz-software.com/topic/3504/lab-ui-animate-sliding-in-views/2

import ui

def shrink(sender):
	def a():
		v.transform=ui.Transform.rotation(-30).concat(ui.Transform.scale(0.1,0.1)).concat(ui.Transform.translation(300,300))
		v.alpha=0
	def compl():
		v.hidden=True
		b2.hidden=False
	ui.animate(a,.5,completion=compl)
def expand(sender):
	v.transform=ui.Transform.rotation(-30).concat(ui.Transform.scale(0.1,0.1)).concat(ui.Transform.translation(300,300))
	v.alpha=0.1
	v.hidden=False
	b2.hidden=True
	def a():
		v.transform=ui.Transform() #default
		v.alpha=1
	def compl():
		pass
	ui.animate(a,.3,completion=compl)
v=ui.View(bg_color='#ffc280',frame=(0,0,200,200))
v.add_subview(ui.TextView(name='text',frame=(20,40,60,40)))
v['text'].text='Click above'
root=ui.View(frame=(0,0,560,560),bg_color='white')
v.center=root.bounds.center()
b=ui.Button(frame=(0,0,50,50))
v.add_subview(b)
b.title='Shrink'
b.action=shrink
b2=ui.Button(title='expand',frame=(root.width,root.height,-100,-100))
b2.hidden=True
b2.action=expand
root.add_subview(b2)
root.present('sheet')
root.add_subview(v)

