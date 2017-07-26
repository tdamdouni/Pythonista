# https://forum.omz-software.com/topic/3758/disable-stop-button-x-in-scene

# Hide X button
import ui
view = ui.View(bg_color = 'slateblue')
view.present('sheet', hide_title_bar=True)
