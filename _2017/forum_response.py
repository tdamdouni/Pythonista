import ui

# only use this func to create a button for convienience
def quick_button(p, title="", **kwargs):
    # p is the parent view
    _inset = 60
    btn = ui.Button(name='btn', **kwargs)
    btn.frame = ui.Rect(0, 0, p.width, p.width).inset(_inset, _inset)
    btn.corner_radius = btn.width / 2
    btn.center = p.bounds.center()
    btn.title = title
    btn.bg_color = 'cornflowerblue'
    btn.tint_color = 'white'
    btn.font = ('Arial Rounded MT Bold', 48)
    p.add_subview(btn)
    return btn

# Create a Custom ui.View, Inherit from ui.View
class MyClass(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if on the beta version update_interval sets the freq that the update
        # method is called.
        self.update_interval = 1  # update method will be called every second
        self.tf = None
        self.counter = 0
        self.make_view()

    def make_view(self):
        btn = quick_button(self, title='OK', action=self.my_btn_action)
        tf = ui.TextField(width=self.width)
        self.add_subview(tf)
        self.tf = tf

    # The update method, called by ui based on self.update_interval,
    # if 0 is not called
    def update(self):
        print("### test", self.counter, "###")
        self.tf.text = "### test {} ###".format(self.counter)
        self.counter += 1

    def my_btn_action(self, sender):
        print('do something here')

if __name__ == '__main__':
    f = (0, 0, 300, 400)
    v = MyClass(frame=f)
    v.present(style='sheet')
