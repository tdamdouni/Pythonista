# https://gist.github.com/jsbain/e64581caa4588625896594882870c50c

'''Dual interpreter experiment:  try launching py2 script from py3.
Result: success.... but globals are cleared,- same as if play button is pressed
'''
import sys
from objc_util import *
import editor,os

@on_main_thread
def _get_editor_tab():
	''' from editor.py in py3, gets the texteditorviewcontroller.
	However...what if no files are open!  this will fail. consuder opening a file in this case'''
	win = UIApplication.sharedApplication().keyWindow()
	root_vc = win.rootViewController()
	if root_vc.isKindOfClass_(PASlidingContainerViewController):
		tabs_vc = root_vc.detailViewController()
		tab = tabs_vc.selectedTabViewController()
		if tab.isKindOfClass_(PA2UniversalTextEditorViewController):
			return tab
	return None
	
@on_main_thread	
def launch_with_py2(path,args):
	'''launch a script at path, using args.  This essentially is what happens when you press the run button and choose py2.  Note, this means globals are cleared.... blechhh'''
	E=editor._get_editor_tab()
	E.runScriptAtPath_withInterpreterVersion_arguments_(path,2,args)

def waitForInterpreter(timeout=5,poll_interval=0.1):
	'''If the interpreter is running another script, the launch is ignored.so wait until it is ready.  
	this should maybe go into launch, along with a Lock so that only one thread can be waiting at a time'''
	import time
	t0=time.time()
	I2=ObjCClass('PythonInterpreter').sharedInterpreter()
	while I2.running():
		time.sleep(poll_interval)
		if time.time()-t0 > timeout:
			raise Exception('Timeout while waiting for interpreter')
			
if __name__=='__main__' and sys.version_info.major==3:
	'''PY3 example path: launch this script a few times in py2'''
	import time
	print('launching py2')
	launch_with_py2(__file__,['hello','world'])
	print('waiting for py2')
	waitForInterpreter(	)
	print('launching py2')
	launch_with_py2(__file__,['helloooo','world'])
	print('done')
if __name__=='__main__' and sys.version_info.major==2:
	'''PY2 starts here.  just print arguments'''
	import sys
	print (sys.argv[1:])
