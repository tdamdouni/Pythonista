# https://forum.omz-software.com/topic/3423/share-code-ui-view-without-x-button

import ui

view = ui.View()
navigationView = ui.NavigationView(view)

# Add a close button
view.left_button_items = [ui.ButtonItem(title="Close", action=lambda x: navigationView.close())]

# Won't show the x-button
navigationView.present("sheet", hide_title_bar=True)

