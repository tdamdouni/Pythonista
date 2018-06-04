from scene import *
class LogEntry(LabelNode):
   def __init__(self,text):
      LabelNode.__init__(self,text)
      self.anchor_point=(0,0)
      self.run_action(Action.sequence(Action.fade_to(0,1.5),Action.call(self.cull)))
   def cull(self):
      '''remove a log entry'''
      self.remove_all_actions()
      self.remove_from_parent()
class Log(Node):
   '''A simple console replacement for scene.
   Log is callable, i.e
      self.log=Log(self)
      self.log('Hello')
   '''
   def __init__(self, parent):
      '''pass parent scene, Log adds itself.  TODO: set font size'''
      parent.add_child(self)
   def add_text(self,text):
      '''add a logentry (this can contain newlines to split multiple lines)
      previous logs entries are shifted up. 
      old entries are faded and removed after a short time
      
      '''
      n=LogEntry(text)
      for c in self.children:
         c.position=(0,c.position.y+n.bbox.height)
      self.add_child(n)
   def __call__(self,text):
      self.add_text(text)
class MyScene(Scene):
   def setup(self):
      self.log=Log(self)
      self.log('Hello\nWorld!')
   def touch_began(self, touch):
      x, y = touch.location
      self.log('touch_began  {},{}'.format(x,y))
      
s=MyScene()
run(s)
