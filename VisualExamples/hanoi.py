from visual import *
## ruth chabay, carnegie mellon university, 2000-06
## rings may be dragged through stuff - a little surreal

scene.width=800
scene.title="Tower of Hanoi"
print("Move the stack to the white pole.")

maxradius=2.5
thick=.5
spacing=maxradius+thick
leftpole=cylinder(pos=(-2*spacing,-3,0), radius=0.3, axis=(0,6,0))
leftpole.color=(.5,.5,.5)
midpole=cylinder(pos=(0,-3,0), radius=0.3, axis=(0,6,0))
midpole.color=(.5,.5,.5)
rightpole=cylinder(pos=(2*spacing,-3,0), radius=0.3, axis=(0,6,0))
floor=box(pos=(0,-3.5,0), size=(23,.99,5),
          color=(1.0,0.5,0), material=materials.wood)

poles=[leftpole,midpole,rightpole]
rings=[]
hues=[(1,0,0), (1,1,0), (0,1,0), (.3,.3,1), (1,0,1)]

for y in arange(-2, 3,1):
    rings.append(ring(pos=(poles[0].x,y,0), radius=.5*(3-y), color=hues[y+2],
                      thickness=thick,axis=(0,1,0)))

stack=[rings[:],[],[]]      # list of rings on each pole
scene.autoscale=0
moves=0

while True:
    rate(100)
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.drag:  # identify pole clicked on
            mx=m.project(normal=vector(0,0,1)).x
            pole1=int((mx+floor.length/2.)/(floor.length/3.))
            # pick up a ring
            if len(stack[pole1])>0:
                select=stack[pole1][-1]     # remove ring from stack
                del(stack[pole1][-1])
                while not (scene.mouse.events and scene.mouse.getevent().drop):      # drag ring
                    select.pos=scene.mouse.project(normal=vector(0,0,1))
                    rate(60)
                mx=select.x
                pole2=int((mx+floor.length/2.)/(floor.length/3.))
                # put down a ring
                if len(stack[pole2])>0:      # stack not empty
                    if stack[pole2][-1].radius > select.radius:  # legal move
                        select.x=poles[pole2].x
                        select.y=-2+len(stack[pole2])
                        stack[pole2].append(select)
                        moves=moves+1
                    else:       # illegal move
                        select.x=poles[pole1].x
                        select.y=-2+len(stack[pole1])
                        stack[pole1].append(select)
                else:           # stack empty
                    select.x=poles[pole2].x
                    select.y=-2
                    stack[pole2].append(select)
                    moves=moves+1
        if len(stack[2])==5:    # task completed?
            print("You won in ",moves," moves.")
            flash=0
            while flash < 6:
                rightpole.color=(1,0,0)
                rate(10)
                rightpole.color=(1,1,1)
                rate(10)
                flash=flash+1
            break
