# @ui
# https://gist.github.com/tjferry14/9ea8bfc0c8d089cdb530
# no .pyui file is needed, the script sets everything up automatically
import ui

def button_tapped(sender):
    v = ui.View()
    v.background_color = 'green'
    v.name = 'Pushed View'
    sender.navigation_view.push_view(v)

root_view = ui.View()
root_view.background_color = 'white'
root_view.name = 'Root View'

button = ui.Button(title='Tap me')
button.action = button_tapped 
root_view.add_subview(button)

nav_view = ui.NavigationView(root_view)
nav_view.present('sheet')