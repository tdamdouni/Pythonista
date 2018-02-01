# https://forum.omz-software.com/topic/3758/disable-stop-button-x-in-scene/6

# Hide X button
import ui
view = ui.View(bg_color = 'slateblue')
view.present('sheet', hide_title_bar=True)

#
class MyScene(scene.Scene):
	def setup(self):
		self.label = scene.LabelNode('Test hide title bar',
		position=self.size/2, parent=self)
		self.hide_close()
		
	def hide_close(self, state=True):
		from obj_util import ObjCInstance
		v = ObjCInstance(self.view)
		# Find close button.  I'm sure this is the worst way to do it
		for x in v.subviews():
			if str(x.description()).find('UIButton) >= 0:
				x.setHidden(state)
				
scene.run(MyScene())

#
v = ui.View

v.present(title_bar_color='#000000',
hide_close_button=True,
orientations=['portrait'])

