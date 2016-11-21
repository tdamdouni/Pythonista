# coding: utf-8

# https://forum.omz-software.com/topic/1764/getting-a-list-of-all-ui-gui-classes-programmatically

# Since all UI elements inherit from ui.View, you could list all subclasses of that class:

import ui

ui_elements = []
for cls in vars(ui).values():
	if isinstance(cls, type) and issubclass(cls, ui.View):
		ui_elements.append(cls)
		
# Or as a list comprehension:
ui_elements = [cls for cls in vars(ui).values() if isinstance(cls, type) and issubclass(cls, ui.View)]

