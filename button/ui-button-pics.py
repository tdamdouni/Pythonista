# https://forum.omz-software.com/topic/3462/lab-easy-way-to-make-pics-using-ui-button

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor
import calendar

def btn_image(text, w = 256):
	btn = ui.Button( title = text)
	btn.frame = (0, 0, w, w)
	btn.bg_color = 'teal'
	btn.tint_color = 'white'
	btn.font = ('Arial Rounded MT Bold', w * .4)
	btn.corner_radius = btn.width / 2
	with ui.ImageContext(w, w) as ctx:
		btn.draw_snapshot()
		return ctx.get_image()
		
if __name__ == '__main__':

	for i in range(1, 13):
		m_name = calendar.month_abbr[i]
		btn_image( m_name, w = 48).show()
		
	for i in range(1, 7):
		btn_image( str(i) , w = 32).show()
		
	lst = ['stop', 'start', 'go' , 'wait']
	for lb in lst:
		btn_image( lb, w = 256).show()

