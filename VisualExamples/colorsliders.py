from visual import *

print("""
Click and drag a ball (with mouse button down) on an RGB or HSV slider.
Click one of the colored objects to print RGB and HSV values.
""")

# Bruce Sherwood; opacity slider added by Jonathan Brandmeyer

scene.userspin = 0
grey = (0.85, 0.85, 0.85)

class slider:
    def __init__(self, pos=vector(0,0,0), axis=vector(0,1.,0), value=None,
                 width=0.15, min=0, max=100., color=(1,0,0)):
        pos = vector(pos)
       # axis = vector(axis)
        if value == None:
            value = min
        self.min = min
        self.max = max
        self.value = value
        self.shaft = cylinder(pos=pos, axis=axis, radius=width/4., color=grey)
        self.start = pos
        self.axis = axis
        self.control = sphere(pos=self.start+(self.min+value)/(self.max-self.min)*self.axis,
                        radius=width/2., color = color)
        self.label = label(pos=self.control.pos, text="%0.2f" % value,
                           opacity=0, box=0, line=0)

    def getslider(self, pos=None):
        pos = vector(pos)
        value = self.min+(self.max-self.min)*(pos.y-self.start.y)/mag(self.axis)
        self.setslider(value)
        return value

    def setslider(self, value=None):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min
        self.value = value
        self.control.pos = self.start+(self.min+value)/(self.max-self.min)*self.axis
        self.label.pos = self.control.pos
        self.label.text="%0.2f" % value

scene.width = 800
scene.height = 400
scene.center = (0,0.5,0)
scene.title = "RGB and HSV color"
wcube = 0.2
rgb = (1,0,0)
opacity = 1
hsv = color.rgb_to_hsv((1,0,0))
ctrl = [slider(pos=(-1.75,0,0), color=(1,0,0), max=1., value=rgb[0]),
        slider(pos=(-1.5,0,0), color=(0,1,0), max=1., value=rgb[1]),
        slider(pos=(-1.25,0,0), color=(0,0,1), max=1., value=rgb[2]),
        slider(pos=(-1,0,0), color=(0.5,0.5,0.5), max=1., value=opacity),
        slider(pos=(+1.0,0,0), color=(1,0,0), max=1., value=hsv[0]),
        slider(pos=(+1.25,0,0), color=(1,1,1), max=1., value=hsv[1]),
        slider(pos=(+1.5,0,0), color=(0.5,0.5,0.5), max=1., value=hsv[2])]
panel = box(pos=(0,0.5,0), length=1.5, height=1, width=0.1, color=rgb, opacity=opacity)
ball = sphere(pos=(0,0.5,0), radius=0.5, color=rgb, opacity=opacity)
cube = box(pos=(0,1.2,0), axis=(1,1,1),
           length=wcube, width=wcube, height=wcube, color=rgb, opacity=opacity)
behind = arrow( pos=(-.75, 0, -.75), axis=(1.5, 1, 0), color=color.white)
dragobj = None

while True:
    rate(50)
    cube.rotate(angle=0.1, axis=scene.up)
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.click == "left" and m.pick in [panel, ball, cube]:
            print("RGB = (%0.3f,%0.3f,%0.3f), opacity = %0.3f" % (ctrl[0].value,ctrl[1].value,ctrl[2].value,ctrl[3].value))
            print("HSV = (%0.3f,%0.3f,%0.3f)" % (ctrl[4].value,ctrl[5].value,ctrl[6].value))
            continue
        elif m.drop == "left":
            dragobj = None
        elif m.drag == "left":
            for index in range(7):
                s = ctrl[index]
                if m.pick is s.control:
                    pos = m.project(normal=(0,0,1))
                    dragobj = s
                    break
    newpos = scene.mouse.project(normal=(0,0,1))
    if dragobj and (newpos != pos):
        pos = newpos
        dragobj.getslider(pos)
        if index <= 3: # rgb sliders
            cube.color = ball.color = panel.color = (ctrl[0].value,ctrl[1].value,ctrl[2].value)
            cube.opacity = ball.opacity = panel.opacity = ctrl[3].value
            hsv = color.rgb_to_hsv(ball.color)
            for nn in range(3):
                ctrl[nn+4].setslider(hsv[nn])
        else: # hsv sliders
            rgb = color.hsv_to_rgb((ctrl[4].value,ctrl[5].value,ctrl[6].value))
            cube.color = ball.color = panel.color = rgb
            cube.opacity = ball.opacity = panel.opacity = ctrl[3].value
            for nn in range(3):
                ctrl[nn].setslider(rgb[nn])

