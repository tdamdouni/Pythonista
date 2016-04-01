## 3-D tictactoe   Ruth Chabay 2000/05

from visual import *
from tictacdat import *

scene.width=600
scene.height=600
scene.title="3D TicTacToe: 4 in a row"

# draw board
gray = (1,1,1)
yo=2.       
base=grid (n=4, ds=1, gridcolor=gray)
base.pos=base.pos+vector(-0.5, -2., -0.5)

second=grid(n=4, ds=1, gridcolor=gray)
second.pos=second.pos+vector(-0.5, -1., -0.5)
third=grid(n=4, ds=1, gridcolor=gray)
third.pos=third.pos+vector(-0.5, 0, -0.5)
top=grid(n=4, ds=1, gridcolor=gray)
top.pos=top.pos+vector(-0.5, 1., -0.5)

# get list of winning combinations
wins=win()

print("****************************************")
print("Drag ball up starting from bottom grid.")
print("Release to deposit ball in a square.")
print("****************************************")
print("  ")

# make sliders
bars={}
balls={}
for x in arange(-2, 2,1):
    for z in arange(-2, 2,1):
        cyl=cylinder(pos=(x,-2,z), axis=(0,3,0), radius=0.05, visible=0)
        bars[(x,-yo,z)]=cyl

# set reasonable viewing angle
scene.center=(-.5,-.5,-.5)
scene.forward = (0,-0.05,-1)
scene.autoscale=0

nballs=0
visbar=None
red=(1,0,0)
blue=(.3,.3,1)
bcolor=red
point=None
won=None

while len(balls) < 4*4*4:
    while True:
        rate(100)
        if scene.mouse.events:
            p = scene.mouse.getevent()
            if p.drag:
                point=p.project(normal=vector(0,1,0),d=-yo)   # 'None' if not in plane
                break
            
    # chose valid square
    if not (point==None):   
        point=(round(point[0]), round(point[1]), round(point[2]))
        if not (visbar==None): visbar.visible=0
        if not (point in bars):
            continue
        visbar=bars[point]
        visbar.visible=1   
        nballs=nballs+1
        b=sphere(pos=point, radius=0.3, color=bcolor)
        while not scene.mouse.events:
            rate(100)
            y=scene.mouse.pos.y
            if y > 1.: y=1.
            if y < -yo: y=-yo
            b.y=y
        scene.mouse.getevent()  # get rid of drop depositing ball
        bpoint=(round(b.x), round(b.y), round(b.z))
        if not(bpoint in balls): # not already a ball there
            b.pos=bpoint
            balls[bpoint]=b
            if bcolor==red: bcolor=blue
            else:bcolor=red
        else:               ## already a ball there, so abort
            b.visible=0  
        visbar.visible=0
        visbar=None
        # check for four in a row
        for a in wins:
            a0=a[0] in balls
            a1=a[1] in balls
            a2=a[2] in balls
            a3=a[3] in balls
            if a0 and a1 and a2 and a3:
                ccolor=balls[a[0]].color
                if balls[a[1]].color==balls[a[2]].color==balls[a[3]].color==ccolor:
                    won=ccolor
                    print(" ")
                    if ccolor==red:
                        print("***********")
                        print(" Red wins!")
                        print("***********")
                    else:
                        print("***********")
                        print(" Blue wins!")
                        print("***********")
                    for flash in arange(0,5):
                        balls[a[0]].color=(1,1,1)
                        balls[a[1]].color=(1,1,1)
                        balls[a[2]].color=(1,1,1)
                        balls[a[3]].color=(1,1,1)
                        rate(10)
                        balls[a[0]].color=ccolor
                        balls[a[1]].color=ccolor
                        balls[a[2]].color=ccolor
                        balls[a[3]].color=ccolor
                        rate(10)
                    break
        if not (won==None):
            break

print("game over")
