# https://forum.omz-software.com/topic/4123/possible-to-change-menubar-header-color-and-font-for-ui-view

import ui

main_view = ui.View(
	frame=(0, 0, 400, 400), bg_color='yellow', name='Test'
)

main_view.present('sheet', title_bar_color='yellow')

