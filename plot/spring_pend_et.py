from pylab import *

#graph1 = gdisplay(title='Vertical Position vs. Time', xtitle ='t (sec)', ytitle ='y (m)', background=color.white)
#funct1=gcurve(color=color.white)

#floor = box (pos=(0,0,0), length=.4, height=0.05, width=.4, color=color.blue)

L = 120
theta0 = -pi/2
#ball2=sphere()
ball = array([L*sin(theta0), -L*cos(theta0),0])
m =70
pivot=array([0,0,0])
AC=.3
rho=1.2



k=5000
dt=0.0001

g = array([0,-9.8,0])

def mag(vec1):
    #this function takes a vector (array) and returns a magnitude
    return sqrt(vec1[0]**2+vec1[1]**2+vec1[2]**2)

F=m*g-k*(ball-pivot)*(mag(ball-pivot)-L)/mag(ball-pivot)
ballp=array([0,0,0])
t=0


#set up plotting
plotx=[]
plott=[]
ploty=[]
plotx2=[]
ploty2=[]
plotw=[]

#here is the stuff to plot the analytical solution-ish
theta = theta0
thetadot=0
thetaddot=-mag(g)*sin(theta)/L
y2=-L*cos(theta)
x2=L*sin(theta)


while t<8:
    #rate(100)
    F=m*g-k*(ball-pivot)*(mag(ball-pivot)-L)/mag(ball-pivot)-.5*rho*AC*mag(ballp)*ballp/m**2
    Fapp = F-m*g
    ballp=ballp + F*dt
    ball = ball +ballp*dt/m

    #euler method for analytical pendulum
    thetaddot=-mag(g)*sin(theta)/L
    thetadot=thetadot+thetaddot*dt
    theta=theta+thetadot*dt
    y2=-L*cos(theta)
    x2=L*sin(theta)
    ploty2=ploty2+[y2]

    t = t+dt
    plott=plott+[t]
    plotx=plotx+[ball[0]]
    ploty=ploty+[ball[1]]
    plotw=plotw+[mag(Fapp)/(m*9.8)]

plot(plott, ploty, linewidth=3)
grid(color='b', linestyle='-', linewidth=0.5)
#ax=gca()
#ax.set_aspect('equal')
title('Giant Swing')
xlabel('time [s]')
ylabel('Apparent Weight [g]')
show()



