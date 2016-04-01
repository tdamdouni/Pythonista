# http://omz-forums.appspot.com/pythonista/post/5867913269477376
# Theming class for ui. only a start and idea
# coding: utf-8
import ui

__THEME_DARK__ = {
                  'my_view_bg_color':'orange',
                  'background_color':(1,0,0,.5),
                  'border_width':1,
                  'tint_color':'white',
                  'corner_radius':3,
                  'width':80,
                  'center':(0,0), # replace with function in the init of theme class. just to know you can

                  }

class theme (object):
    def __init__(self, view):
        self.view = view
        self.theme_dict = __THEME_DARK__
        # i am sure there is an elgant way to early bind the function in the dict. guessing the order of declaration, would allow me to specify in the dict.
        self.theme_dict['center'] = self._center()
        self.theme_view(self.view)

    def theme_view(self, view):
        #handle the view, differently from the subviews.. i would think this would be the normal requirement.
        view.bg_color = self.theme_dict['my_view_bg_color']
        for obj in view.subviews:
            self._theme_obj(obj)

    def _theme_obj(self, obj):
        for attr in dir(obj):
            if attr in self.theme_dict:
                setattr(obj,attr,self.theme_dict[attr])

    def _center(self):
        return (300,300)

if __name__ == '__main__':
    #print dir(ui.Button)
    v = ui.View()
    v.name = 'Demo'
    button = ui.Button(title='Help me!')
    v.add_subview(button)
    t = theme(v)
    v.present('sheet')