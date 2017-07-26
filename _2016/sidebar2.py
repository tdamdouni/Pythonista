# coding: utf-8

# https://gist.github.com/Tileyon/9ea9e4c36e1df21177ca15c743d135bf

# https://forum.omz-software.com/topic/3543/share-in-work-side-bar-replacement/3

'''sidebar
a sidebar replacement for pythonista.
Lives in the editor.
'''
import ui
from objc_util import UIApplication, ObjCInstance
from ctypes import cast, py_object, c_void_p
import clipboard, editor

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
				if f.size.width + self._width == 		self.containerView.frame().size.width:
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
			
def select_action(self):
    i=editor.get_selection()
    editor.set_selection(i[0],i[1]+1)
        
def copy_action(sender):
    i=editor.get_selection()
    t=editor.get_text()
    clipboard.set(t[i[0]:i[1]])

def paste_action(sender):
    i=editor.get_selection()
    t=editor.get_text()
    editor.replace_text(i[0],i[1], clipboard.get())
    editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))
    
def cut_action(sender):
    i=editor.get_selection()
    t=editor.get_text()
    clipboard.set(t[i[0]:i[1]])
    editor.replace_text(i[0],i[1], '')
    editor.set_selection(i[0],i[0])

def indent(self):
    """indent selected lines by one tab"""
    import editor
    import re

    i=editor.get_line_selection()
    t=editor.get_text()
    # replace every occurance of newline with  newline plus indent, except last newline
    
    INDENTSTR = '    '
    editor.replace_text(i[0],i[1]-1,INDENTSTR+re.sub(r'\n',r'\n'+INDENTSTR,t[i[0]:i[1]-1]))

    editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

def unindent(self):
    """unindent selected lines all the way"""
    import editor
    import textwrap

    i=editor.get_line_selection()
    t=editor.get_text()

    editor.replace_text(i[0],i[1], textwrap.dedent(t[i[0]:i[1]]))

    editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

def comment_action(sender):
    """" comment out selected lines"""
    import re
    COMMENT='#'
    i=editor.get_line_selection()
    t=editor.get_text()
    # replace every occurance of newline with  ewline plus COMMENT, except last newline
    editor.replace_text(i[0],i[1]-1,COMMENT+re.sub(r'\n',r'\n'+COMMENT,t[i[0]:i[1]-1]))
    editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

def uncomment_action(self):
    """" uncomment selected lines"""
    import re
    COMMENT='#'
    i=editor.get_line_selection()
    t=editor.get_text()
    # replace every occurance of newline # with newline, except last newline
    if all( [x.startswith('#') for x in t[i[0]:i[1]-1].split(r'\n')]):
        editor.replace_text(i[0],i[1]-1,re.sub(r'^'+COMMENT,r'',t[i[0]:i[1]-1],flags=re.MULTILINE))
    editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))

def execlines_action(self):
    """execute selected lines in console.   """
    import textwrap
    a=editor.get_text()[editor.get_line_selection()[0]:editor.get_line_selection()[1]]
    exec(textwrap.dedent(a))
    
def finddocstring(self):
    ''' find the docstring at current cursor location
    '''
    import StringIO
    from jedi import Script

    i=editor.get_selection()
    t=editor.get_text()
    (line,txt)=[(line,n) for (line,n) in enumerate(StringIO.StringIO(editor.get_text()[:i[1]]))][-1]
    script = Script(t, line+1, len(txt))

    dfn = script.goto_definitions()
    if dfn:
        doc=dfn[0].doc
        import ui
        v=ui.TextView()
        v.width=200
        v.height=250
        v.text=doc
        v.present('popover')
        #editor._set_toolbar(v)
    
if __name__ == '__main__':
	s=SideBar()
	
	b01=ui.Button(image=ui.Image('iob:ios7_bolt_32'))
	b01.action = execlines_action
	s.add_subview(b01)
	b01.y=60
	b01.x=10
	
	b02=ui.Button(image=ui.Image('iob:code_32'))
	b02.action = select_action
	s.add_subview(b02)
	b02.y=120
	b02.x=10
	
	b03=ui.Button(image=ui.Image('iob:ios7_copy_outline_32'))
	b03.action = copy_action
	s.add_subview(b03)
	b03.y=180
	b03.x=10
	
	b04=ui.Button(image=ui.Image('iob:ios7_trash_outline_32'))
	b04.action = cut_action
	s.add_subview(b04)
	b04.y=240
	b04.x=10
	
	b05=ui.Button(image=ui.Image('iob:clipboard_32'))
	b05.action = paste_action
	s.add_subview(b05)
	b05.y=300
	b05.x=10
	
	b06=ui.Button(image=ui.Image('iob:ios7_skipforward_outline_32'))
	b06.action = indent
	s.add_subview(b06)
	b06.y=360
	b06.x=10
	
	b07=ui.Button(image=ui.Image('iob:ios7_skipbackward_outline_32'))
	b07.action = unindent
	s.add_subview(b07)
	b07.y=420
	b07.x=10
	
	b08=ui.Button(image=ui.Image('iob:pound_32'))
	b08.action = comment_action
	s.add_subview(b08)
	b08.y=480
	b08.x=10
	
	'''
	b09=ui.Button(image=ui.Image('iob:ios7_checkmark_outline_32'))
	b09.action = uncomment_action
	s.add_subview(b09)
	b09.y=540
	b09.x=10
	'''
	
	b09=ui.Button(image=ui.Image('iob:pound_32'))
	b09.action = uncomment_action
	b09.height = 40
	b09.width = 40
	#b09.tint_color = 'green'
	b09.title ='-'
	s.add_subview(b09)
	b09.y=540
	b09.x=10
	
	b10=ui.Button(image=ui.Image('iob:ios7_information_outline_32'))
	b10.action = finddocstring
	s.add_subview(b10)
	b10.y=600
	b10.x=10
	
	s.present()

