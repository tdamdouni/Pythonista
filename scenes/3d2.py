# https://files.slack.com/files-pri/T0M854UF2-F3GKKPYJZ/3d_2.py

from objc_util import *
import ui
import math

load_framework('ModelIO')
load_framework('SceneKit')
load_framework('SpriteKit')

SCNView, SCNScene, SCNBox, SCNText, SCNNode, SCNLight, SCNAction, UIFont, MDLAsset, MDLObject, SCNCone , SCNMaterial, SCNTorus, SKTexture = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox', 'SCNText', 'SCNNode', 'SCNLight', 'SCNAction', 'UIFont', 'MDLAsset', 'MDLObject', 'SCNCone', 'SCNMaterial', 'SCNTorus', 'SKTexture'])

class SCNVector3 (Structure):
	_fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]

def returni(item):
	global slide
	slide = item
	return slide

view = ui.load_view('3D')
view.present('panel')

main_view = view['3D']
main_view_objc = ObjCInstance(main_view)
scene_view = SCNView.alloc().initWithFrame_options_(((0, 0),(main_view.width, main_view.height-100)), None).autorelease()
#scene_view = SCNView.alloc().initWithFrame_options_(((0, 0),(10000, 10000)), None).autorelease()
scene_view.setAutoresizingMask_(53)
scene_view.setAllowsCameraControl_(True)
scene_view.setShowsStatistics_(True)
scene = SCNScene.scene()
root_node = scene.rootNode()
text_mesh = SCNText.textWithString_extrusionDepth_('Test', 6.0)
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
root_node.addChildNode_(text_node)
box = SCNBox.boxWithWidth_height_length_chamferRadius_(100, 0., 100, 1)
box_node = SCNNode.nodeWithGeometry_(box)
root_node.addChildNode_(box_node)

#cone = SCNCone.coneWithTopRadius_bottomRadius_height_(0,10,50)
#cone_node = SCNNode.nodeWithGeometry_(cone)
#root_node.addChildNode_(cone_node)
torus = SCNTorus.torusWithRingRadius_pipeRadius_(10, 5)
torus_node = SCNNode.nodeWithGeometry_(torus)
root_node.addChildNode_(torus_node)
'''rotate_action = SCNAction.repeatActionForever_(SCNAction.rotateByX_y_z_duration_(0, math.pi*2, math.pi*2, 10))
text_container.runAction_(rotate_action)
root_node.addChildNode_(text_container)'''
light_node = SCNNode.node()
light_node.setPosition_((0, 100, 0))
light_node.setRotation_((1, 0, 0, -math.pi/2))
light = SCNLight.light()
light.setType_('spot')
light.setCastsShadow_(True)
light.setColor_(UIColor.yellowColor().CGColor())
light.setShadowSampleCount_(300)
light_node.setLight_(light)
root_node.addChildNode_(light_node)
scene_view.setScene_(scene)
scene_view.setDebugOptions_(3 << 0 <<2)
main_view_objc.addSubview_(scene_view)
#view.autoresizing = 'WHLRTB'
#main_view.width = 1500
#main_view.height = 1000

scene_view.setBackgroundColor_(UIColor.grayColor())

u=nsurl('lamp.obj')
a=MDLAsset.new().initWithURL_(u)
mesh = a.objects()[0]
