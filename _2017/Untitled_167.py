from objc_util import *
import ui
NSBundle.bundleWithPath_('/System/Library/Frameworks/CoreAudioKit.framework').load()
app=UIApplication.sharedApplication()
CABTMIDICentralViewController=ObjCClass('CABTMIDICentralViewController')
vc=CABTMIDICentralViewController.new()

root=ui.View(frame=(0,0,200,320))
v1=ui.View(frame=(0,0,200,320),bgcolor='blue',name='a')
nav=ui.NavigationView(v1,frame=(0,0,200,320))
root.add_subview(nav)
nc=ObjCInstance(nav).navigationController()

root.present('sheet')
@on_main_thread
def run():
	nc.pushViewController_animated_(vc,False)
run()
