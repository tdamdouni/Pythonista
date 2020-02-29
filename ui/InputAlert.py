from __future__ import print_function
import ui
class InputAlert(ui.View):
    '''a ui that is added to the root view of a class, as a subview.
    call input_alert() to simulate a modal dialog.
    if cancel is selected, returns None.
    note that input_alert must be called in a background thread, since it does not return until the dialog is closed.
    
    also, note if view is closed while dialog is open, the dialog still returns.'''
    def __init__(self):
        from threading import Event
        self.e=Event()
        self.width=1
        self.height=1
    def input_alert(self,title='', 
                    message='', 
                    input='', 
                    ok_button_title='ok', 
                    hide_cancel_button=False):
        #first, cover up view
        #then 
        
        from threading import Timer
        print(threading.enumerate())
        from thread import interrupt_main
        self.e.clear()
        for s in self.subviews:
            self.remove_subview(s)
            
        if self.superview:
            dim=ui.View(frame=(0,0,self.superview.width, self.superview.height), bg_color=(0.5, 0.5, 0.5, 0.75))
            
            inputbox=ui.View()
            inputbox.width=300
            inputbox.corner_radius=10
            inputbox.bg_color='white'
            inputbox.border_color='black'
            inputbox.center = (dim.width/2,dim.height/2)
            
            titlelabel = ui.Label()
            titlelabel.text=title
            titlelabel.alignment=ui.ALIGN_CENTER
            titlelabel.font=('<system-bold>',14)
            titlelabel.size_to_fit()
            titlelabel.y=10
            titlelabel.x=0

            messagelabel = ui.Label()
            messagelabel.text=message
            messagelabel.alignment=ui.ALIGN_CENTER
            messagelabel.font=('<system>',12)
            messagelabel.x=0
            messagelabel.y=titlelabel.height+titlelabel.y
            messagelabel.size_to_fit()

            
            inputfield = ui.TextField()
            inputfield.text=input
            inputfield.font=('<system>',12)
            inputfield.height=titlelabel.height*1.5
            inputfield.x=0.1*inputbox.width
            inputfield.y=messagelabel.height + messagelabel.y
            inputfield.width = .8*inputbox.width
            inputfield.corner_radius=0
            inputfield.border_width=1
            inputfield.action=self.input_action
            
            buttons=ui.SegmentedControl()
            buttons.corner_radius=0
            buttons.height=30
            buttons.segments=('Cancel','Ok')
            buttons.width=titlelabel.width=messagelabel.width=inputbox.width
            buttons.width+=10
            buttons.x-=5
            buttons.y=inputfield.y+inputfield.height+10
            buttons.action = self.button_action
            
            inputbox.height = buttons.y+buttons.height-1
            dim.add_subview(inputbox)
            inputbox.add_subview(titlelabel)
            inputbox.add_subview(messagelabel)
            inputbox.add_subview(inputfield)
            inputbox.add_subview(buttons)
            self.superview.add_subview(dim)
            self.bring_to_front()
            dim.bring_to_front()
            
            self.width=dim.width
            self.height=dim.height
            def check_if_onscreen():
                if not self.on_screen:
                    self.e.set()
                else:
                    Timer(0.25,check_if_onscreen).start()
            check_if_onscreen()
            self.e.wait()
            self.superview.remove_subview(dim)
            if not hide_cancel_button and buttons.selected_index==0:
                rtnvalue=None
                self.width=1
                self.height=1
                interrupt_main()
                self.e.set()

            else:
                rtnvalue=inputfield.text
            self.width=1
            self.height=1
            return rtnvalue
    def button_action(self,sender):
        self.e.set()
    def input_action(self,sender):
        self.e.set()
    def get_top_view(self):
        '''find root window'''
        #find root window
        root=self
        while root.superview:
            root=root.superview
        return root
if __name__=='__main__':
    v=ui.View(frame=(0,0, 500, 600))
    b=ui.Button(frame=(20,20,100,100),bg_color='blue')

    v.add_subview(b)
    v.present('sheet')
    i=InputAlert()
    v.add_subview(i)
#b.bring_to_front()
    @ui.in_background
    def ia(sender):
        #print threading.current_thread()
        #print 'push'
        b.bg_color= i.input_alert('enter a color','valid coloname','green')
    b.action=ia
    b.title='push'


