from visual import *
# demonstration of vector cross product

print("""
Vector cross product: Red cross Green = Yellow
Drag to change green vector
Click to toggle fixed angle or fixed length
""")

# Ruth Chabay

scene.title="Vector Cross Product"
scene.width=600
scene.height=600
R = 0.15*4
plane = curve(pos=[(0, -10, -10), (0, -10, 10), (0, 10,10), (0, 10, -10),
              (0, -10, -10), (0,-6,-10), (0,-6,10), (0, -2, 10), (0, -2, -10),
              (0,2,-10), (0,2,10), (0,6,10), (0,6,-10),(0,10, -10),              
              (0,10,-6), (0,-10,-6), (0,-10,-2), (0,10,-2), (0,10,2),
              (0,-10,2), (0,-10,6), (0,10,6)])

s_theta=sphere(pos=(0,-12,-10), radius=0.6, color=(0.6, 1.0, 0.6))
s_theta_label=label(pos=s_theta.pos, text="Fix Angle", yoffset=-5,
                    opacity=0, box=0, line=0)
s_length=sphere(pos=(0,-12,10), radius=0.6, color=(0.6, 0.6, 1.0))
s_length_label=label(pos=s_length.pos, text="Fix Length", yoffset=-5,
                    opacity=0, box=0, line=0)

s_text=label(pos=(0,12,0), text="Yellow = Red x Green",
                    opacity=0, box=0, line=0)
               
fixlength = 0
fixtheta = 0

avector = array ([0,0,-3.5])
bvector = vector (0,3,2)

a = arrow(pos=(0,0,0), shaftwidth=R, color=color.red)
b = arrow(pos=(0,0,0), axis=bvector, shaftwidth=R, color=color.green)
a.axis =avector
cvector = cross(avector,bvector)
c = arrow(pos=(0,0,0), axis=cvector, shaftwidth=R, color=color.yellow)

scene.autoscale = 0
scene.forward = (-1,-.5,-1)

drag = 0

while True:
    rate(100)
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.drag:
            drag = True
            obs = None
        elif m.drop:
            drag = False
        elif m.click:
            if m.pick is s_length:
                if fixtheta:
                    fixtheta = not(fixtheta)
                    s_theta.color = (0.6, 1.0, 0.6)
                fixlength=not(fixlength)
                if fixlength:
                    s_length.color=(0.0, 0.0, 1.0)
                else:
                    s_length.color=(0.6, 0.6, 1.0)
            elif m.pick is s_theta:
                if fixlength:
                    fixlength = not(fixlength)
                    s_length.color=(0.6, 0.6, 1.0)
                fixtheta = not(fixtheta)
                if fixtheta:
                    s_theta.color=(0.0, 1.0, 0.0)
                else:
                    s_theta.color = (0.6, 1.0, 0.6)
    if drag:
        rate(100)
        newobs=scene.mouse.project(normal=vector(1,0,0), d=0)
        if newobs and (newobs != obs):
            obs = newobs
            if not fixlength and not fixtheta:
                bvector = obs
                if bvector.mag > 20: bvector=bvector*(20/bvector.mag)
                b.axis=bvector
            elif fixlength:
                length=3.9
                bvector = length*norm(obs)
                b.axis=bvector
            elif fixtheta:
                length=mag(obs)
                bvector=length*norm(vector(0, .3, 1))
                b.axis=bvector

            cvector=cross(avector,b.axis)
            c.axis=cvector

