import threading,ui
from objc_util import *

c.dispatch_queue_get_label.argtypes=[c_void_p]
c.dispatch_queue_get_label.restype=c_char_p
DISPATCH_CURRENT_QUEUE_LABEL=c_void_p(0)


def checkThread(case=''):
	currentLabel = c.dispatch_queue_get_label(DISPATCH_CURRENT_QUEUE_LABEL)
	currenThread=threading.current_thread()
	print(case,currentLabel,currenThread)
def b1():
	checkThread('undecorated')

@on_main_thread
def b2():
	checkThread('on_main_thread')
	
@ui.in_background
def b3():
	checkThread('in_background')
	

def b4():
	def d():
		checkThread('delayed')
	ui.delay(d,0.1)

def b5():
	def d():
		checkThread('animated')
		s.y=s.y+1
	def c():
		checkThread('animatcompletion')
	ui.animate(d,0.1,completion=c)
class timerview(ui.View):
	def update(self):
		print('##### Called from UI (press each button)')
		checkThread('update')
		self.update_interval=0.
v=timerview(frame=(0,0,400,400))
v.update_interval=2.
s=ui.SegmentedControl()
s.segments=('ui','main','back','delay','animate')

def a(sender):
	print(s.selected_index)
	if s.selected_index==0:
		b1()
	elif s.selected_index==1:
		b2()
	elif s.selected_index==2:
		b3()
	elif s.selected_index==3:
		b4()
	elif s.selected_index==4:
		b5()
s.action=a
s.size_to_fit()
v.add_subview(s)
s.width=400


def threadtest():
	b1()
	b2()
	b3()
	b4()
	b5()
print('##### current thread:')
checkThread()

print('##### things running from a thread:')
t=threading.Thread(target=threadtest)
t.start()
t.join()

v.present('sheet')
