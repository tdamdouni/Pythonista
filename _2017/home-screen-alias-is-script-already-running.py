# https://forum.omz-software.com/topic/4097/home-screen-alias-is-script-already-running/6

import builtins, ui

try:
	bookView = builtins.navigation
except:
	bookView = None
	
if bookView and isinstance(bookView, ui.View) and bookView.on_screen:
	print('Reusing existing book view')
	navigation = bookView
	inventoryView = builtins.inventory
	reviewView = builtins.reviews
else:
	reviewView = ui.load_view('views/reviews')
	inventoryView = ui.load_view('views/inventory')
	reviewView.flex = 'WH'
	inventoryView.flex = 'WH'
	
	if isPhone:
		inventoryView.remove_subview(inventoryView['kinds'])
		titleView = inventoryView['titles']
		titleView.width = inventoryView.width-12
		
	navigation = StuffView(frame=inventoryView.frame, name='Books & Stuff')
	navigation.add_subview(reviewView)
	navigation.add_subview(inventoryView)
	navigation.present()
	builtins.navigation = navigation
	builtins.inventory = inventoryView
	builtins.reviews = reviewView

