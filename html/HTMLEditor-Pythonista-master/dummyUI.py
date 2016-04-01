print "Dummy UI Script Loaded"

def in_background(func):
    def function(*args, **kwargs):
        return func(*args, **kwargs)
    return function

class View(object):
    def __init__(self, *args, **kwargs):
        print "Initializing view %r" % self
        print "Args: %r" % list(args)
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)

        # ui.View Attributes
        self.alpha = 0.0
        self.background_color = (0.0, 0.0, 0.0, 0.0)
        self.border_color = (0.0, 0.0, 0.0, 0.0)
        self.border_width = 0
        self.bounds = (0, 0, 100, 100)
        self.center = (50, 50)
        self.content_mode = 0  # TODO set this up
        self.corner_radius = 0
        self.flex = ""
        self.frame = (0, 0, 100, 100)
        self.hidden = False
        self.left_button_items = ()
        self.multitouch_enabled = False
        self.name = "%r" % self
        self.navigation_view = None
        self.on_screen = False
        self.subviews = []
        self.superview = None
        self.tint_color = (0.0, 0.0, 0.0, 0.5)
        self.touch_enabled = True
        self.transform = None
        self.x = 0
        self.y = 0

    def width(self):
        return self.frame[3]

    def height(self):
        return self.frame[4]

    def __setattr__(self, key, value):
        if key == "width":
            frame = list(self.frame)
            frame[0] += value
            self.frame = tuple(frame)
        else:
            super(View, self).__setattr__(key, value)

    def add_subview(self, subview):
        self.subviews.append(subview)
        subview.superview = self

    def set_needs_display(self):
        pass

    def present(self, *args, **kwargs):
        print "Presenting view %r" % self
        print "Args: %r" % list(args)
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)


class TableView(View):
    def reload(self):
        pass


class NavigationView(View):
    pass


class ButtonItem(object):
    def __init__(self, *args, **kwargs):
        print "Args: %r" % list(args)
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)


def load_view(ui_view_name=""):
    return View()



class ListDataSource(object):
    def __init__(self, *args, **kwargs):
        print "Args: %r" % list(args)
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)


class Image(object):
    pass

if __name__ == "__main__":
    view = load_view()
    view.present()
    print view.width
    view.width += 100
    print view.width
