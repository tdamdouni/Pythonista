# https://forum.omz-software.com/topic/3777/moving-from-one-pyui-file-to-another

import ui

main_view = ui.load_view("main.pyui")
other_view = ui.load_view("other.pyui")

# Action of the button in main_view that should show the second view
def my_button_action(sender):
	other_view.present("sheet")
	
main_view.present()

