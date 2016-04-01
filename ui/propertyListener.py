# @ui
# https://gist.github.com/jsbain/87cf25db0d3f1b16c512
import threading
class propertyListener(threading.Thread):
    '''create a listener on one or more of a view's properties, and dispatches a callback whenever those properties change.
    
    NOTE:  it is highly recommended that the propertyListener instance is part of s custom view class, and in that class's will_close method, call stop() on the instance.  otherwise, it will continue to poll even after the view is closed, and could cause problems later.

cosntructor args:
    view  -  the view to watch
    propertylist   -  list of properties to watch. must be a list even if only one prop, e.g ['frame']
    action     the callback to call.  the function should be of the following form
        def action(sender, propertyname, oldvalue, newvalue) or
        def action(self, sender, propertyname, oldvalue,newvalue) if in a class
    polling_time  - (default 1 second) time in seconds to poll the properties

'''
    
    def __init__(self, view, propertylist, action, polling_time=1):
        self.should_stop=False
        self.action=action
        self.view = view
        self.propertyDict = {prop:getattr(view,prop) for prop in propertylist}
        self.polling_time=polling_time
        threading.Thread.__init__(self)
        self.start()
    def run(self):
        '''overrides Thread.run to do what we want'''
        import time
        while not self.should_stop:
            for prop in self.propertyDict.keys():
                newvalue=getattr(self.view,prop)
                oldvalue=self.propertyDict[prop]
                if newvalue != oldvalue:
                    self.action(self.view,prop,oldvalue,newvalue)
                    self.propertyDict[prop]=newvalue
            time.sleep(self.polling_time)
        threading.Thread.__init__(self) # allow restart after stop
        
    def stop(self):
        ''' stops the listener. should always call stop when done with the view!'''
        self.should_stop = True 

if __name__=='__main__':
    # example usage:  
    #from propertListener import propertyListener

    import console
    import ui
    class myView(ui.View):
        def __init__(self):
            self.present('sheet')
            v1=ui.View(frame=(0,0,300,300),bg_color='white')
            n=ui.NavigationView(v1)
    
            self.add_subview(n)
            
    
    
            def myaction(sender,prop, oldvalue,newvalue):
                console.hud_alert('{}={}'.format(prop,newvalue))
            self.p=propertyListener(v1,['on_screen'],myaction,polling_time=0.25)
            
            def pushnew(sender):
                n.push_view(ui.View(bg_color='yellow',frame=(0,0,400,400)))
    
            b1=ui.Button(frame=(100,100,100,100),bg_color='red')
            b1.action=pushnew
            v1.add_subview(b1)
            n.size_to_fit()
    
        def will_close(self):
            self.p.stop()
            console.hud_alert('stopped')
            
    myView()