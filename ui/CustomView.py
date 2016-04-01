# coding: utf-8

# https://forum.omz-software.com/topic/2472/custom-ui-class-a-ui-view-or-loaded-from-a-pyui-file-share-but-i-am-not-happy

# Custom ui.class a ui.view or loaded from a pyui file [share] but I am not happy

# This works, sort of...one class that can either be a loaded pyui file or a class inherited from ui.View. It works. But not one step... I got so close but ran out of ideas. I can see the problem, it's in the comments of the code. Maybe there is such a simple solution... But seems hopeless to me :(
# Well it is one step. But, you have to create your ui.View inside the new method. So really it does work. But limiting in my mind...
# I think it's still good, but it's killing me, I can't get that last step

#

class PanelMorphic(ui.View):
    def __init__(self, **kwargs):
        # if we are here, creating a ui.View in code
        # BUT... with the new, i cant get in here.
        # tried so many differnt ways ;(
        print 'IN __INIT__()'

    def __new__(self, *args,  **kwargs):
        # check kwargs to see if we were passed a pyui_file
        if not kwargs.get('pyui_file', False):
            cls =  ui.View(*args, **kwargs)
            
            '''
                this sort of COOL. But i cant work out how to call the
                __init__ or another methid in the class until we return 
                from here.
                i can build up the ui.View in here, but not ideal.
                typically a lot of code to build a ui.View. 
                would be great if we could call a method in here.
                
                Also, could call a method to build the ui.View after
                the object is created. Which us probably what i will do
                if i can solve it. But its so close....
                its killing me inside
                
                but i have trued so many ways. The basic crux of the matter 
                as far as i can see, until this method returns, there
                is no PanelMorphic object. if you try to create one, oh 
                opps, you are in the new again. 
                what come first the chicken or the egg...
            '''
            
            # cant work out a way to do this....
            # would love if someone could show me
            
            # the line below fails... 
            # self._make_view_in_code_(*args, **kwargs)
            return cls

        else:
            cls = ui.load_view(kwargs.get('pyui_file', False))
            cls['tb_countries'].data_source.items = _country_list
            cls['seg'].segments = string.ascii_uppercase
            return cls
            
    def _make_view_in_code_(self, *args, **kwargs):
        print 'IN _make_view_in_code_()'

v = PanelMorphic(frame = (0,0, 500, 500), background_color = 'navy'))
v = PanelMorphic(pyui_file = 'Countries')