from __future__ import print_function
# @ui
# https://gist.github.com/jsbain/1cf350e92bb5f59706ca
# example of custom touch dispatch module
import ui

# wrapper class for Touch, since ui.Touch is readonly
class Touch(object):
    def __init__(self,touch):
        self.location=touch.location
        self.touch_id=touch.touch_id
        self.phase=touch.phase
        self.prev_location=touch.prev_location
        self.timestamp=touch.timestamp


class TouchDispatcher(ui.View):
    def __init__(self,name='root',bg_color='blue'):
        self.multitouch_enabled=True
        self.bg_color=bg_color
        self.name=name

    def touch_began(self,touch):
        # ideally would check hits, and dispatch if needed
        # for multitouch, need to keep internal data base of active touches, since this gets called for each touch....
        print('began', self.name, touch.touch_id)
        self.lasttouch=touch
        
    def touch_moved(self,touch):
        # ideally would check hits, and dispatch if needed, such as to scrollview
        # note for multitouch we need something complex here.
        print('moved',self.name, touch.touch_id)
        self.lasttouch=touch
        
    def touch_ended(self,touch):
        # dispatch whatever is under the touch
        # for multitouch probably only want to execute when there are no active touches left.
        # this method would need to clean out touches, but still keep info on the active gesture.  when there are no active touches left, then kill the gesture
        # for now.... just look under the touch, and call something appropriate.
        # need to handle each ui type!
        print(self.name, 'touch ended')
        for s in self.subviews:
            #probably need to check whether another view is on top...
            if TouchDispatcher.hit(s,ui.convert_point(touch.location,self,s)):
                if isinstance(s,ui.TextField):
                    print('..textfield begin editing')
                    s.begin_editing()
                    #think about setting cursor.... HARD! but possible i think?
                elif isinstance(s, ui.Button):
                    print('..button launch')
                    s.action(s)
                elif isinstance(s, TouchDispatcher):
                    # adjust touch location to subviews coordinates, then dispatch
                    print('..touch end: dispatch: ', s.name)
                    t=Touch(touch)
                    t.location=ui.convert_point(touch.location,self,s)
                    s.touch_ended(t)

    @staticmethod
    def hit(uiobj,location):
        ''' check if location is inside uiobj's bounds'''
        if location[0]<0 or location[1]<0 or location[0]>uiobj.width or location[1]>uiobj.height:
            return False
        else :
            return True
     
        
if __name__=='__main__':
    v=TouchDispatcher(name='root')
    
    #populate some contents
    b=ui.Button(frame=(10,10,100,100),bg_color='red',name='button1')
    b.title='press'
    t=ui.TextField(frame=(110,10,300,50),bg_color='white')
    v.add_subview(t)
    def myaction(sender):
        print(sender.name,' pressed')
    b.action=myaction
    v.add_subview(b)
    
    #create a second dispatcher to demonstrate trickle down
    v2=TouchDispatcher(name='second_view',bg_color='cyan')
    v2.frame=(200,200,300,300)
    b=ui.Button(frame=(10,10,100,100),bg_color='red',name='button2')
    b.title='press'
    b.action=myaction
    t=ui.TextField(frame=(110,10,300,50),bg_color='white')
    v2.add_subview(t)
    v2.add_subview(b)
    
    v.add_subview(v2)
    
    #important!  create overlay generic view, which hides events from the buttons,etc, and instead forces the underlying TouchDispatcher to handle.
    # TODO.. add the overlay to init, then override add_subview, such that overlay is brought to front after any other subviews are added.
    overlay=ui.View(frame=v.frame, name='overlay',bg_color=None) #transparent view
    overlay.flex='wh'
    v.add_subview(overlay)
    
    v.present('sheet')