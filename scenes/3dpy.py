# https://forum.omz-software.com/topic/1686/3d-in-pythonista/11

# https://code.tutsplus.com/tutorials/an-introduction-to-scenekit-fundamentals--cms-23847

from objc_util import *
import ui
import math

load_framework('SceneKit')

SCNView, SCNScene, SCNBox, SCNText, SCNNode, SCNLight, SCNCamera, SCNAction, UIFont = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox', 'SCNText', 'SCNNode', 'SCNLight',  'SCNCamera', 'SCNAction', 'UIFont'])

class SCNVector3 (Structure):
	_fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]
	
'''
https://code.tutsplus.com/tutorials/an-introduction-to-scenekit-fundamentals--cms-23847
'''
'''
override func viewDidLoad() {
    super.viewDidLoad()

    let sceneView = SCNView(frame: self.view.frame)
    self.view.addSubview(sceneView)

    let scene = SCNScene()
    sceneView.scene = scene

    let camera = SCNCamera()
    let cameraNode = SCNNode()
    cameraNode.camera = camera
    cameraNode.position = SCNVector3(x: 0.0, y: 0.0, z: 3.0)

    let light = SCNLight()
    light.type = SCNLightTypeOmni
    let lightNode = SCNNode()
    lightNode.light = light
    lightNode.position = SCNVector3(x: 1.5, y: 1.5, z: 1.5)

    let cubeGeometry = SCNBox(width: 1.0, height: 1.0, length: 1.0, chamferRadius: 0.0)
    let cubeNode = SCNNode(geometry: cubeGeometry)

    scene.rootNode.addChildNode(lightNode)
    scene.rootNode.addChildNode(cameraNode)
    scene.rootNode.addChildNode(cubeNode)
}
'''

@on_main_thread
def demo():
	main_view = ui.View()
	main_view_objc = ObjCInstance(main_view)
	scene_view = SCNView.alloc().initWithFrame_options_(((0, 0),(400, 400)), None).autorelease()
	scene_view.setAutoresizingMask_(18)
	scene_view.setAllowsCameraControl_(True)
	main_view_objc.addSubview_(scene_view)
	main_view.name = 'SceneKit Demo'
	
	scene = SCNScene.scene()
	scene_view.setScene_(scene)
	
	root_node = scene.rootNode()
	
	camera = SCNCamera.camera()
	camera_node = SCNNode.node()
	camera_node.setCamera(camera)
	camera_node.setPosition((0.0, 0.0, 3.0))
	
	light = SCNLight.light()
	light.setType_('omni')
	light_node = SCNNode.node()
	light_node.setLight_(light)
	light_node.setPosition((1.5, 1.5, 1.5))
	
	cube_geometry = SCNBox.boxWithWidth_height_length_chamferRadius_(1, 1, 1, 0)
	cube_node = SCNNode.nodeWithGeometry_(cube_geometry)
	
	root_node.addChildNode_(light_node)
	root_node.addChildNode_(camera_node)
	root_node.addChildNode_(cube_node)
	
	main_view.present()
	
demo()

