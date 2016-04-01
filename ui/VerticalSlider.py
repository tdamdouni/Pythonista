import ui,math

class VerticalSlider(ui.View):
    '''a vertical Slider class -- identical to ui.Slider except rotated.
    To use in the pyui editor, simply add a CustomView, and set Custom View name to VerticalSlider.   in your main ui code, be sure to use 
    
    from VerticalSlider import VerticalSlider
    
    before calling ui.load_view
    '''
    def __init__(self):
        '''set up this view containing a rotated slider.  the key is to set x,y=0 after rotation'''
        self.slider=ui.Slider()
        self.add_subview(self.slider)
        self.slider.transform=ui.Transform().rotation(math.radians(90))
        self.slider.x=self.slider.y=0
    def layout(self):
        '''force internal slider to follow this Views width/height'''
        s=self.slider
        s.height,s.width=self.height,self.width
       # s.x=s.y=0 # i thought this might be needed, but it seems not to be.  
    
    # we want various View parameters to masquerade as the internal slider's.
    #   the importand ones seem to be 
    #        tint_color, bg_color, action, continuous, value
    #   though a few others like alpha, borderparameters, etc might be needed 
    #   if you plan on modifying from within the action
    @property
    def tint_color(self):
        return self.slider.tint_color
    @tint_color.setter
    def tint_color(self, value):
        self.slider.tint_color = value
 
    @property
    def bg_color(self):
        return self.slider.bg_color
    @bg_color.setter
    def bg_color(self, value):
        self.slider.bg_color = value
 
    @property
    def background_color(self):
        return self.slider.bg_color
    @background_color.setter
    def background_color(self, value):
        self.slider.bg_color = value
 
    @property
    def action(self):
        return self.slider.action
    @action.setter
    def action(self, action):
        # replace sender with self, otherwise sender.superview would return this object!
        self.slider.action = lambda sender:action(self)

    @property
    def continuous(self):
        return self.slider.continuous
    @continuous.setter
    def continuous(self, value):
        self.slider.continuous = value

    @property
    def value(self):
        return self.slider.value
    @value.setter
    def value(self, value):
        self.slider.value = value
        
if __name__=='__main__':
    root=ui.View()
    lbl=ui.Label(name='value')
    lbl.text='0.00'
    lbl.frame=(150,0,100,100)
    vs=VerticalSlider()
    vs.frame=(50,0,50,400 )
    def update(sender):
        sender.superview['value'].text=str(sender.value)
    vs.action=update
    vs.bg_color='red'
    vs.tint_color='green'
    root.add_subview(lbl)
    root.add_subview(vs)   
    root.present('panel')     
    
