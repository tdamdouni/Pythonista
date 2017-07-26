# https://gist.github.com/jsbain/84ab564cf1ae26ce4ad100b103502b17

# https://forum.omz-software.com/topic/3497/pythonista-3-external-keyboard-shortcut-to-switch-tabs

from objc_util import *

@on_main_thread
def select(idx):
	import editor
	tvc=editor._get_editor_tab().parentViewController()
	tbv=tvc.tabBarView()
	tvs=tbv.tabViews()
	if idx < len(tvs):
		tvc.tabBarView().tabSelected_(tvs[idx])
		tvc.switchToTabViewController_(tvc.tabViewControllers()[idx])
	
@on_main_thread
def nextTab():
	import editor
	tvc=editor._get_editor_tab().parentViewController()
	tbv=tvc.tabBarView()
	tvs=tbv.tabViews()
	current=tbv.selectedTabIndex()
	next=(current+1)%len(tvs)
	tbv.tabSelected_(tvs[next])
	tvc.switchToTabViewController_(tvc.tabViewControllers()[next])


@on_main_thread
def prevTab():
	import editor
	tvc=editor._get_editor_tab().parentViewController()
	tbv=tvc.tabBarView()
	tvs=tbv.tabViews()
	current=tbv.selectedTabIndex()
	next=(current-1)%len(tvs)
	tbv.tabSelected_(tvs[next])
	tvc.switchToTabViewController_(tvc.tabViewControllers()[next])

#select(0)
#nextTab()
#prevTab()
