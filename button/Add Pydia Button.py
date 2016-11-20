# coding: utf-8

# https://gist.github.com/bmw1821/d9883042b95a818e6429

def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	
	methods = [pydiaButtonPressed]
	PydiaItemController = create_objc_class('PydiaItemController', NSObject, methods = methods)
	
	pydiaItemController = PydiaItemController.new()
	
	try:
		PydiaBarButtonItem = ObjCClass('PydiaBarButtonItem')
	except ValueError:
		PydiaBarButtonItem = create_objc_class('PydiaBarButtonItem', UIBarButtonItem)
		
	pydiaItem = PydiaBarButtonItem.alloc().initWithImage_style_target_action_(ns(ui.Image.named('iob:ios7_cart_outline_32')), 0, pydiaItemController, sel('pydiaButtonPressed'))
	
	leftBarButtonItems = list(tabVC.persistentLeftBarButtonItems())
	leftBarButtonItems.append(pydiaItem)
	tabVC.persistentLeftBarButtonItems = ns(leftBarButtonItems)
	tabVC.reloadBarButtonItemsForSelectedTab()
	
def pydiaButtonPressed(_self, _cmd):
	from PydiaKit import launch
	launch()
	
if __name__ == '__main__':
	main()

