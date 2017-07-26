# https://pythonista-app.slack.com/archives/codinghelp/p1481850796000351

from objc_util import *
import ui

load_framework('ModelIO')
load_framework('SceneKit')
SCNView, SCNScene, SCNBox, SCNText, SCNNode, SCNLight, SCNAction, UIFont, MDLAsset = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox', 'SCNText', 'SCNNode', 'SCNLight', 'SCNAction', 'UIFont', 'MDLAsset'])

@on_main_thread
def setup():
	v = ui.View()
	o=ObjCInstance(v._objc_ptr)
	u=nsurl('lamp.obj')
	scene_view = SCNView.alloc().initWithFrame_options_(((0,0),(1000, 1000)), None).autorelease()
	scene_view.setAutoresizingMask_(32)
	scene_view.setAllowsCameraControl_(True)
	a=MDLAsset.new().initWithURL_(u)
	s = SCNScene.sceneWithMDLAsset_(a)
	rootNode = s.rootNode()
	mesh = a.objects()[0]
	'''light_node = SCNNode.node()
	light_node.setPosition_((0, 100, 10))
	light = SCNLight.light()
	light.setType_('ambient')
	light.setCastsShadow_(True)
	light_node.setLight_(light)
	rootNode.addChildNode_(light_node)'''
	scene_view.setScene_(s)
	o.addSubview_(scene_view)
	globals().update(locals())
	
setup()

