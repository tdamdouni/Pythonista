from pylab import *
#from visual import vector, dot, mag


## mark out the pitch
xlist=linspace(0,50.0,500)
ylist=linspace(-35.0, 35.0, 350)
X,Y = meshgrid(xlist, ylist)


lg=7.32 #goal length

#penalty box length
pboxy=lg+2*16.5
pboxx=16.5

## the x,y location of the goal posts
g1x=0
g2x=0
g1y=lg/2
g2y=-lg/2

#the vector location from ball to goals
r1x=g1x-X
r2x=g2x-X
r1y=g1y-Y
r2y=g2y-Y

#manual dot product
dotpro=r1x*r2x+r1y*r2y
magr1=sqrt(r1x**2+r1y**2)
magr2=sqrt(r2x**2+r2y**2)
Z=arccos(dotpro/(magr1*magr2))


## this goes and sets Z to zero inside penalty box
for i in range(len(Z[:,0])):
    for j in range(len(Z[0,:])):
    
        if X[i,j]<16.5 and abs(Y[i,j])<16.5:
            Z[i,j]=0.

figure()
#CP1=contour(X,Y,Z)
#clabel(CP1, inline=True, fontsize=10)

CP2=contourf(X,Y,Z)
colorbar(CP2)
xlabel('x [m]')
ylabel('y [m]')
grid(True)
show()
