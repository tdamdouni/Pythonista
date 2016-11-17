# https://forum.omz-software.com/topic/3321/use-objc_util-functions-to-draw-on-a-ui-view/2

import ui,time
from objc_util import *
# create a view
v=ui.View()
v.bg_color='white'
vv=ObjCInstance(v)

# grab view's layer
layer=vv.layer()

# add a shapelayer
CAShapeLayer=ObjCClass('CAShapeLayer')
shlayer=CAShapeLayer.layer()
shlayer.frame=layer.bounds()
layer.addSublayer_(shlayer)

# add some stuff to the shapelayer, using a ui.Path
p=ui.Path.rounded_rect(5,5,80,80,22)
shlayer.path=ObjCInstance(p).CGPath()

#stroke it
shlayer.strokeColor = UIColor.colorWithRed(0.75,green=0.0,blue=0.0,alpha=1.0).CGColor()
shlayer.fillColor=UIColor.colorWithRed(1,green=1.0,blue=1.0,alpha=1.0).CGColor()
shlayer.lineWidth = 9
shlayer.strokeEnd=.0

#sublayer must be added before view is presented... dunno why.
v.present('sheet')

# demo.  seems to have built in default animation
time.sleep(1)
on_main_thread(lambda: shlayer.setStrokeEnd_(1))()
time.sleep(1)
on_main_thread(lambda: shlayer.setStrokeEnd_(0))()
time.sleep(1)
for i in range(30):
	on_main_thread(lambda: shlayer.setStrokeEnd_(i/29.))()
	time.sleep(.1)
	
	
# --------------------

