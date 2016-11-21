# coding: utf-8

# https://gist.github.com/steventroughtonsmith/ad7eda38c797dfddc394

from objc_util import *

UIApplication = ObjCClass('UIApplication')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	tabVC.tabCollectionView().collectionViewLayout().itemSize = CGSize(328,200)
	tabVC.tabCollectionView().contentInset = UIEdgeInsets(58,0,0,0)
	
	overviewItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('ShowTabs'), 0, tabVC, sel('showTabOverview:'))
	tabVC.persistentLeftBarButtonItems = [overviewItem]
	tabVC.reloadBarButtonItemsForSelectedTab()
	
if __name__ == '__main__':
	main()

