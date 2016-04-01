# @ui
# https://gist.github.com/jsbain/6e4e406b07f52a68d961
import ui
class Touch(object):
    ''' writable version of ui.Touch''' 
    def __init__(self,touch):
        self.location=touch.location
        self.touch_id=touch.touch_id
        self.phase=touch.phase
        self.prev_location=touch.prev_location
        self.timestamp=touch.timestamp
        
        
class ZoomView(ui.View):
    '''view which is pinch zoomable and draggable.'''
    def __init__(self):
        self.touches={}
        self.multitouch_enabled=True
        self.bg_color='white'
        self.border=20
        
    def fix_touch(self,touch):
        '''convert to root coords. i think this doesnt quite work, '''
        t=Touch(touch)
        t.location=ui.convert_point(t.location,self,self.superview)
        t.prev_location=ui.convert_point(t.prev_location,self,self.superview)
        return t
        
    def touch_began(self,touch):
        '''keep track of touches'''
        self.touches[touch.touch_id]=self.fix_touch(touch)
        if len(self.touches.keys())==2:
            self.set_needs_display()
            self.bring_to_front()
            t0=self.touches.values()[0]
            t1=self.touches.values()[1]
            self.orig_frame=self.frame
            self.orig_touchdiff=[abs(t0.location[axis]-t1.location[axis]) for axis in range(0,2)]
            self.orig_touchavg=[abs(t0.location[axis]/2.0+t1.location[axis]/2.0) for axis in range(0,2)]
            self.orig_border=self.border_color
            self.border_color=(0.00, 0.50, 1.00) 
            self.border_width= self.border_width+3
    def touch_moved(self,touch):
        '''update touch, then determine change in pos, height and width'''
        prevtouch=self.touches[touch.touch_id]
        self.touches[touch.touch_id]=self.fix_touch(touch)
        self.touches[touch.touch_id].prev_location=prevtouch.location
        if len(self.touches.keys())==2:
            t0=self.touches.values()[0]
            t1=self.touches.values()[1]
            
            diffpos=[abs(t0.location[axis]-t1.location[axis]) for axis in range(0,2)]
            dw,dh=[diffpos[x]-self.orig_touchdiff[x] for x in (0,1)]
            
            
            avgpos=[t0.location[axis]/2.0+t1.location[axis]/2.0 for axis in range(0,2)]
            dx,dy=[avgpos[x]-self.orig_touchavg[x] for x in (0,1)] 
            
            #compute new frame
            f=list(self.orig_frame)
            f[0]=f[0]-dw/2.0+dx
            f[1]=f[1]-dh/2.0+dy
            f[2]=max(f[2]+dw,self.border*2+1)
            f[3]=max(f[3]+dh,self.border*2+1)
            self.frame=tuple(f)

        self.set_needs_display()
        
    def touch_ended(self,touch):
        '''clean up unused touch'''
        del(self.touches[touch.touch_id])
        if len(self.touches.keys())==1: 
            self.border_color=self.orig_border
            self.border_width=self.border_width-3
        self.set_needs_display()
        
    def layout():
        '''override to do more complex layout when resizing'''
        pass
        
if __name__=='__main__':
    import random
    from functools import partial
    def create_new_window(root,sender):
        v=ZoomView()
        v.bg_color=0.90, 0.90, 0.90
        v.border_color='grey'
        v.border_width=2
        v.x=random.randrange(75,300)
        v.y=random.randrange(75,300)
        v.width=v.height=300
        closebutton=ui.Button(frame=(250,0,50,50), bg_color='grey')
        closebutton.image=ui.Image.named('ionicons-close-round-32')
        closebutton.flex='bl'
        def closeview(sender):
            sender.superview.superview.remove_subview(sender.superview)
        closebutton.action=closeview
        tv=ui.TextView()
        tv.frame=(20,20,258,258)
        tv.flex='wh'
        v.add_subview(tv)
        v.add_subview(closebutton)
        root.add_subview(v)
        
    root=ui.View(bg_color=(0.00, 0.00, 0.50))
    new_button=ui.Button(title='+new window',bg_color=(0.80, 0.80, 0.80),frame=(0,0,75,75))
    new_button.action=partial(create_new_window,root)
    root.add_subview(new_button)
    root.present()
  #  v=ZoomView()