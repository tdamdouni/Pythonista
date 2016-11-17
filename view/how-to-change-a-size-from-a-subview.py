# https://forum.omz-software.com/topic/3529/how-to-change-a-size-from-a-subview

import ui

view = ui.View()  # this is correct however you might want to consider setting a frame size. `view = ui.View(frame=(0,0,width,height))` as the default is less than 200/200 from memory
view.present('portrait')  # from documentation `ui.View.present(style='default', animated=True, popover_location=None, hide_title_bar=False, title_bar_color=None, title_color=None, orientations=None)` therefore if you want to force a orientation you need to provide values for `orientations` not `style` http://omz-software.com/pythonista/docs/ios/ui.html#ui.View.present

def button():  # `ui.Button` actions require a sender argument, ie `def button(sender):...` where `sender` can be named anything
	ui.Imageview('Image').height = 120  # this creates a new `ui.ImageView` and doesn't actually reference any view from you `view` variable in the global stack. This is why you `ui.ImageView` height is not changing. Consider reading the documentation and examples to see how this is done
	
img = ui.ImageView()  # this is correct however you might want to set a new frame size here as the default is 0/0. Which cause also be an attributing reason to why you aren't seeing anything. `ui.ImageView(frame=(0,0,200,200)` or you can set it later with `img.width`, `img.height`, `img.x` and `img.y`
img.name = 'Veer'
img.heigt = 150  # I'm going to assume that this is just a typo
view.add_subview(img)

button = ui.Button()  # by naming the variable of this object to `button` you have overrided the method by the same name, thus you will get a `Exception` when tapping the button. Consider renaming either the method name to something else or renaming this variable to something else.
button.action = button
view.add_subview(button)

