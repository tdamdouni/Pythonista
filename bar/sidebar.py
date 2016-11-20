# https://gist.github.com/jsbain/8e872d12349ed11484ead7632d4859ad

'''sidebar
a sidebar replacement for pythonista.
Lives in the editor.
'''
import ui
from objc_util import UIApplication, ObjCInstance
from ctypes import cast, py_object, c_void_p
class SideBar(ui.View):
	def __init__(self,width=55,*args,**kwargs):
		'''initialize the sidebar
		arguments:
		width (default = 55)
		'''
		app=UIApplication.sharedApplication()
		self.containerView=app.keyWindow().rootViewController().\
		detailContainerView()
		# we will add ourself as a subview of the container view, on the right edge, and also resize the other subviews to fit.
		self.background_color='white'
		self.alpha=0.5
		self.width=width
		self.y=20
		self.height=self.containerView.frame().size.height
		self.siblings=self.containerView.subviews()
		close=ui.Button(image=ui.Image('iob:close_round_24'))
		close.frame=[5,5,24,24]
		close.action=self._close
		self.add_subview(close)
		self.flex='LH'
		ObjCInstance(self).tag=hash('SideBar')
	def layout(self):
		'''resize other views when this view changes width'''
		for sib in self.siblings:
			f=sib.frame()
			if f.size.width + self._width ==                self.containerView.frame().size.width:
				f.size.width = self.containerView.frame().size.width-self.width
				sib.frame=f
			self._width=self.width
			self.x=self.containerView.frame().size.width-self.width
	def present(self):
		'''if another sidebar is being presented, close it first.  add to the editor window, shrinking other content'''
		if self.on_screen:
			return
		for sib in self.siblings:
			if sib.tag()==hash('SideBar'):
				sib.removeFromSuperview()
			else:
				f=sib.frame()
				if f.size.width==self.containerView.frame().size.width:
					f.size.width -= self.width
					sib.frame=f
			self.x=self.containerView.frame().size.width-self.width
			self.containerView.addSubview_(ObjCInstance(self))
			self._width=self.width
	def close(self):
		'''for programmatic close'''
		self._close(self)
	def _close(self,sender):
		''' button callback. reset siblings, and close subview'''
		ObjCInstance(self).removeFromSuperview()
		for sib in self.siblings:
			f=sib.frame()
			if f.size.width==self.containerView.frame().size.width-self.width:
				f.size.width+=self.width
				sib.frame=f
		if hasattr(self,'will_close') and callable(self.will_close):
			self.will_close()
			
if __name__ == '__main__':
	s=SideBar()
	b=ui.Button(image=ui.Image('iob:calculator_32'))
	s.add_subview(b)
	b.y=33
	b.flex='lr'
	s.present()

