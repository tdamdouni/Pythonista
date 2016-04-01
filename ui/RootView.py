import ui

class RootView(ui.View):
    def __init__(self):
        '''Children must call RootView.__init__(self), in order to set up hidden webview!'''
        self.__w=ui.WebView(frame=(1,1,1,1))
        self.add_subview(self.__w)
        
    @staticmethod
    def convert_point(point=(0,0),from_view=None,to_view=None):
        '''fixed convert point for fullscreen application.
        works for any present type
        existing function in fullscreen reports relative to portrait
        TODO: does not work if from_view or to_view has been Transformed'''

        (w,h)=ui.get_screen_size()

        #detect what convert_point things rotation is.
        origin=ui.convert_point((0,0),from_view,to_view )
        xaxis=ui.convert_point((1,0),from_view,to_view )
        xaxis=[xaxis[j]-origin[j] for j in (0,1)]
        yaxis=ui.convert_point((0,1),from_view,to_view )
        yaxis=[yaxis[j]-origin[j] for j in (0,1)]
        pt_c=ui.convert_point(tuple(point),from_view,to_view)
        pt=[0,0]

        if from_view is not None:
            pt[0]=( (xaxis[0]==-1)*h
                  + xaxis[0]*pt_c[0]
                  + (yaxis[0]==1)*w
                  - yaxis[0]*pt_c[1])

            pt[1] = ( (xaxis[1]==1)*h
                    - xaxis[1]*pt_c[0]
                    + (yaxis[1]==-1)*w
                    + yaxis[1]*pt_c[1])
        else:  #just get corrected origin, and subtract out
            origin_offset=RootView.convert_point((0,0),to_view,from_view)
            pt[0]=  point[0]  - origin_offset[0]
            pt[1]=  point[1]  - origin_offset[1]
        return tuple(pt)
        
    @staticmethod
    def convert_rect(rect=(0,0,0,0),from_view=None,to_view=None):
        pt=RootView.convert_point((rect[0],rect[1]), from_view,to_view)
        return (pt[0], pt[1], rect[2], rect[3])
        
    def get_keyboard_frame(self,frame=None):
        '''get corrected keyboard frame, in the screen coordinates.
        built in function breaks when in fullscreen, as it reports kbframe relative to a landscape screen'''
        #TODO:  remove dependence on webview, use xaxis/yaxis to determine rotation instead

        if frame is None:
            frame=ui.get_keyboard_frame()
        origin=ui.convert_point((0,0),None,self )
        xaxis=ui.convert_point((1,0),None,self )
        xaxis=[xaxis[j]-origin[j] for j in (0,1)]
        yaxis=ui.convert_point((0,1),None,self )
        yaxis=[yaxis[j]-origin[j] for j in (0,1)]

        o=self.__w.eval_js('window.orientation')

        (w,h)=ui.get_screen_size()

        if xaxis[0]==1 and yaxis[1]==1 and frame[0]==0:
            #we are not in fullscreen, just return kbframe
            fixedframe=frame
        elif o=='0':
            fixedframe= frame            #ok
        elif o=='-90':

            fixedframe= [frame[1], frame[0], h,frame[2]]
        elif o=='180':
            fixedframe= [frame[0], h-frame[1]-frame[3], frame[2],frame[3]]        #okrqq
        elif o=='90':
            fixedframe= [frame[1], w-frame[0]-frame[2],h,frame[2]]
        else:
            raise Error('UnexpectedOrientation')
        return fixedframe
        
    def get_orientation(self):
        return self.__w.eval_js('window.orientation')


if __name__=='__main__':

    class testconvert(RootView):
        def __init__(self):
            RootView.__init__(self)
            self.t1=ui.Label(frame=(0,60,400,20))
            self.t2=ui.Label(frame=(0,90,400,20))
            self.t3=ui.TextView( frame=(0,120,700,200),bg_color=(0.7,0.7,0.7,0.5))

            self.t3.text='textview for kb'
            # the first time the keyboard appears, get kbframe is wrong...
            #  so, show then hide keyboard.
            self.t3.begin_editing()
            ui.delay(self.t3.end_editing,0.5)
            # finally, show kbframe again
            ui.delay(self.t3.begin_editing,1.0)


            self.t1.text='touch to begin'
            [self.add_subview(s) for s in [self.t1,self.t2,self.t3]]

        def touch_began(self,touch):
            self.t1.text='touch in view:={} == {}'.format(touch.location, self.convert_point(self.convert_point(touch.location,self,None),None ,self))
            self.t2.text='touch in screen:={0:1}'.format(self.convert_point(touch.location,self,None))


        def draw(self):
            '''draw a green box around kb frame, padded by 10 pixels'''
            kb=self.get_keyboard_frame()
           # print kb
            kb_self=self.convert_rect(kb,None,self)
           # print kb_self
            ui.set_color((0,1,0,0.5))
            ui.fill_rect(kb_self[0]-10,kb_self[1]-10, kb_self[2]+20,kb_self[3]+20)

            self.t3.text=('orientation {}\n'
                          'kbframe       {}\n'
                          'kbframe fixed {}\n '
                          'kbframe in V  {}\n').format(self.get_orientation(),ui.get_keyboard_frame(),kb,kb_self)

        def keyboard_frame_did_change(self,frame):
            '''wait a tiny bit, then update display.
            i forget why i thought i needed the delay, maybe to ensure convert_point was updated.
            does not seem to be needed now'''
            ui.delay(self.set_needs_display,0.2)


        def touch_moved(self,touch):
            self.touch_began(touch)

    #main code
    import console
    ptype=console.alert('select present type','select one','fullscreen','panel','sheet')
    ptypes=('fullscreen','panel','sheet')
    V=testconvert()
    def show():
        V.present(ptypes[ptype-1],hide_title_bar=False   )  #works if hide is True too
        V.bg_color=(1,1,1)
    ui.delay(show,0.5) # wait until dialog is really gone
