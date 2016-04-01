from visual.graph import *

# Using a graph-plotting module

# If xmax, xmin, ymax, or ymin specified, the related axis is not autoscaled
# Can turn off autoscaling with
#    oscillation.autoscale[0]=0 for x or oscillation.autoscale[1]=0 for y
oscillation = gdisplay(xtitle='Time', ytitle='Response (click and drag mouse to see coordinates)')
funct1 = gcurve(color=color.cyan)
funct2 = gvbars(delta=0.5, color=color.red)
funct3 = gdots(color=color.yellow)

for t in arange(-30, 74, 1):
    funct1.plot( pos=(t, 5.0+5.0*cos(-0.2*t)*exp(0.015*t)) )
    funct2.plot( pos=(t, 2.0+5.0*cos(-0.1*t)*exp(0.015*t)) )
    funct3.plot( pos=(t, 5.0*cos(-0.03*t)*exp(0.015*t)) )

histo = gdisplay(title='Histogram', x=0, y=400, width=800,height=400)
datalist1 = [5, 37, 12, 21, 25, 28, 8, 63, 52, 75, 7]
data = ghistogram(bins=arange(-20, 80, 10), color=color.red)
data.plot(data=datalist1) 
datalist2 = [7, 23, 25, 72, -15]
data.plot(data=datalist2, accumulate=1)

