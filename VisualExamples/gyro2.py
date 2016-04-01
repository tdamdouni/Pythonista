from visual import *

# Gyroscope sitting on a pedestal

# The analysis is in terms of Lagrangian mechanics.
# The Lagrangian variables are polar angle theta,
# azimuthal angle phi, and spin angle alpha.

# Bruce Sherwood

scene.width=800
scene.height=800
scene.title='Nutating Gyroscope'

Lshaft = 1. # length of gyroscope shaft
r = Lshaft/2. # distance from support point to center of mass
Rshaft = 0.03 # radius of gyroscope shaft
M = 1. # mass of gyroscope (massless shaft)
Rrotor = 0.4 # radius of gyroscope rotor
Drotor = 0.1 # thickness of gyroscope rotor
Dsquare = 1.4*Drotor # thickness of square that turns with rotor
I = 0.5*M*Rrotor**2. # moment of inertia of gyroscope
hpedestal = Lshaft # height of pedestal
wpedestal = 0.1 # width of pedestal
tbase = 0.05 # thickness of base
wbase = 3.*wpedestal # width of base
g = 9.8
Fgrav = vector(0,-M*g,0)
top = vector(0,0,0) # top of pedestal

theta = pi/3. # initial polar angle of shaft (from vertical)
thetadot = 0 # initial rate of change of polar angle
alpha = 0 # initial spin angle
alphadot = 15 # initial rate of change of spin angle (spin ang. velocity)
phi = -pi/2. # initial azimuthal angle
phidot = 0 # initial rate of change of azimuthal angle
## Comment in the following statements to get pure precession
##if abs(cos(theta)) < 1e-8:
##    phidot = M*g*r/(I*alphadot)
##else:
##    phidot = (-alphadot+sqrt(alphadot**2+2*M*g*r*cos(theta)/I))/cos(theta)

pedestal = box(pos=top-vector(0,hpedestal/2.,0),
                 height=hpedestal, length=wpedestal, width=wpedestal,
                 color=(0.4,0.4,0.5))
base = box(pos=top-vector(0,hpedestal+tbase/2.,0),
                 height=tbase, length=wbase, width=wbase,
                 color=pedestal.color)

gyro=frame(axis=(sin(theta)*sin(phi),cos(theta),sin(theta)*cos(phi)))
shaft = cylinder(axis=(Lshaft,0,0), radius=Rshaft, color=(0,1,0),
                 material=materials.rough, frame=gyro)
rotor = cylinder(pos=(Lshaft/2 - Drotor/2, 0, 0),
                 axis=(Drotor, 0, 0), radius=Rrotor, color=(1,0,0),
                 material=materials.rough, frame=gyro)

trail = curve(radius=Rshaft/8., color=(1,1,0))

dt = 0.000005
t = 0.
Nsteps = 300 # number of calculational steps between graphics updates

while True:
    rate(200)
    for step in range(Nsteps): # multiple calculation steps for accuracy
        # Calculate accelerations of the Lagrangian coordinates:
        atheta = (phidot**2*sin(theta)*cos(theta)
                  -2.*(alphadot+phidot*cos(theta))*phidot*sin(theta)
                  +2.*M*g*r*sin(theta)/I)
        aphi = 2.*thetadot*(alphadot-phidot*cos(theta))/sin(theta)
        aalpha = phidot*thetadot*sin(theta)-aphi*cos(theta)
        # Update velocities of the Lagrangian coordinates:
        thetadot = thetadot+atheta*dt
        phidot = phidot+aphi*dt
        alphadot = alphadot+aalpha*dt
        # Update Lagrangian coordinates:
        theta = theta+thetadot*dt
        phi = phi+phidot*dt
        alpha = alpha+alphadot*dt

    gyro.axis = vector(sin(theta)*sin(phi),cos(theta),sin(theta)*cos(phi))
    # Display approximate rotation of rotor and shaft:
    gyro.rotate(angle=alphadot*dt*Nsteps)
    trail.append(pos=gyro.pos + gyro.axis * Lshaft)
    t = t+dt*Nsteps
