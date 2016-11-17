# https://forum.omz-software.com/topic/3379/share-interactive-matplotlib-backend/6 

import ui

class MyClass(ui.View):
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)   
        self.make_view()
        
    def make_view(self):
        tbl = ui.TableView(frame=self.bounds)
        tbl.data_source = ui.ListDataSource(items = range(0, 100))
        tbl.flex = 'wh'
        self.add_subview(tbl)

    
if __name__=='__main__':
    f=(0,0,490,490)
    mc = MyClass(frame = f)
    
    #i=ui.ImageView(frame=(0,0,490,490))
    #i.image=ui.Image.named('test:Mandrill')
    #i.name='Family resemblance'
    #i.alpha=1
    o=Overlay(content=mc)
    o.content_view.border_width=2
    #i.border_width=1
    #i.content_mode=ui.CONTENT_SCALE_ASPECT_FIT
# --------------------
