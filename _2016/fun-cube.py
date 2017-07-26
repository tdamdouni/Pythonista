# https://forum.omz-software.com/topic/3922/for-the-fun-a-photos-cube

from objc_util import *
import ui
import math

load_framework('SceneKit')

SCNView, SCNScene, SCNBox ,SCNNode, SCNMaterial, SCNCamera, SCNLookAtConstraint = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox' ,'SCNNode', 'SCNMaterial', 'SCNCamera', 'SCNLookAtConstraint' ])

@on_main_thread
def demo():
	main_view = ui.View()
	main_view_objc = ObjCInstance(main_view)
	scene_view = SCNView.alloc().initWithFrame_options_(((((0, 0),(100, 50)), ), None)).autorelease()
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
	camera_node.setPosition((-3.0,3.0, 3))

	cube_geometry = SCNBox.boxWithWidth_height_length_chamferRadius_(1, 1, 1, 0)

	Material_img1 = SCNMaterial.material()
	Material_img1.contents = UIImage.imageWithContentsOfFile_('Photo1.JPG')
	Material_img2 = SCNMaterial.material()
	Material_img2.contents = UIImage.imageWithContentsOfFile_('Photo2.JPG')
	Material_img3 = SCNMaterial.material()
	Material_img3.contents = UIImage.imageWithContentsOfFile_('Photo3.JPG')
	Material_img4 = SCNMaterial.material()
	Material_img4.contents = UIImage.imageWithContentsOfFile_('Photo4.JPG')
	Material_img5 = SCNMaterial.material()
	Material_img5.contents = UIImage.imageWithContentsOfFile_('Photo5.JPG')
	Material_img6 = SCNMaterial.material()
	Material_img6.contents = UIImage.imageWithContentsOfFile_('Photo6.JPG')
	cube_geometry.setMaterials_([Material_img1,Material_img2,Material_img3,Material_img4,Material_img5,Material_img6])

	cube_node = SCNNode.nodeWithGeometry_(cube_geometry)

	# Add a constraint to the camera to keep it pointing to the target cube
	constraint = SCNLookAtConstraint.lookAtConstraintWithTarget_(cube_node)
	constraint.gimbalLockEnabled = True
	camera_node.constraints = [constraint]

	root_node.addChildNode_(camera_node)    
	root_node.addChildNode_(cube_node)

	main_view.present(hide_title_bar=True)

demo()
