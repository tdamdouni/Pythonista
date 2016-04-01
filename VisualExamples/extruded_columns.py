from visual import *
# Kadir Haldenbilen, February 2011, using the new extrusion object
scene.range = 4
scene.forward = (-0.55, 0.30, -0.80)
scene.width = scene.height = 800
scene.autocenter = True
scene.visible = False

def pstar(pos=(0,0,0), np=8, radius=0.02, length=0.02):
    st = shapes.triangle(length=length)
    stf = frame(pos=pos)
    est = extrusion(frame=stf, pos=paths.star(n=np, radius=radius), shape=st)
    stf.rotate(angle=pi/2)
    return est

def column(pos=(0,0,0), height=3.0, rotate=0.0):

    column = frame(pos=pos)
    col_body = shapes.ngon(radius=0.20, np=16, roundness=0.0, invert=True)
    cbe = extrusion(frame=column, pos=[(0,0,0),(0,height,0)], shape=col_body,
                    scale=[(1,1),(0.8,0.8)])

    chs = shapes.rectangle(width=0.06)
    chr = shapes.ellipse(width=0.04, height=0.04)
    cha = shapes.circle(pos=(0.02,0.02), radius=0.05)
    ch = chs-cha
    che = extrusion(frame=column, pos=paths.circle(radius=0.23), shape=ch)

    cbase = cylinder(frame=column, pos=(0,-0.33,0), radius=0.26,
                     axis=(0,height/10.0,0))
    fr1 = frame(frame=column, pos=(0,-0.09,0))
    cbr1 = extrusion(frame=fr1, pos=paths.circle(radius=0.23), shape=cha)

    fr2 = frame(frame=column, pos=(0,-0.30,0))
    cbr2 = extrusion(frame=fr2, pos=paths.circle(radius=0.23), shape=cha)

    cbd = shapes.rectangle(width=0.65, height=0.65, roundness=0.1, invert=True)
    cbf = frame(frame=column, pos=(0,-0.70,0))
    cbde = extrusion(frame=cbf, pos=[(0,0,-0.375),(0,0,0.375)], shape=cbd)
    cbs = extrusion(frame=column, pos=[(0,-1.22,0.370), (0,-1.22,0.42)],
                    scale=[(0.5,0.5), (0.5,0.5)], shape="*")
    cbf.rotate(angle=pi/2)

    def spiral(nloop=1, tightness=1.0, dir=1.0, scale=1.0):

        spr = []
        for t in range(1, 1024*nloop, 16):
            t *= 0.01
            x = tightness/10.0 * t * math.cos(t)*dir*scale
            y = tightness/10.0 * t * math.sin(t)*scale
            spr.append((x,y))

        return spr


    spiral = spiral(nloop=1, tightness=1.0, dir=1.0, scale=0.15)
    deltax = 0.0
    deltay = -0.40

    srevrs = []
    srevrs.extend(spiral)
    srevrs.reverse()
    for sp in srevrs:
        spiral.append((+sp[0]-deltax, -sp[1]+deltay))

    sfrm = frame(frame=column,pos=(0.20,3,0.20))
    sp1 = extrusion(frame=sfrm, pos=spiral, shape=chr, material=materials.rough)

    sfrm2 = frame(frame=column,pos=(0.20,3,-0.20))
    sp2 = extrusion(frame=sfrm2, pos=spiral, shape=chr, material=materials.rough)
    sp2.frame.rotate(axis=(0,0,1), angle=-pi/2)
    
    sfrm3 = frame(frame=column,pos=(0.20,3,-0.05))
    sp3 = extrusion(frame=sfrm3, pos=spiral[30:-30], shape=chr, material=materials.plastic)
    sp3.frame.rotate(axis=(0,0,1), angle=-pi/2)
    sfrm4 = frame(frame=column,pos=(0.20,3,0))
    sp4 = extrusion(frame=sfrm4, pos=spiral[30:-30], shape=chr, material=materials.plastic)
    sp4.frame.rotate(axis=(0,0,1), angle=-pi/2)
    sfrm5 = frame(frame=column,pos=(0.20,3,+0.05))
    sp5 = extrusion(frame=sfrm5, pos=spiral[30:-30], shape=chr, material=materials.plastic)
    sp5.frame.rotate(axis=(0,0,1), angle=-pi/2)
    
    
    psp = Polygon(spiral[30:-30])

    esp = extrusion(frame=sfrm, pos=[(0,0,0),(0,0,-0.4)], shape=psp, material=materials.plastic)
    esp.frame.rotate(axis=(0,0,1), angle=-pi/2)

    ctp = shapes.rectangle(width=0.30, roundness=0.2, invert=True)
    ctf = frame(frame=column, pos=(0,3.10,0))
    ctop = extrusion(frame=ctf, pos = paths.line(end=(0,0.3,0), np=7),
                     scale=[(1,1), (1.1,1.1), (1.15,1.15), (1.2,1.2), (1.3,1.3),
                            (1.5,1.5), (1.8,1.8)],
                     shape=ctp, material=materials.plastic)
    

    ps =pstar(pos=(0.0,3.05,0.20))
    ps.frame.frame = column

    column.rotate(axis=(0,1,0), angle=rotate)
    return column

bb = box(size=(5,0.2,5), pos=(0,-1.19,0))
c2 = column(pos=(-1,0,0), rotate=0)
c3 = column(pos=(+1,0,0), rotate=0)

afrm = frame(pos=(0,3.4,0))
abrg = extrusion(frame=afrm, pos=paths.arc(radius=1.0, angle1=0, angle2=pi),
                 shape=shapes.ngon(np=8, radius=0.18))
afrm.rotate(angle=pi/2)
scene.visible = True
