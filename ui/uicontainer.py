import ui
class FlowContainer(ui.View):
    """  a subclass of View that automatically flows subviews in the order they were added.
    and reflows upon resize.
    also, set a few sane defaults, and expose some of the commonly midified params in thr constructor

    """ 

    def __init__(self, 
                 background_color=(0.9, 0.9, .9), 
                 border_color=(.5, .5, .5),
                 border_width=1,
                 corner_radius=5,
                 frame=(0,0,200,200),
                 flex='WH',
                 padding=5,
                 subviews=None,
                 name=None
        ):
            """initialize view.  
            flex settings control layout.  """
            self.background_color=background_color
            self.border_color=border_color
            self.border_width=border_width
            self.corner_radius=corner_radius
            self.frame=frame
            self.flex=flex
            self.padding=padding
            self.name=name
            #monkey patch add_subview to also call layout. 
            # also accept list of subviews to add for easy initalizstion
            old_add_subview=self.add_subview
            def new_add_subview(subviews):
                if not hasattr(subviews,'__contains__'):
                    subviews=[subviews]
                for s in subviews:
                    old_add_subview(s)
                self.layout()    
                
            self.add_subview = new_add_subview 
            
            if subviews:   #accept subview list from constructor
                new_add_subview(subviews)
                
                
    def max_width(self):
        """ return max width of this view, based on parent frame and flex settings.
        if flex width is not allowed, simply return current width.
        if flex width is allowed:
            if flex left is nor allowed, max is parent width minus current left value
            if left is flex, and right is also flex, simply return parent width.
            if only left is allowe to flex, return right """

        if not 'W' in self.flex:
            return self.width
        if not 'L' in self.flex: # fix l
            if self.superview:
                return self.superview.width-self.x
            else:
                return self.width   #todo. rotation tracking to get screen width
        elif 'R' in self.flex: #L and R flex
            return self.superview.width 
        else: # l flex only
                return min(self.superview.width,self.x+self.width) 


    def layout(self):
        """layout subviews. called whenever subviews change or view resizes.
        not, currently property observers dont work, so subview resize wint relayout this view
        Loop over children, adding each to the right, as long as it fits in  the frame.
          if a child doesnt fit, increase width, as allowed by flex settings.
          once max width is reached, start adding to next row.  each row is sized to the tallest item in the row.
          currently only top alignment is supported """
          
        rowheight=0
        currow=0
        curpt=[self.padding,self.padding] #starting top left
        w=h=0    # view's width and height, after layout completes'
        wmax=self.max_width()    #max width, per flex settings
        for s in self.subviews:
            if s.width > wmax:    # child wont fit.  resize it.
               s.width=wmax 
            if s.width + curpt[0] > wmax:    # child wont fit on this row, so add a new row
                currow += 1
                curpt[0]=self.padding
                curpt[1]+=rowheight
                rowheight=s.height+self.padding
            #add child to curr row by adjusting child position
            s.x = curpt[0]
            s.y = curpt[1]
            curpt[0]+=s.width+self.padding
            w=max(curpt[0],w)    #keep track of max width per row
            if s.height + self.padding > rowheight: #update rowheight if needed
                rowheight=s.height+self.padding
            # todo: ideally we'd allow top, bottom, or middle valign, which would require recentering subviews in each row '

        h=curpt[1]+rowheight    #keep track of veiw's height'
        #okay, now we have new width, new height.  new frame depends on flex.
        self.flex_resize(w,h)
        
        
    def flex_resize(self,w,h):
        """ resize this view, honoring flex settings"""
        oldframe=self.frame
        
        if 'W' in self.flex:
            self.width=w
        if 'H' in self.flex:
            self.height=h
        if not 'L' in self.flex:
            pass
            # dont change x
        elif 'R' in self.flex: #R and L flexing, probably should do this proportionally. instead just keep center fixed
            self.x=oldframe[0]+oldframe[2]/2-self.width/2
        else: #flex l only.. keep right fixed
            self.x=oldframe[0]+oldframe[2]-self.width
            
            
            
if __name__=="__main__":
    # few examples
    import console
    
    # set up a view
    v=ui.View()    
    v.add_subview(ui.Switch(frame=(400,5,50,20),name='switch'))
    t=ui.Label(frame=(450,5,200,20))
    t.text='random sizes'
    v.add_subview(t)
    
    f=FlowContainer()
    v.add_subview(f)
    v.present('panel')  #to set screensize
    
    f.flex='hw'
    f.frame=(0,50,0,0)  #auto size to fit contents
    t=ui.Label(frame=(15,25,500,25))

    t.text='height and width flex'
    v.add_subview(t)
    
    
    f2=FlowContainer()
    v.add_subview(f2)
    f2.flex='whl'
    f2.frame=(50,250,500,100)  #fixed size
    t=ui.Label(frame=(15,225,500,25))
    t.text='height and width flex, flex left'
    v.add_subview(t)
    
    
    f3=FlowContainer()
    v.add_subview(f3)
    f3.flex=''
    f3.frame=(50,450,400,300)  #fixed size
    t=ui.Label(frame=(15,425,500,25))
    t.text='fixed size'
    v.add_subview(t)
    
    
    def addbut(sender,toview):
        root=sender
        while root.superview:
            root=root.superview
        #add a button to parent view
        import random,string
        if root['switch'].value:
            w=random.randrange(30,110)
            h=random.randrange(20,75)
        else:
            w=40
            h=40
        title=string.ascii_letters[random.randint(0,26)]
        for v in toview:
            b=ui.Button(frame=(0,0,w,h),bg_color=(.8,.8,.8))
            b.border_width=1
            b.border_color=(0,0,0)
            b.corner_radius=10
            b.title=title
            b.action=lambda sender:addbut(sender,toview)
            v.add_subview(b)
    
    addbut(v,[f,f2,f3])
    t=ui.Label(frame=(100,100,400,200))
    t.bg_color=(0,1,1,.75)
    t.text='instructions:  push button to add more buttons. rotate screen to see how flow changes.  adjust switch to generate random size buttons'
    t.line_break_mode=ui.LB_WORD_WRAP
    t.number_of_lines=0

    t.present('popover',popover_location=(50,150))

    t.bounds=(35,35,t.width-70,t.height-70)

