# https://forum.omz-software.com/topic/4154/getlocation-takes-0-positional-arguments-but-1-was-given/2

import location
import ui


def getLocation(sender):
	location.start_updates()
	label1.text = str(location.get_location())
	location.stop_updates()
	
	
label1 = ui.Label(border_width=1, frame=(100, 0, 500, 200), number_of_lines=0)
main_view = ui.View(name='Location', bg_color='#bfff8e')
main_view.add_subview(label1)
main_view.add_subview(ui.Button(title='location', frame=(0, 30, 75, 75),
                                tint_color='black', action=getLocation))
main_view.present()

