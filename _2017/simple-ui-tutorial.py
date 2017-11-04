# https://forum.omz-software.com/topic/3988/simple-ui-tutorial/23

import ui
import clipboard
import console


class MyConsole(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tv = None
        self.make_view()

    def make_view(self):
        tv = ui.TextView(frame=self.bounds,
                         flex='wh',
                         font=('Menlo', 24),
                         editable=False,
                         )
        self.tv = tv
        self.add_subview(self.tv)

        '''
        Create 2 ui.ButtonItem to insert into the menubar.  ButtonItem's are
        one of those pesky ui Items that are not subclassed from ui.View
        Its not a big deal, just good to know they differ from ui.Button.
        You can see in the docs.

        Below, I am adding the 2 menu buttons to the right side as it seems to
        make sense. There is a method left_button_items also.
        '''
        mbtn_clear = ui.ButtonItem(title='Clear', action=self.clear_console, tint_color='red')
        mbtn_copy = ui.ButtonItem(title='Copy', action=self.copy_console)
        self.right_button_items = (mbtn_clear, mbtn_copy)

    def write_line(self, txt):
        self.tv.text += "{}\n".format(txt)

    def clear_console(self, sender=None):
        '''
        sender is set to None so sender is not required to call this method.
        The action from the menu ButtonItem needs to see it there though.
        But it means you can call this method on the object withouut having
        to pass a sender.  i.e if youwanted to clear the console from your
        code rather than the menu button action.
        ie. obj.clear_console() will work.
        Same goes for the copy_console method below.
        '''
        self.tv.text = ""

    def copy_console(self, sender=None):
        clipboard.set(self.tv.text)
        console.hud_alert('{} characters copied.'.format(len(self.tv.text)))


if __name__ == '__main__':
    f = (0, 0, ui.get_screen_size()[0], ui.get_screen_size()[1])
    v = MyConsole(frame=f, name='My Full Sceen Console')
    v.present(style='', animated=False)
    for i in range(100):
        v.write_line('line-{}'.format(i))
