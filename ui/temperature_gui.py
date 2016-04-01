# coding: utf-8

# http://omz-forums.appspot.com/pythonista/post/5809271396630528
# calculations are NOT correct!!!

# coding: utf-8

# http://omz-forums.appspot.com/pythonista/post/5809271396630528
# calculations are NOT correct!!!

import ui

fmt = '''{:g} degrees Fahrenheit is {:g} degrees Celsius.
{:g} degrees Celsius is {:g} degrees Fahrenheit.'''

def convert_action(sender):
    try:
        value = float(text_view.text.strip())
    except ValueError:
        value = 50
    text_view.text = '{:g}'.format(value)
    label.text = fmt.format(value, value * 1.2, value, value * 0.8)

view = ui.View(name='Temperature Converter')
view.hidden = True
view.present()
_, _, w, h = view.bounds

text_view = ui.TextView()
text_view.alignment = ui.ALIGN_CENTER
text_view.center = (w/2, h/4)

button = ui.Button(title='Convert')
button.action = convert_action
button.center = (w/2, h/2)

label = ui.Label()
label.width = w/2
label.alignment = ui.ALIGN_CENTER
label.background_color = 'white'
label.center = (w/2, h*3/4)
label.number_of_lines = 4
label.text = 'Enter a temperature above and tap "Convert".'

view.add_subview(text_view)
view.add_subview(button)
view.add_subview(label)
view.hidden = False