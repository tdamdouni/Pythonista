# https://forum.omz-software.com/topic/3988/simple-ui-tutorial/5

# Learning Alignment Options In UI
# Pythonista
# Flex LRTBWH
import ui

w,h = ui.get_screen_size()
h = h - 64
view = ui.View(name = 'Flex', bg_color = 'lightyellow', frame = (0,0,w,h))
#view.flex = 'WH'
# label height and button width
bh = bw = 80
# margin
mg = 10


lb1 = ui.Label(name = 'Label1', bg_color = 'yellow', frame =(mg,mg,bw,bh))
lb1.border_color = 'black'
lb1.border_width = 1
lb1.flex = 'RB'
lb1.alignment=1
lb1.text = lb1.flex

lb2 = ui.Label(name = 'Label2', bg_color = 'yellow', frame =(w-(bw+mg),mg, bw,bh))
lb2.border_color = 'black'
lb2.border_width = 1
lb2.flex = 'LB'
lb2.alignment=1
lb2.text = lb2.flex

lb3 = ui.Label(name = 'Label3', bg_color = 'yellow', frame =(mg,h-(bh+mg),bw,bh))
lb3.border_color = 'black'
lb3.border_width = 1
lb3.flex = 'RT'
lb3.alignment=1
lb3.text = lb3.flex

lb4 = ui.Label(name = 'Label4', bg_color = 'yellow', frame =(w-(bw+mg),h-(bh+mg),bw,bh))
lb4.border_color = 'black'
lb4.border_width = 1
lb4.flex = 'LT'
lb4.alignment=1
lb4.text = lb4.flex

# center
lb5 = ui.Label(name = 'Label5', bg_color = 'yellow', frame =((w-bw)*.5,(h-bh)*.5,bw,bh))
lb5.border_color = 'black'
lb5.border_width = 1
lb5.flex = 'LRTB'
lb5.alignment=1
lb5.text = lb5.flex

view.add_subview(lb1)
view.add_subview(lb2)
view.add_subview(lb3)
view.add_subview(lb4)
view.add_subview(lb5)

view.present('screen')

# --------------------

# Learning Alignment Options In UI
# Pythonista
# Flex LRTBWH
import ui


def make_label(name, frame):
	return ui.Label(
	alignment=1,
	bg_color='yellow',
	border_color='black',
	border_width=1,
	flex=name,
	frame=frame,
	name=name,
	text=name)
	
	
w, h = ui.get_screen_size()
h -= 64
bh = bw = 80  # label height and button width
mg = 10  # margin
view = ui.View(name='Flex', bg_color='lightyellow', frame=(0, 0, w, h))
view.add_subview(make_label(name='RB', frame=(mg, mg, bw, bh)))
view.add_subview(make_label(name='LB', frame=(w - (bw + mg), mg, bw, bh)))
view.add_subview(make_label(name='RT', frame=(mg, h - (bh + mg), bw, bh)))
view.add_subview(make_label(name='LT',
                            frame=(w - (bw + mg), h - (bh + mg), bw, bh)))
view.add_subview(make_label(name='LRTB',
                            frame=((w - bw) * .5, (h - bh) * .5, bw, bh)))
view.present()
# --------------------

