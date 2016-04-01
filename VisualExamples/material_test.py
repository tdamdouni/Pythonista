from visual import *
show_sphere = True
scene.width = scene.height = 800
    
names = ['wood', 'rough', 'marble', 'plastic', 'earth', 'diffuse', 'emissive', 'unshaded',
         'shiny', 'chrome', 'blazed', 'silver', 'bricks', 'BlueMarble', 'ice', 'glass']
lookup = {"wood" : materials.wood, "rough" : materials.rough,
         "marble" : materials.marble, "plastic" : materials.plastic,
         "earth" : materials.earth, "diffuse" : materials.diffuse,
         "emissive" : materials.emissive, "unshaded" : materials.unshaded,
         "shiny" : materials.shiny, "chrome" : materials.chrome,
         "blazed" : materials.blazed, "silver" : materials.silver,
         "bricks" : materials.bricks, "BlueMarble" : materials.BlueMarble,
          "ice" : materials.ice, "glass" : materials.glass}

def destroy():
    for obj in scene.objects:
        obj.visible = False
        del obj

def show_object(index, x, y, show_sphere):
    sphere(pos=(x,y,0), radius=R/5, color=color.red)
    mat = lookup[names[index]]
    if show_sphere:
        s = sphere(pos=(x,y,0), radius=R, material=mat, index=index)
        if names[index] == "bricks":
            s.rotate(angle=pi/2, axis=(1,0,0))
    else:
        box(pos=(x,y,0), size=(D,D,D), material=mat, index=index)
    label(pos=(x,y-.5), box=0, text=names[index])

D = 0.7 # size of box
R = .4 # radius of sphere
first = True
show = -1 # means show all the objects
while True:
    destroy()
    scene.range = 2.2
    scene.fov = 0.5
    scene.center = (1.5,1.5)
    scene.forward = (0,0,-1)
    if first: scene.visible = False
    index = 0
    for y in range(4):
        for x in range(4):
            if index >= 16: break
            show_object(index, x, 3-y, show_sphere)
            index += 1
    label(pos=(1.5,3.53), box=0,
          text="Hit a key to toggle between spheres and boxes, or click an object to enlarge it.")
    if first: scene.visible = True
    first = False
    picked = None
    while True:
        rate(30)
        if scene.mouse.events:
            m = scene.mouse.getevent()
            if m.click and picked:
                picked = None
                break
            elif m.click and m.pick:
                mouseloc = scene.mouse.project(normal=(0,0,1))
                xp, yp = (mouseloc.x, mouseloc.y)
                x, y = (m.pick.x, m.pick.y)
                if (x-xp)**2 + (y-yp)**2 < R**2:
                    picked = m.pick
                    destroy()
                    scene.center = (0,-.1*R,0)
                    scene.range = 1.5*R
                    show_object(m.pick.index, 0, 0, show_sphere)
                    label(pos=(0,1.2*R), box=0, text="Hit a key to toggle between spheres and boxes, or click to see all materials.")
        elif scene.kb.keys:
            scene.kb.getkey()
            show_sphere = (not show_sphere)
            if not picked: break
            destroy()
            scene.forward = (0,0,-1)
            show_object(m.pick.index, 0, 0, show_sphere)
            label(pos=(0,1.2*R), box=0, text="Hit a key to toggle between spheres and boxes, or click to see all materials.")
