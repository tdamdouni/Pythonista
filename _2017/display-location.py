# https://forum.omz-software.com/topic/4154/getlocation-takes-0-positional-arguments-but-1-was-given

import location, ui

def getLocation(sender):
	location.start_updates()
	loc = location.get_location()
	location.stop_updates()
	
	#label1.text += loc
	
def getStreetAddress(loc):
	return location.reverse_geocode(loc)[0]
	label1.text = loc
	
	
main_view = ui.View(name = 'Location')
main_view.bg_color = '#bfff8e'


button1 = ui.Button(title = 'location')
button1.frame = (0,30,75,75)
button1.tint_color = 'black'
button1.action = getLocation


label1 = ui.Label(text = '')
label1.number_of_lines = 0
label1.border_width = 1
label1.frame = (100,0,500,200)



main_view.present()

main_view.add_subview(button1)
main_view.add_subview(label1)

