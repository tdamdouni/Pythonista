# https://forum.omz-software.com/topic/4233/viewing-definitions/5

# action move_to example
import scene

class MyScene(scene.Scene):
	def setup(self):
		self.label_node = scene.LabelNode('A',
		position=(100,400), parent=self)
		self.animate_action = scene.Action.move_to(340, 400, 2)
		
	def touch_ended(self, touch):
		self.label_node.run_action(self.animate_action)
		
scene.run(MyScene())

'''
# action move_to example implemented using update
import scene

class MyScene(scene.Scene):
    def setup(self):
        self.label_node = scene.LabelNode('A',
                    position=(100,400), parent=self)
        #self.animate_action = scene.Action.move_to(340, 400, 2)
        self.start_flag = False

    def update(self):
        if self.start_flag:
            x,y = self.label_node.position
            if x < 340:
                self.label_node.position = (x+2, y)
            else:
                self.start_flag = False

    def touch_ended(self, touch):
        self.start_flag = True
        #self.label_node.run_action(self.animate_action)

scene.run(MyScene())
'''


'''
# action move_to example implemented using custom_action
import scene

def custom_action(node, progress):
    x,y = node.initial_position
    node.position = (x+240*progress, y)

class MyScene(scene.Scene):
    def setup(self):
        self.label_node = scene.LabelNode('A',
                    position=(100,400), parent=self)
        x,y = self.label_node.position
        self.label_node.initial_position = (x,y)
        self.animate_action = scene.Action.call(custom_action, 2)

    def touch_ended(self, touch):
        self.label_node.run_action(self.animate_action)

scene.run(MyScene())
'''

