# coding: utf-8

# https://forum.omz-software.com/topic/1686/3d-in-pythonista/7

from objc_util import *
import ui
import math

SCNView, SCNScene, SCNBox, SCNText, SCNNode, SCNLight, SCNAction, UIFont = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox', 'SCNText', 'SCNNode', 'SCNLight', 'SCNAction', 'UIFont'])

class SCNVector3 (Structure):
	_fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]
	
@on_main_thread
def demo():
	main_view = ui.View()
	main_view_objc = ObjCInstance(main_view)
	scene_view = SCNView.alloc().initWithFrame_options_(((0, 0),(400, 400)), None).autorelease()
	scene_view.setAutoresizingMask_(18)
	scene_view.setAllowsCameraControl_(True)
	scene = SCNScene.scene()
	root_node = scene.rootNode()
	text_mesh = SCNText.textWithString_extrusionDepth_('@tdamdouni', 6.0)
	text_mesh.setFlatness_(0.2)
	text_mesh.setChamferRadius_(0.4)
	text_mesh.setFont_(UIFont.fontWithName_size_('HelveticaNeue-Bold', 18))
	bbox_min, bbox_max = SCNVector3(), SCNVector3()
	text_mesh.getBoundingBoxMin_max_(byref(bbox_min), byref(bbox_max), restype=None, argtypes=[POINTER(SCNVector3), POINTER(SCNVector3)])
	text_width = bbox_max.x - bbox_min.x
	text_node = SCNNode.nodeWithGeometry_(text_mesh)
	text_node.setCastsShadow_(True)
	text_container = SCNNode.node()
	text_container.addChildNode_(text_node)
	text_container.setPosition_((0, 40, 0))
	text_node.setPosition_((-text_width/2, 0, 0))
	box = SCNBox.boxWithWidth_height_length_chamferRadius_(100, 4, 100, 1)
	box_node = SCNNode.nodeWithGeometry_(box)
	root_node.addChildNode_(box_node)
	rotate_action = SCNAction.repeatActionForever_(SCNAction.rotateByX_y_z_duration_(0, math.pi*2, math.pi*2, 10))
	text_container.runAction_(rotate_action)
	root_node.addChildNode_(text_container)
	light_node = SCNNode.node()
	light_node.setPosition_((0, 100, 10))
	light_node.setRotation_((1, 0, 0, -math.pi/2))
	light = SCNLight.light()
	light.setType_('spot')
	light.setCastsShadow_(True)
	light.setColor_(UIColor.cyanColor().CGColor())
	light_node.setLight_(light)
	root_node.addChildNode_(light_node)
	scene_view.setScene_(scene)
	main_view_objc.addSubview_(scene_view)
	main_view.name = 'SceneKit Demo'
	main_view.present()
	
demo()

