from __future__ import print_function
import ui, threading, time
from uicontainer import FlowContainer
from threading import Timer
#from initializer import initializer


class PopupButton (ui.View):
    # a button like class, which allows for long touch popup
#    @initializer
    def __init__(self,
                 frame=(0, 0, 40, 40),
                 title='',
                 flex='',
                 background_color=(.8,.8,.8),
                 longtouch_delay=0.5,
                 touch_enabled=True,
                 border_color=(0,0,0),
                 border_width=1,
                 corner_radius=10,
                 action=(lambda sender:None),
                 childButtons=[],
                 font=('HelveticaNeue',26)):
        #ui props
        self.frame=frame
        self.title=title
        self.flex=''
        self.background_color=background_color
        self.longtouch_delay=longtouch_delay
        self.touch_enabled=touch_enabled
        self.border_color=border_color
        self.border_width=border_width
        self.corner_radius=corner_radius
        self.action = action
        self.multitouch_enabled=False
        self.font=font
        #custom properties
        self.doing_longtouch=False #is long touch activated
        self.touched=False         #currently touching button
        self.t =  None
        flow=FlowContainer(name='longtapbox',flex='whr')
        flow.hidden=True
        self.flow=flow
        self.content_mode=ui.CONTENT_LEFT
        for b in childButtons:
            self.add_subview(b)

    def add_subview(self,subview):
        #override add_subview to add to longtapbox
        ui.View.add_subview(self.flow,subview)
        
    def get_top_view(self):
        #find root window
        root=self
        while root.superview:
            root=root.superview
        return root

    def will_close(self):
        # This will be called when a presented view is about to be dismissed.
        # You might want to save data here.
        if self.t:
            t.stop()
        ui.cancel_delays()
        pass

    def draw(self):
        # redraw button
        def darken(color):
            return tuple([0.5*x for x in color])

        
        #set up button size to fit.
        padding=10
        textsize=ui.measure_string(string=self.title,max_width=0,font=self.font,alignment=ui.ALIGN_CENTER)

        #draw border
        ui.set_color(self.border_color)
        path = ui.Path.rounded_rect(0, 0, self.width, self.height,self.corner_radius)
        path.line_width=self.border_width
        path.stroke()
        
        #fill button, depending on touch state
        if self.touched:
            if self.doing_longtouch:
                ui.set_color('blue')
            else:
                ui.set_color('grey')
        else :
            ui.set_color(self.bg_color)
        path.fill()
        
        # fill corner darker, if has children
        if self.flow.subviews:
            corner = ui.Path()
            corner.move_to(self.width-1.5*self.corner_radius,0)
            corner.line_to(self.width,0)
            corner.line_to(self.width,1.5*self.corner_radius)
            corner.line_to(self.width-1.5*self.corner_radius,0)
            ui.set_color(darken(darken(self.bg_color)))
            corner.stroke()
            corner.fill()

        # draw title, center vertically, horiz
        rect=list(self.bounds)
        rect[1]=(rect[3]-textsize[1])/2 #vert center
        rect[2]=max(rect[2],textsize[0]+10)
        ui.draw_string(self.title, rect=tuple(rect), font=self.font, color=self.tint_color, alignment=ui.ALIGN_CENTER, line_break_mode=ui.LB_WORD_WRAP)
        
        if textsize[0]>self.bounds[2]:
            self.width=textsize[0]+10

    def layout(self):
        self.set_needs_display()
        
    def do_long_touch(self):
        if self.touched:
            self.doing_longtouch=True
            root=self.get_top_view()
            flow=self.flow
            #set popup flow as child to root, in proper location
            # root needs to be a plain view without layout manager
            myposinroot=ui.convert_point((0,0),self,root)
            flow.x=myposinroot[0]
            flow.y=myposinroot[1]
            root.add_subview(flow)
            flow.layout()
            flow.bg_color=self.bg_color
            flow.border_color=self.border_color
            flow.tint_color=self.tint_color
            flow.hidden=False
            def pop():
                flow.y=flow.y-flow.height-20
                flow.x=flow.x
            ui.animate(pop,0.05)
            self.set_needs_display()
            # add delayed cleanup of the popup, for panel mode where this deosnt behave

            self.longtouchcleanuptimer=Timer(3.0,self.longtouch_cleanup)
            self.longtouchcleanuptimer.start()


    def touch_began(self, touch):
        # Called when a touch begins.
        # set timer for longtap, which gets cancelled in touch ended
        self.touched=True
        #self.t = threading.Timer(self.longtouch_delay, self.long_touch)
        #self.t.start()
        # ececute do_long_touch after a delay
        ui.delay(self.do_long_touch, self.longtouch_delay)

        self.doing_longtouch=False
        self.set_needs_display()
        self.lastTouchTime=time.time()


    def childHits(self,location):
        location=list(location)
        location[1]-=25 # allow room for a finger, mske virtual hit point a little higher
        for s in self.flow.subviews:
            if PopupButton.hit(s,ui.convert_point(tuple(location),self,s)):
                s.bg_color=(0,0,1)
                yield s
            else :
                s.bg_color=(.8,.8,.8)

    @staticmethod
    def hit(self,location):
        if location[0]<0 or location[1]<0 or location[0]>self.width or location[1]>self.height:
            return False
        else :
            return True

    def touch_moved(self, touch):
        # Called when a touch moves.
        #if not self.doing_longtouch:
        try:
            self.longtouchcleanuptimer.cancel()
            self.longtouchcleanuptimer=Timer(3.0,self.longtouch_cleanup)
            self.longtouchcleanuptimer.start()
        except AttributeError:
            pass
        t= time.time()
        if t<self.lastTouchTime +0.1:
            # avoid running moved at too high a rate. probably not necessary
            return
        if self.doing_longtouch:
            for s in self.childHits(touch.location):
                # call hover? right now childHit sets and unsets hilite
                # so loop is needed in order to call childHit
                pass
            if not PopupButton.hit(self,touch.location):
                if self.touched: # avoid unnecessary redraw
                    self.touched=False
                    self.set_needs_display()
            else:
                if not self.touched:
                    self.touched=True
                    self.set_needs_display()
        elif not PopupButton.hit(self,touch.location):
            if self.touched :
                self.touched=False
                self.longtouch_cleanup()
                self.set_needs_display()
        elif not self.touched:
            self.touched=True
            self.doing_longtouch=False
            self.longtouch_cleanup()
            self.touch_began(touch)
        self.lastTouchTime=t




        #pass
    def longtouch_cleanup(self):
        self.get_top_view().remove_subview(self.flow)

    def touch_ended(self, touch):
        # Called when a touch ends.  if touch ended before timer, cancel it
        #self.t.cancel()
        ui.cancel_delays()
        if self.doing_longtouch:
            for  s in self.childHits(touch.location):
                s.action(s)
        if self.touched:
            #normal button action
            self.touched=False
            self.set_needs_display()
            self.action(self)
        #else:
        #    return
        self.doing_longtouch=False
        self.touched=False
        self.set_needs_display()
        self.longtouch_cleanup()



if __name__=='__main__':

    v=ui.View()
    s=ui.ScrollView()
    keyrow=FlowContainer(frame=(0,200,400,40))
    def addKey(key,altkeys,keyrow):
        def printkey(sender):
            print(key)
        b=PopupButton(title=key, action=printkey,frame=(0,0,60,60))
        keyrow.add_subview(b)
        if altkeys:
            for ak in altkeys:
                addKey(ak,None,b)

    import string,random
    for i in range(0,10):
        key=random.choice(string.ascii_letters)
        addKey(key,random.sample(string.ascii_letters, random.randrange(0,5)),keyrow)
    addKey('ABCDefghijk',None ,keyrow)
    v.add_subview(s)
    s.add_subview(keyrow)
    s.flex='Wh'
    

   # v.present('sheet')
    v.present('panel',hide_title_bar=True)
    x,y,w,h=v.frame
    s.content_size=(w+1,h+1)
