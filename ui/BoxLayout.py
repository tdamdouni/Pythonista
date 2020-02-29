from __future__ import print_function
import ui
class hBoxLayout(ui.View):
    def __init__(self,subviews=None,flex=''):
        print('hb init')
        self.padding=10
        self.originalSizes=[]
        self._flex=flex
        self.border_color=(0,0,1)
        self.border_width=2
        self.height=0
        if subviews:
            self.add_subview(subviews)
            

    def add_subview(self,subviews):
        if not hasattr(subviews,'__contains__'):
            subviews=[subviews]
        for s in subviews:
            self.originalSizes.append(s.frame[2:3])
            ui.View.add_subview(self,s)
        self.layout()
            
    def layout(self):
        print('hlay',self.width, self.height)
        # first, compute total width needed for existing 
        needed_width=sum( [s[0] for s in self.originalSizes])
        flex_count=sum([1 for s in self.subviews if s.flex.find('W')>=0])
        fixed_width=sum([s.width if s.flex.find('W')<0 else 0 for s in self.subviews ])
        flex_width=(self.width - fixed_width-(len(self.subviews)+1)*self.padding)
        max_height=max([s.height for s in self.subviews]+[self.height])
        #self.height=max_height+2*self.padding
        x=self.padding
        for s in self.subviews:
            s.x=x
            if s.flex.find('W')>=0:
                s.width=float(flex_width)/flex_count
            if s.flex.find('H')>=0:
                s.height=max_height
            print(s.width)
            x=x+s.width+self.padding
            #set height settings, max_height
        self.width=x
        print('hlayout done', max_height)

class vBoxLayout(ui.View):
    def __init__(self, subviews=None):
        self.padding=10
        self.originalSizes=[]
        self.lastsize=(self.width,self.height)
        if subviews:
            self.add_subview(subviews)
        self.border_color=(0,1,0)
        self.border_width=2
    def add_subview(self,subviews):
        if not hasattr(subviews,'__contains__'):
            subviews=[subviews]
        _hidden=self.hidden
        self.hidden=True
        for s in subviews:
            self.originalSizes.append(s.frame[2:])
            print('bf add')
            ui.View.add_subview(self,s)

        self.hidden=_hidden
            #self.originalSizes.append(s.frame[2:])
        print('bf lay')
        self.layout()
            
    def layout(self):
        # first, compute total width needed for existing 
        print('vlay',self.width, self.height)
        needed_height=sum( [s[1] for s in self.originalSizes])
        flex_count=sum([1 for s in self.subviews if s.flex.find('H')>=0])
        fixed_height=sum([s.height if s.flex.find('H')<0 else 0 for s in self.subviews ])
        flex_height=(self.height - fixed_height-(len(self.subviews)+1)*self.padding)
        max_width=max([s.width for s in self.subviews]+[self.width])
        self.width=max_width+2*self.padding
        y=self.padding
        for s in self.subviews:
            s.y=y
            if s.flex.find('H')>=0:
                s.height=float(flex_height)/flex_count
            if s.flex.find('W')>=0:
                s.width=max_width
            #print s.width
            y=y+s.height+self.padding
            #set height settings
        self.height=y
        print('vlay done', len(self.subviews))
  
            
if __name__=='__main__':
    from uiCheckBox import CheckBox
    root=ui.View()
    root.present('sheet')
    vbox=vBoxLayout()
    vbox.frame=(0,0,root.width,root.height)
    vbox.flex=''
    root.add_subview(vbox)
    vbox.hidden=True
    #set up hBox for each row, checkbox, textfield
    vbox.add_subview([
                      hBoxLayout([CheckBox(),ui.TextField(frame=(0,10,200,30),bg_color=(1,0,0))],flex='h'),
                      hBoxLayout([CheckBox(),ui.TextField(frame=(0,0,200,30),bg_color=(1,0,0))],flex='h')])
    vbox.hidden=False
    print('add done')
    
    b=ui.Button(bg_color=(1,0,0))

    b.width=50
    b.height=50
    b.flex=''
    vbox.add_subview(b)
    b=ui.Button(bg_color=(0.5,0.5,0))

    b.width=50
    b.height=50
    b.flex=''
    vbox.add_subview(b)

