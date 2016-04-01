# https://omz-forums.appspot.com/pythonista/post/5905674621943808
# coding: utf-8
import ui

ui_elements = []
for cls in vars(ui).values():
    if isinstance(cls, type) and issubclass(cls, ui.View):
        ui_elements.append(cls)

# Or as a list comprehension:
ui_elements = [cls for cls in vars(ui).values() if isinstance(cls, type) and issubclass(cls, ui.View)]