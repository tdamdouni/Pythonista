# https://forum.omz-software.com/topic/3534/lab-strange-visual-effect-trying-to-create-a-radial-blur

'''
    Pythonista Forum - @Phuket2
'''
import ui

class MyClass(ui.View):
	#def __init__(self, *args, **kwargs):
                #super().__init__(*args, **kwargs)

	def draw(self):
		wh = 100
		r = ui.Rect(0, 0, wh, wh)
		r.center(self.bounds.center())
		s = ui.Path.oval(*r)
		rd = 1
		for i in range(int(r.width)):
			s = ui.Path.oval(*r)
			s.line_width = 1
			c = (0,  rd, 0, 1)
			ui.set_color( c)
			s.stroke()
			r = r.inset(.5, .5)
			rd -=.01
			
			
if __name__ == '__main__':
	w, h = 320, 480
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=False)
# --------------------

