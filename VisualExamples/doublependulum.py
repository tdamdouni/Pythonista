from visual.graph import *

# Double pendulum

# The analysis is in terms of Lagrangian mechanics.
# The Lagrangian variables are angle of upper bar and angle of lower bar,
# measured from the vertical.

# Bruce Sherwood
#
# Corrections to the Lagrangian calculations by Owen Long, UC. Riverside
#

scene.title = 'Double Pendulum'
scene.height = scene.width = 800

g = 9.8
M1 = 2.0
M2 = 1.0
L1 = 0.5 # physical length of upper assembly; distance between axles
L2 = 1.0 # physical length of lower bar
I1 = M1*L1**2/12 # moment of inertia of upper assembly
I2 = M2*L2**2/12 # moment of inertia of lower bar
d = 0.05 # thickness of each bar
gap = 2*d # distance between two parts of upper, U-shaped assembly
L1display = L1+d # show upper assembly a bit longer than physical, to overlap axle
L2display = L2+d/2 # show lower bar a bit longer than physical, to overlap axle

hpedestal = 1.3*(L1+L2) # height of pedestal
wpedestal = 0.1 # width of pedestal
tbase = 0.05 # thickness of base
wbase = 8*gap # width of base
offset = 2*gap # from center of pedestal to center of U-shaped upper assembly
top = vector(0,0,0) # top of inner bar of U-shaped upper assembly
scene.center = top-vector(0,(L1+L2)/2.,0)

theta1 = 2.1 # initial upper angle (from vertical)
theta2 = 2.4 # initial lower angle (from vertical)
theta1dot = 0 # initial rate of change of theta1
theta2dot = 0 # initial rate of change of theta2

pedestal = box(pos=top-vector(0,hpedestal/2.,offset),
                 height=1.1*hpedestal, length=wpedestal, width=wpedestal,
                 color=(0.4,0.4,0.5))
base = box(pos=top-vector(0,hpedestal+tbase/2.,offset),
                 height=tbase, length=wbase, width=wbase,
                 color=pedestal.color)
axle = cylinder(pos=top-vector(0,0,gap/2.-d/4.), axis=(0,0,-offset), radius=d/4., color=color.yellow)

frame1 = frame(pos=top)
bar1 = box(frame=frame1, pos=(L1display/2.-d/2.,0,-(gap+d)/2.), size=(L1display,d,d), color=color.red)
bar1b = box(frame=frame1, pos=(L1display/2.-d/2.,0,(gap+d)/2.), size=(L1display,d,d), color=color.red)
axle1 = cylinder(frame=frame1, pos=(L1,0,-(gap+d)/2.), axis=(0,0,gap+d),
                 radius=axle.radius, color=axle.color)
frame1.axis = (0,-1,0)
frame2 = frame(pos=frame1.axis*L1)
bar2 = box(frame=frame2, pos=(L2display/2.-d/2.,0,0), size=(L2display,d,d), color=color.green)
frame2.axis = (0,-1,0)
frame1.rotate(axis=(0,0,1), angle=theta1)
frame2.rotate(axis=(0,0,1), angle=theta2)
frame2.pos = top+frame1.axis*L1

dt = 0.00005
t = 0.

C11 = (0.25*M1+M2)*L1**2+I1
C22 = 0.25*M2*L2**2+I2

#### For energy check:
##gdisplay(x=800)
##gK = gcurve(color=color.yellow)
##gU = gcurve(color=color.cyan)
##gE = gcurve(color=color.red)

while t < 5:
    rate(1/dt)
    # Calculate accelerations of the Lagrangian coordinates:
    C12 = C21 = 0.5*M2*L1*L2*cos(theta1-theta2)
    Cdet = C11*C22-C12*C21
    a = .5*M2*L1*L2*sin(theta1-theta2)
    A = -(.5*M1+M2)*g*L1*sin(theta1)-a*theta2dot**2
    B = -.5*M2*g*L2*sin(theta2)+a*theta1dot**2
    atheta1 = (C22*A-C12*B)/Cdet
    atheta2 = (-C21*A+C11*B)/Cdet
    # Update velocities of the Lagrangian coordinates:
    theta1dot += atheta1*dt
    theta2dot += atheta2*dt
    # Update Lagrangian coordinates:
    dtheta1 = theta1dot*dt
    dtheta2 = theta2dot*dt
    theta1 += dtheta1
    theta2 += dtheta2

    frame1.rotate(axis=(0,0,1), angle=dtheta1)
    frame2.pos = top+frame1.axis*L1
    frame2.rotate(axis=(0,0,1), angle=dtheta2)
    t = t+dt

#### Energy check:
##    K = .5*((.25*M1+M2)*L1**2+I1)*theta1dot**2+.5*(.25*M2*L2**2+I2)*theta2dot**2+\
##        .5*M2*L1*L2*cos(theta1-theta2)*theta1dot*theta2dot
##    U = -(.5*M1+M2)*g*L1*cos(theta1)-.5*M2*g*L2*cos(theta2)
##    gK.plot(pos=(t,K))
##    gU.plot(pos=(t,U))
##    gE.plot(pos=(t,K+U))

