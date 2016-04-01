from visual import *

def grid(n=5, ds = 1., gridcolor = (.6, .6, .6)):
    assert n > 2, "n must be > 2"
    j=n//2
    k=j*2
    if k==n: offset=0
    else: offset = ds/2.
    grid = curve(color = gridcolor)
    for z in arange (-(j+offset)*ds, (j+offset+1)*ds, ds):
        for x in arange(-(j+offset)*ds, (j+offset+1)*ds, ds):
            grid.append(pos=(x, 0, z))
            if x == (j+offset) and not z==(j+offset):
                grid.append (pos=(-(j+offset)*ds,0,z))
                grid.append (pos=(-(j+offset)*ds,0,z+1))
    grid.append(pos=((j+offset)*ds,0,-(j+offset)*ds))
    grid.append (pos=(-(j+offset-1)*ds,0,-(j+offset)*ds))

    for x in arange (-(j+offset)*ds, (j+offset)*ds, ds):
        for z in arange (-(j+offset)*ds, (j+offset+1)*ds, 1):
            grid.append (pos=(x, 0, z))
            if z == (j+offset):
                grid.append (pos=(x,0,-(j+offset)*ds))
                grid.append (pos=(x+1, 0, -(j+offset)*ds))
    return grid

def win():    
    wins1=[]
    wins2=[]
    wins3=[]
    wins4=[]
    wins=[]

    # planar rows & columns
    for y in arange (-2,2,1):
        z=-2
        for x in arange(-2, 2,1):
            col=[(x,y,z), (x,y,z+1), (x,y,z+2), (x,y,z+3)]
            wins1.append(col)
        x=-2
        for z in arange(-2,2,1):
            row=[(x,y,z), (x+1,y,z), (x+2,y,z),(x+3,y,z)]
            wins1.append(row)

##    print "wins1"    
##    for a in arange(0,len(wins1)):
##        print wins1[a]

    # planar diagonals
    x=-2
    z=-2
    for y in arange (-2,2,1):
        wins2.append([(x,y,z), (x+1,y,z+1), (x+2,y,z+2), (x+3,y,z+3)])
        wins2.append([(x,y,z+3), (x+1,y,z+2), (x+2,y,z+1), (x+3,y,z)])

##    print "  "
##    print "wins2"
##    for a in arange(0,len(wins2)):
##        print wins2[a]

    y=-2
    # vertical columns
    for x in arange (-2,2,1):
        for z in arange (-2,2,1):
             wins3.append([(x,y,z),(x,y+1,z), (x,y+2,z), (x,y+3,z)])

##    print "  "
##    print "wins3"
##    for a in arange(0,len(wins3)):
##        print wins3[a]

    # 3d diagonals
    x=-2
    y=-2
    z=-2
    wins4.append([(x,y,z), (x+1, y+1, z+1), (x+2, y+2, z+2), (x+3,y+3,z+3)])
    z=1
    wins4.append([(x,y,z), (x+1, y+1, z-1), (x+2, y+2, z-2), (x+3,y+3,z-3)])
    x=1
    z=-2
    wins4.append([(x,y,z), (x-1, y+1, z+1), (x-2, y+2, z+2), (x-3,y+3,z+3)])
    z=1
    wins4.append([(x,y,z), (x-1, y+1, z-1), (x-2, y+2, z-2),(x-3,y+3,z-3)])

    # 3d slant
    z=-2
    y=-2
    for x in arange(-2,2,1):
        wins4.append([(x,y,z), (x,y+1,z+1), (x,y+2,z+2), (x,y+3,z+3)])
        wins4.append([(x,y,z+3), (x,y+1,z+2), (x,y+2,z+1), (x,y+3,z)])
    x=-2
    for z in arange(-2,2,1):
        wins4.append([(x,y,z), (x+1,y+1,z), (x+2,y+2,z), (x+3,y+3,z)])
        wins4.append([(x+3,y,z), (x+2,y+1,z), (x+1,y+2,z), (x,y+3,z)])
        
##    print "  "
##    print "wins4"
##    for a in arange(0,len(wins4)):
##        print wins4[a]

    wins=wins1+wins2+wins3+wins4
    return wins

##a=win()
print(" ")
print("Run 'tictac.py' to play 3D tictactoe.")

