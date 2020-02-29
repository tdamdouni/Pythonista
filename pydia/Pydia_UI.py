# coding: utf-8

# https://gist.github.com/bmw1821/bc2ccf257d60804be010

from __future__ import print_function
from objc_util import *
from UIKit import *
from Foundation import *
import PydiaKit
import console
import os

sourcesTableViewController = None
sourcesNavigationController = None
sourcePackagesTableViewController = None
updatesTableViewController = None
updatesNavigationController = None
installedTableViewController = None
installedNavigationController = None
searchTableViewController = None
searchNavigationController = None
searchBar = None
mainTabBarController = None
packageDetailsTableViewController = None

packageDetailsInstallBarButtonItem = None
packageDetailsModifyBarButtonItem = None

selectedSource = None

@on_main_thread
def main():
	global rootVC, tabVC, sourcesTableViewController, sourcesNavigationController, sourcePackagesTableViewController, updatesTableViewController, updatesNavigationController, installedTableViewController, installedNavigationController, searchTableViewController, searchNavigationController, searchBar, mainTabBarController, packageDetailsTableViewController
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	
	SourcesTableViewController = create_objc_class('SourcesTableViewController', UITableViewController, methods = [viewWillAppear_, numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_, tableView_commitEditingStyle_forRowAtIndexPath_, reloadSources, addSource], protocols = [])
	sourcesTableViewController = SourcesTableViewController.new()
	sourcesTableViewController.title = 'Sources'
	sourcesTableViewController.tableView().tag = 1
	
	addSourceBarButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(4, sourcesTableViewController, sel('addSource'))
	reloadSourcesBarButtonItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Textures/ionicons-ios7-refresh-empty-32.png'), 0, sourcesTableViewController, sel('reloadSources'))
	sourcesTableViewController.navigationItem().rightBarButtonItems = [reloadSourcesBarButtonItem, addSourceBarButtonItem]
	
	SourcePackagesTableViewController = create_objc_class('SourcePackagesTableViewController', UITableViewController, methods = [viewWillAppear_, viewDidLoad, numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_], protocols = [])
	sourcePackagesTableViewController = SourcePackagesTableViewController.new()
	sourcePackagesTableViewController.tableView().tag = 5
	
	sourcesNavigationController = UINavigationController.alloc().initWithRootViewController_(sourcesTableViewController)
	sourcesNavigationController.tabBarItem = UITabBarItem.alloc().initWithTitle_image_selectedImage_('Sources', UIImage.imageNamed_('Textures/ionicons-ios7-albums-outline-32.png'), UIImage.imageNamed_('Textures/ionicons-ios7-albums-32.png'))
	
	
	UpdatesTableViewController = create_objc_class('UpdatesTableViewController', UITableViewController, methods = [viewWillAppear_, numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_, ], protocols = [])
	updatesTableViewController = UpdatesTableViewController.new()
	updatesTableViewController.title = 'Updates'
	updatesTableViewController.tableView().tag = 2
	
	updatesNavigationController = UINavigationController.alloc().initWithRootViewController_(updatesTableViewController)
	updatesNavigationController.tabBarItem = UITabBarItem.alloc().initWithTitle_image_selectedImage_('Updates', UIImage.imageNamed_('Textures/ionicons-ios7-clock-outline-32.png'), UIImage.imageNamed_('Textures/ionicons-ios7-clock-32.png'))
	reloadUpdatesBadgeValue()
	
	
	InstalledTableViewController = create_objc_class('InstalledTableViewController', UITableViewController, methods = [viewWillAppear_, numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_, ], protocols = [])
	installedTableViewController = InstalledTableViewController.new()
	installedTableViewController.title = 'Installed'
	installedTableViewController.tableView().tag = 3
	
	installedNavigationController = UINavigationController.alloc().initWithRootViewController_(installedTableViewController)
	installedNavigationController.tabBarItem = UITabBarItem.alloc().initWithTitle_image_selectedImage_('Installed', UIImage.imageNamed_('Textures/ionicons-ios7-download-outline-32.png'), UIImage.imageNamed_('Textures/ionicons-ios7-download-32.png'))
	
	
	SearchTableViewController = create_objc_class('SearchTableViewController', UITableViewController, methods = [viewWillAppear_, numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_, searchBar_textDidChange_, searchBarSearchButtonClicked_, searchBarCancelButtonClicked_], protocols = ['UISearchBarDelegate'])
	searchTableViewController = SearchTableViewController.new()
	searchTableViewController.title = 'Search'
	searchTableViewController.tableView().tag = 4
	
	searchNavigationController = UINavigationController.alloc().initWithRootViewController_(searchTableViewController)
	searchNavigationController.tabBarItem = UITabBarItem.alloc().initWithTitle_image_selectedImage_('Search', UIImage.imageNamed_('Textures/ionicons-ios7-search-32.png'), UIImage.imageNamed_('Textures/ionicons-ios7-search-strong-32.png'))
	
	searchBar = UISearchBar.alloc().init()
	searchBar.delegate = searchTableViewController
	searchBar.searchBarStyle = 2
	searchBar.placeholder = 'Search for a Package'
	searchBar.showsCancelButton = True
	searchTableViewController.navigationItem().titleView = searchBar
	
	MainTabBarController = create_objc_class('MainTabBarController', UITabBarController, methods = [closePydia])
	mainTabBarController = MainTabBarController.alloc().init()
	mainTabBarController.viewControllers = [sourcesNavigationController, updatesNavigationController, installedNavigationController, searchNavigationController]
	mainTabBarController.title = 'Pydia'
	
	#closePydiaBarButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(14, mainTabBarController, sel('closePydia'))
	
	closePydiaBarButtonItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Textures/ionicons-ios7-close-outline-32.png'), 0, mainTabBarController, sel('closePydia'))
	
	sourcesTableViewController.navigationItem().leftBarButtonItems = [closePydiaBarButtonItem, sourcesTableViewController.editButtonItem()]
	updatesTableViewController.navigationItem().leftBarButtonItem = closePydiaBarButtonItem
	installedTableViewController.navigationItem().leftBarButtonItem = closePydiaBarButtonItem
	searchTableViewController.navigationItem().leftBarButtonItem = closePydiaBarButtonItem
	
	PackageDetailsTableViewController = create_objc_class('PackageDetailsTableViewController', UITableViewController, methods = [viewWillAppear_, numberOfSectionsInTableView_, tableView_numberOfRowsInSection_, tableView_heightForRowAtIndexPath_, tableView_cellForRowAtIndexPath_, tableView_didSelectRowAtIndexPath_, modifyPackage, installPackage, removePackage], protocols = [])
	packageDetailsTableViewController = PackageDetailsTableViewController.alloc().initWithStyle_(1)
	packageDetailsTableViewController.tableView().tag = 6
	packageDetailsTableViewController.title = 'Details'
	
	def pydiaLoadedCompletionHandler(_self, _cmd):
		reloadSources()
	pydiaLoadedCompletionHandlerBlock = ObjCBlock(pydiaLoadedCompletionHandler, None, [c_void_p, c_void_p])
	retain_global(pydiaLoadedCompletionHandlerBlock)
	rootVC.presentViewController_animated_completion_(mainTabBarController, True, pydiaLoadedCompletionHandlerBlock)
	
def closePydia(_self, _cmd):
	rootVC.dismissViewControllerAnimated_completion_(True, None)
	
def reloadSources(_self = None, _cmd = None):
	reloadingSourcesAlert = loadingAlertControllerWithTitle('Reloading Sources...')
	
	def loadingAlertPresentedCompletionHandler(_self, _cmd):
	
		PydiaKit.Sources.download_source_files()
		sourcesTableViewController.dismissViewControllerAnimated_completion_(True, None)
		sourcesTableViewController.tableView().reloadData()
		reloadUpdatesBadgeValue()
		
	loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
	retain_global(loadingAlertPresentedCompletionHandlerBlock)
	sourcesTableViewController.presentViewController_animated_completion_(reloadingSourcesAlert, True, loadingAlertPresentedCompletionHandlerBlock)
	
def addSource(_self, _cmd):
	source_url = console.input_alert('Add Source', 'Enter the URL of a Pydia source', '', 'Add')
	source = PydiaKit.Sources.add_source(source_url)
	if source:
		console.alert('Source Added', 'Added the source \'%s\'' % source.name, 'Close', hide_cancel_button = True)
		reloadSources()
	else:
		console.alert('Error', 'The source could not be added. Please ensure you entered the URL correctly, you are connected to the Internet, and have not already added the source.', 'Close', hide_cancel_button = True)
		
#MARK: TableViewControllerMethods Methods

def loadingAlertControllerWithTitle(title):
	loadingAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_(title, '\n', 1)
	activityIndicatorFrame = loadingAlert.view().bounds()
	activityIndicatorFrame.origin.y += 17.5
	activityIndicator = UIActivityIndicatorView.alloc().initWithFrame_(activityIndicatorFrame)
	activityIndicator.autoresizingMask = 18
	activityIndicator.activityIndicatorViewStyle = 2
	activityIndicator.startAnimating()
	loadingAlert.view().addSubview_(activityIndicator)
	return loadingAlert
	
def informationAlertController(title, message):
	informationAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_(title, message, 1)
	informationAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Close', 1, None))
	return informationAlert
	
def viewDidLoad(_self, _cmd):
	self = ObjCInstance(_self)
	
def viewWillAppear_(_self, _cmd, _animated):
	self = ObjCInstance(_self)
	if self in [sourcesTableViewController, updatesTableViewController, installedTableViewController, searchTableViewController]:
		self.tableView().reloadData()
	elif self is sourcePackagesTableViewController:
		self.tableView().reloadData()
		self.title = selectedSource.name
	elif self is packageDetailsTableViewController:
		packageDetailsTableViewController.tableView().reloadData()
		reloadPackageDetailsModifyBarButtonItem()
		
def reloadUpdatesBadgeValue():
	updates = PydiaKit.Package.get_package_updates()
	updatesNavigationController.tabBarItem().badgeValue = str(len(updates)) if len(updates) else None
	
def reloadPackageDetailsModifyBarButtonItem():
	package = packageDetailsTableViewController.package
	barButtonItem = None
	if PydiaKit.Package.get_installed_package_for_identifier(package.identifier):
		if PydiaKit.Package.get_package_for_identifier(package.identifier):
			barButtonItem = UIBarButtonItem.alloc().initWithTitle_style_target_action_('Modify', 0, packageDetailsTableViewController, sel('modifyPackage'))
		else:
			barButtonItem = UIBarButtonItem.alloc().initWithTitle_style_target_action_('Remove', 0, packageDetailsTableViewController, sel('removePackage'))
	else:
		barButtonItem = UIBarButtonItem.alloc().initWithTitle_style_target_action_('Install', 0, packageDetailsTableViewController, sel('installPackage'))
	packageDetailsTableViewController.navigationItem().rightBarButtonItem = barButtonItem
	
def modifyPackage(_self, _cmd):
	modifyPackageAlertController = UIAlertController.alertControllerWithTitle_message_preferredStyle_(None, None, 0)
	if PydiaKit.Package.update_available_for_package(packageDetailsTableViewController.package):
		def alertActionUpdate(action):
			def alertActionConfirmUpdate(action):
				def loadingAlertPresentedCompletionHandler(_self, _cmd):
					try:
						global update
						update = PydiaKit.Package.update_package(packageDetailsTableViewController.package.identifier)
						def loadingAlertDismissedCompletionHandler(_self, _cmd):
							global update
							if update:
								packageDetailsTableViewController.tableView().reloadData()
								reloadUpdatesBadgeValue()
								message = '\'%s\' was successfuly updated to version %s.' % (update.name, str(update.version))
								packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Updated', message), True)
							else:
								message = '\'%s\' could not be updated.' % packageDetailsTableViewController.package.name
								packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
								
						loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
						retain_global(loadingAlertDismissedCompletionHandlerBlock)
						packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
					except PydiaKit.Package.PackageInstallOverwriteException as e:
						def loadingAlertDismissedCompletionHandler(_self, _cmd):
							file_list = '\n\n'.join(e.files)
							overwriteAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Overwrite Files?', 'The following files will be overwritten if you continue:\n\n' + file_list, 1)
							def alertActionContinueUpdate(action):
								def loadingAlertPresentedCompletionHandler(_self, _cmd):
									global update
									update = PydiaKit.Package.update_package(packageDetailsTableViewController.package.identifier, True)
									def loadingAlertDismissedCompletionHandler(_self, _cmd):
										global update
										if update:
											packageDetailsTableViewController.tableView().reloadData()
											reloadUpdatesBadgeValue()
											message = '\'%s\' was successfuly updated to version %s.' % (update.name, str(update.version))
											packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Updated', message), True)
										else:
											message = '\'%s\' could not be updated.' % packageDetailsTableViewController.package.name
											packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
											
									loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
									retain_global(loadingAlertDismissedCompletionHandlerBlock)
									packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
									
								loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
								retain_global(loadingAlertPresentedCompletionHandlerBlock)
								packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Updating Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
							alertActionContinueUpdateBlock = ObjCBlock(alertActionContinueUpdate, None, [c_void_p])
							retain_global(alertActionContinueUpdateBlock)
							overwriteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
							overwriteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Continue', 2, alertActionContinueUpdateBlock))
							packageDetailsTableViewController.presentModalViewController_animated_(overwriteAlert, True)
						loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
						retain_global(loadingAlertDismissedCompletionHandlerBlock)
						packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
				loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
				retain_global(loadingAlertPresentedCompletionHandlerBlock)
				packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Updating Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
			confirmUpdatePackageAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Update Package', 'Update \'%s\'?' % packageDetailsTableViewController.package.name, 1)
			alertActionConfirmUpdateBlock = ObjCBlock(alertActionConfirmUpdate, None, [c_void_p])
			retain_global(alertActionConfirmUpdateBlock)
			confirmUpdatePackageAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
			confirmUpdatePackageAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Update', 0, alertActionConfirmUpdateBlock))
			packageDetailsTableViewController.presentModalViewController_animated_(confirmUpdatePackageAlert, True)
		alertActionUpdateBlock = ObjCBlock(alertActionUpdate, None, [c_void_p])
		retain_global(alertActionUpdateBlock)
		modifyPackageAlertController.addAction_(UIAlertAction.actionWithTitle_style_handler_('Update', 0, alertActionUpdateBlock))
	else:
		def alertActionReinstall(action):
			def alertActionConfirmReinstall(action):
				def loadingAlertPresentedCompletionHandler(_self, _cmd):
					package = packageDetailsTableViewController.package
					global success
					success = PydiaKit.Package.install_package(package, True)
					def loadingAlertDismissedCompletionHandler(_self, _cmd):
						global success
						if success:
							message = '\'%s\' was successfuly reinstalled.' % packageDetailsTableViewController.package.name
							packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Reinstalled', message), True)
						else:
							message = '\'%s\' could not be reinstalled.' % packageDetailsTableViewController.package.name
							packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
					loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
					retain_global(loadingAlertDismissedCompletionHandlerBlock)
					packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
					
				loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
				retain_global(loadingAlertPresentedCompletionHandlerBlock)
				packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Reinstalling Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
				
			confirmReinstallPackageAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Reinstall Package', 'Reinstall \'%s\'?' % packageDetailsTableViewController.package.name, 1)
			alertActionConfirmReinstallBlock = ObjCBlock(alertActionConfirmReinstall, None, [c_void_p])
			retain_global(alertActionConfirmReinstallBlock)
			confirmReinstallPackageAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
			confirmReinstallPackageAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Reinstall', 0, alertActionConfirmReinstallBlock))
			packageDetailsTableViewController.presentModalViewController_animated_(confirmReinstallPackageAlert, True)
			
		alertActionReinstallBlock = ObjCBlock(alertActionReinstall, None, [c_void_p])
		retain_global(alertActionReinstallBlock)
		modifyPackageAlertController.addAction_(UIAlertAction.actionWithTitle_style_handler_('Reinstall', 0, alertActionReinstallBlock))
		
	def alertActionRemove(action):
		def alertActionConfirmRemove(action):
			def loadingAlertPresentedCompletionHandler(_self, _cmd):
				package = packageDetailsTableViewController.package
				global success
				success = PydiaKit.Package.uninstall_package(package.identifier)
				def loadingAlertDismissedCompletionHandler(_self, _cmd):
					global success
					if success:
						message = '\'%s\' was successfuly removed.' % packageDetailsTableViewController.package.name
						packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Removed', message), True)
						
						packageDetailsTableViewController.tableView().reloadData()
						reloadPackageDetailsModifyBarButtonItem()
						reloadUpdatesBadgeValue()
					else:
						message = '\'%s\' could not be removed.' % packageDetailsTableViewController.package.name
						packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
				loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
				retain_global(loadingAlertDismissedCompletionHandlerBlock)
				packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
			loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
			retain_global(loadingAlertPresentedCompletionHandlerBlock)
			packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Removing Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
		message = 'Are you sure you want to remove \'%s\'?' % packageDetailsTableViewController.package.name
		dependant_packages = PydiaKit.Package.packages_dependant_on(packageDetailsTableViewController.package.identifier)
		if len(dependant_packages) > 0:
			message += '\n\nThe following packages depend on \'%s\' and may not work properly if you remove it:\n\n' % packageDetailsTableViewController.package.name
			message += '\n\n'.join([package.name for package in dependant_packages])
		confirmDeleteAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Remove Package', message, 1)
		
		alertActionConfirmRemoveBlock = ObjCBlock(alertActionConfirmRemove, None, [c_void_p])
		retain_global(alertActionConfirmRemoveBlock)
		confirmDeleteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Remove', 2, alertActionConfirmRemoveBlock))
		confirmDeleteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
		
		packageDetailsTableViewController.presentModalViewController_animated_(confirmDeleteAlert, True)
		
	alertActionRemoveBlock = ObjCBlock(alertActionRemove, None, [c_void_p])
	retain_global(alertActionRemoveBlock)
	modifyPackageAlertController.addAction_(UIAlertAction.actionWithTitle_style_handler_('Remove', 2, alertActionRemoveBlock))
	modifyPackageAlertController.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
	if UIDevice.currentDevice().userInterfaceIdiom() == 1:
		modifyPackageAlertController.modalPresentationStyle = 7
		barButtonItemView = packageDetailsTableViewController.navigationItem().rightBarButtonItem().valueForKey_('view')
		modifyPackageAlertController.popoverPresentationController().sourceView = barButtonItemView
		modifyPackageAlertController.popoverPresentationController().sourceRect = ((barButtonItemView.frame().size.height, barButtonItemView.frame().size.width / 2), (1, 1))
	packageDetailsTableViewController.presentModalViewController_animated_(modifyPackageAlertController, True)
	
def installPackage(_self, _cmd):
	def alertActionConfirmInstall(action):
		def loadingAlertPresentedCompletionHandler(_self, _cmd):
			try:
			
				global success
				success = PydiaKit.Package.install_package(packageDetailsTableViewController.package)
				def loadingAlertDismissedCompletionHandler(_self, _cmd):
					global success
					if success:
					
						message = '\'%s\' was successfuly installed.' % packageDetailsTableViewController.package.name
						packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Installed', message), True)
						
						reloadPackageDetailsModifyBarButtonItem()
						
					else:
						message = '\'%s\' could not be installed.' % packageDetailsTableViewController.package.name
						packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
						
				loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
				retain_global(loadingAlertDismissedCompletionHandlerBlock)
				packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
			except PydiaKit.Package.PackageInstallOverwriteException as e:
				def loadingAlertDismissedCompletionHandler(_self, _cmd):
					file_list = '\n\n'.join(e.files)
					overwriteAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Overwrite Files?', 'The following files will be overwritten if you continue:\n\n' + file_list, 1)
					def alertActionContinueInstall(action):
						def loadingAlertPresentedCompletionHandler(_self, _cmd):
							global success
							success = PydiaKit.Package.install_package(packageDetailsTableViewController.package, True)
							def loadingAlertDismissedCompletionHandler(_self, _cmd):
								global success
								if success:
									packageDetailsTableViewController.tableView().reloadData()
									
									message = '\'%s\' was successfuly installed.' % packageDetailsTableViewController.package.name
									packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Installed', message), True)
									
									reloadPackageDetailsModifyBarButtonItem()
									
								else:
									message = '\'%s\' could not be installed.' % packageDetailsTableViewController.package.name
									packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
									
							loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
							retain_global(loadingAlertDismissedCompletionHandlerBlock)
							packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
						loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
						retain_global(loadingAlertPresentedCompletionHandlerBlock)
						packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Installing Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
					alertActionContinueInstallBlock = ObjCBlock(alertActionContinueInstall, None, [c_void_p])
					retain_global(alertActionContinueInstallBlock)
					overwriteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
					overwriteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Continue', 2, alertActionContinueInstallBlock))
					packageDetailsTableViewController.presentModalViewController_animated_(overwriteAlert, True)
				loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
				retain_global(loadingAlertDismissedCompletionHandlerBlock)
				packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
			except PydiaKit.Package.PackageInstallMissingDependencyException as e:
				def loadingAlertDismissedCompletionHandler(_self, _cmd):
					dependencies_list = '\n\n'.join(e.identifiers)
					packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', 'The following packages reqiured for installation of %s could not be located:\n\n%s\n\nYou may need to add an additional source.' % (packageDetailsTableViewController.package.name, dependencies_list)), True)
				loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
				retain_global(loadingAlertDismissedCompletionHandlerBlock)
				packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
		loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
		retain_global(loadingAlertPresentedCompletionHandlerBlock)
		packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Installing Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
		
	confirmInstallPackageAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Install Package', 'Install \'%s\'?' % packageDetailsTableViewController.package.name, 1)
	alertActionConfirmInstallBlock = ObjCBlock(alertActionConfirmInstall, None, [c_void_p])
	retain_global(alertActionConfirmInstallBlock)
	confirmInstallPackageAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
	confirmInstallPackageAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Install', 0, alertActionConfirmInstallBlock))
	packageDetailsTableViewController.presentModalViewController_animated_(confirmInstallPackageAlert, True)
	
def removePackage(_self, _cmd):
	def alertActionConfirmRemove(action):
		def loadingAlertPresentedCompletionHandler(_self, _cmd):
			package = packageDetailsTableViewController.package
			global success
			success = PydiaKit.Package.uninstall_package(package.identifier)
			def loadingAlertDismissedCompletionHandler(_self, _cmd):
				global success
				if success:
					message = '\'%s\' was successfuly removed.' % packageDetailsTableViewController.package.name
					packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Package Removed', message), True)
					
					packageDetailsTableViewController.tableView().reloadData()
					reloadPackageDetailsModifyBarButtonItem()
					reloadUpdatesBadgeValue()
				else:
					message = '\'%s\' could not be removed.' % packageDetailsTableViewController.package.name
					packageDetailsTableViewController.presentModalViewController_animated_(informationAlertController('Error', message), True)
			loadingAlertDismissedCompletionHandlerBlock = ObjCBlock(loadingAlertDismissedCompletionHandler, None, [c_void_p, c_void_p])
			retain_global(loadingAlertDismissedCompletionHandlerBlock)
			packageDetailsTableViewController.dismissViewControllerAnimated_completion_(True, loadingAlertDismissedCompletionHandlerBlock)
		loadingAlertPresentedCompletionHandlerBlock = ObjCBlock(loadingAlertPresentedCompletionHandler, None, [c_void_p, c_void_p])
		retain_global(loadingAlertPresentedCompletionHandlerBlock)
		packageDetailsTableViewController.presentViewController_animated_completion_(loadingAlertControllerWithTitle('Removing Package...'), True, loadingAlertPresentedCompletionHandlerBlock)
	message = 'Are you sure you want to remove \'%s\'?' % packageDetailsTableViewController.package.name
	dependant_packages = PydiaKit.Package.packages_dependant_on(packageDetailsTableViewController.package.identifier)
	if len(dependant_packages) > 0:
		message += '\n\nThe following packages depend on \'%s\' and may not work properly if you remove it:\n\n' % packageDetailsTableViewController.package.name
		message += '\n\n'.join([package.name for package in dependant_packages])
	confirmDeleteAlert = UIAlertController.alertControllerWithTitle_message_preferredStyle_('Remove Package', message, 1)
	
	alertActionConfirmRemoveBlock = ObjCBlock(alertActionConfirmRemove, None, [c_void_p])
	retain_global(alertActionConfirmRemoveBlock)
	confirmDeleteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Remove', 2, alertActionConfirmRemoveBlock))
	confirmDeleteAlert.addAction_(UIAlertAction.actionWithTitle_style_handler_('Cancel', 1, None))
	
	packageDetailsTableViewController.presentModalViewController_animated_(confirmDeleteAlert, True)
	
def numberOfSectionsInTableView_(_self, _cmd, _tableView):
	if ObjCInstance(_tableView).tag() == 6:
		return 3
	return 1
	
def tableView_numberOfRowsInSection_(_self, _cmd, _tableView, _section):
	tableView = ObjCInstance(_tableView)
	if tableView.tag() == 1:
		return len(PydiaKit.Sources.get_sources()) + len(PydiaKit.Sources.get_unloaded_source_URLs())
	elif tableView.tag() == 2:
		update_count = len(PydiaKit.Package.get_package_updates())
		if update_count > 0:
			return update_count
		else:
			return 1
	elif tableView.tag() == 3:
		return len(PydiaKit.Package.get_installed_packages())
	elif tableView.tag() == 4:
		return len(PydiaKit.Package.get_packages_for_search_text(str(searchBar.text())))
	elif tableView.tag() == 5:
		if selectedSource:
			return len(selectedSource.packages)
	elif tableView.tag() == 6:
		update = PydiaKit.Package.update_available_for_package(packageDetailsTableViewController.package)
		return [1, 4 if update else 3, 1][_section]
	return 0
	
def tableView_titleForHeaderInSection_(_self, _cmd, _tableView, _section):
	print(_section)
	return NSString.alloc().initWithString_('a')
	#return ['', 'Info', 'Description'][_section]
	
def tableView_heightForRowAtIndexPath_(_self, _cmd, _tableView, _indexPath):

	tableView = ObjCInstance(_tableView)
	indexPath = ObjCInstance(_indexPath)
	
	if tableView.tag() == 6:
	
		if indexPath.section() == 2:
		
			package = packageDetailsTableViewController.package
			
			labelWidth = tableView.frame().size.width - (tableView.separatorInset().left * 2)
			
			cellHeight = ns(package.description).sizeWithFont_constrainedToSize_lineBreakMode_(UIFont.fontWithName_size_('.SFUIText-Regular', 17), (labelWidth, 3.40282347E+38), 0).height + 20
			
			return cellHeight if cellHeight > 44 else -1
			
	return -1
	
def tableView_cellForRowAtIndexPath_(_self, _cmd, _tableView, _indexPath):

	tableView = ObjCInstance(_tableView)
	indexPath = ObjCInstance(_indexPath)
	
	reuseIdentifier = 'Cell'
	
	cellStyle = 3
	if tableView.tag() == 2:
		updates = PydiaKit.Package.get_package_updates()
		if len(updates) == 0:
			cellStyle = 0
	if tableView.tag() == 6:
		if indexPath.section() in [0, 2]:
			cellStyle = 0
		elif indexPath.section() == 1:
			cellStyle = 1
			
	cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(cellStyle, reuseIdentifier)
	if tableView.tag() == 1:
		sources = PydiaKit.Sources.get_sources()
		if indexPath.row() < len(sources):
			source = sources[indexPath.row()]
			cell.textLabel().text = source.name
			cell.detailTextLabel().text = PydiaKit.Sources.get_source_URLs()[source.identifier]
			cell.accessoryType = 1
		else:
			cell.textLabel().text = 'Failed to Load Source'
			cell.detailTextLabel().text = PydiaKit.Sources.get_unloaded_source_URLs()[indexPath.row() - len(sources)]
			cell.textLabel().textColor = UIColor.redColor()
			cell.detailTextLabel().textColor = UIColor.redColor()
			cell.selectionStyle = 0
	elif tableView.tag() == 2:
		updates = PydiaKit.Package.get_package_updates()
		if len(updates) > 0:
			package = updates[indexPath.row()]
			cell.textLabel().text = package.name
			cell.detailTextLabel().text = 'Version: %s (Installed Version: %s)' % (str(package.version), str(PydiaKit.Package.get_installed_package_for_identifier(package.identifier).version))
			cell.accessoryType = 1
		else:
			cell.textLabel().text = 'All Packages are Up to Date'
			cell.textLabel().textAlignment = 1
			cell.selectionStyle = 0
	elif tableView.tag() == 3:
		package = PydiaKit.Package.get_installed_packages()[indexPath.row()]
		cell.textLabel().text = package.name
		update = PydiaKit.Package.update_available_for_package(package)
		if update:
			cell.detailTextLabel().text = '[Update Available] Version: %s (Installed Version: %s)' % (str(update .version), str(package.version))
			cell.detailTextLabel().textColor = UIColor.greenColor()
		else:
			cell.detailTextLabel().text = 'Version: %s' % str(package.version)
		cell.accessoryType = 1
	elif tableView.tag() == 4:
		package = PydiaKit.Package.get_packages_for_search_text(str(searchBar.text()))[indexPath.row()]
		cell.textLabel().text = package.name
		cell.detailTextLabel().text = package.description
		cell.accessoryType = 1
	elif tableView.tag() == 5:
		if selectedSource:
			package = selectedSource.packages[indexPath.row()]
			cell.textLabel().text = package.name
			cell.detailTextLabel().text = package.description
			cell.accessoryType = 1
	elif tableView.tag() == 6:
		package = packageDetailsTableViewController.package
		if indexPath.section() == 0:
			cell.textLabel().text = package.name
			cell.textLabel().textAlignment = 1
		elif indexPath.section() == 1:
			update = PydiaKit.Package.update_available_for_package(package)
			if update:
				if indexPath.row() == 0:
					cell.textLabel().text = 'Version'
					cell.detailTextLabel().text = str(update.version)
				elif indexPath.row() == 1:
					cell.textLabel().text = 'Installed Version'
					installed_package = PydiaKit.Package.get_installed_package_for_identifier(package.identifier)
					cell.detailTextLabel().text = str(installed_package.version)
				elif indexPath.row() == 2:
					cell.textLabel().text = 'Author'
					cell.detailTextLabel().text = package.author
				elif indexPath.row() == 3:
					cell.textLabel().text = 'Source'
					source = PydiaKit.Sources.get_source_for_identifier(package.source_identifier)
					if source:
						cell.detailTextLabel().text = source.name
					else:
						cell.detailTextLabel().text = 'Unknown Source'
			else:
				if indexPath.row() == 0:
					cell.textLabel().text = 'Version'
					cell.detailTextLabel().text = str(package.version)
				elif indexPath.row() == 1:
					cell.textLabel().text = 'Author'
					cell.detailTextLabel().text = package.author
				elif indexPath.row() == 2:
					cell.textLabel().text = 'Source'
					source = PydiaKit.Sources.get_source_for_identifier(package.source_identifier)
					if source:
						cell.detailTextLabel().text = source.name
					else:
						cell.detailTextLabel().text = 'Unknown Source'
		elif indexPath.section() == 2:
			cell.textLabel().text = package.description
			cell.textLabel().numberOfLines = 0
		cell.selectionStyle = 0
		
	return cell.ptr
	
def tableView_didSelectRowAtIndexPath_(_self, _cmd, _tableView, _indexPath):

	tableView = ObjCInstance(_tableView)
	indexPath = ObjCInstance(_indexPath)
	
	if tableView.tag() == 1:
		if indexPath.row() < len(PydiaKit.Sources.get_sources()):
			global selectedSource
			selectedSource = PydiaKit.Sources.get_sources()[indexPath.row()]
			sourcesNavigationController.pushViewController_animated_(sourcePackagesTableViewController, True)
	elif tableView.tag() == 2:
		updates = PydiaKit.Package.get_package_updates()
		if len(updates):
			package = updates[indexPath.row()]
			packageDetailsTableViewController.package = package
			updatesNavigationController.pushViewController_animated_(packageDetailsTableViewController, True)
	elif tableView.tag() == 3:
		installed_package = PydiaKit.Package.get_installed_packages()[indexPath.row()]
		package = PydiaKit.Package.get_package_for_identifier(installed_package.identifier)
		packageDetailsTableViewController.package = package if package else installed_package
		installedNavigationController.pushViewController_animated_(packageDetailsTableViewController, True)
	elif tableView.tag() == 4:
		package = PydiaKit.Package.get_packages_for_search_text(str(searchBar.text()))[indexPath.row()]
		packageDetailsTableViewController.package = package
		searchNavigationController.pushViewController_animated_(packageDetailsTableViewController, True)
	elif tableView.tag() == 5:
		package = selectedSource.packages[indexPath.row()]
		packageDetailsTableViewController.package = package
		sourcesNavigationController.pushViewController_animated_(packageDetailsTableViewController, True)
		
def tableView_canEditRowAtIndexPath_(_self, _cmd, _tableView, _indexPath):

	tableView = ObjCInstance(_tableView)
	indexPath = ObjCInstance(_indexPath)
	if tableView.tag() == 1:
		return True
	return False
	
def tableView_editingStyleForRowAtIndexPath_(_self, _cmd, _tableView, _indexPath):

	tableView = ObjCInstance(_tableView)
	indexPath = ObjCInstance(_indexPath)
	if tableView.tag() == 1:
		return 1
	return 0
	
def tableView_commitEditingStyle_forRowAtIndexPath_(_self, _cmd, _tableView, editingStyle, _indexPath):
	import json
	
	tableView = ObjCInstance(_tableView)
	indexPath = ObjCInstance(_indexPath)
	
	if editingStyle == 1:
	
		sources_list_dir = os.path.expanduser('~/Documents')  + '/site-packages/Pydia/Pydia User Info/Sources.json'
		
		sources = json.load(open(sources_list_dir))
		
		source_identifier = None
		
		if indexPath.row() < len(PydiaKit.Sources.get_sources()):
			source_identifier = PydiaKit.Sources.get_sources()[indexPath.row()].identifier
		else:
			source_url = PydiaKit.Sources.get_unloaded_source_URLs()[indexPath.row() - len(PydiaKit.Sources.get_sources())]
			for identifier in PydiaKit.Sources.get_source_URLs():
				if PydiaKit.Sources.get_source_URLs()[identifier] == source_url:
					source_identifier = identifier
					break
					
		sources.pop(source_identifier, '')
		
		json.dump(sources, open(sources_list_dir, 'w'))
		
		PydiaKit.Sources.download_source_files()
		
		tableView.deleteRowsAtIndexPaths_withRowAnimation_([indexPath], 2)
		
def searchBar_textDidChange_(_self, _cmd, _searchBar, _searchText):
	searchTableViewController.tableView().reloadData()
	
def searchBarSearchButtonClicked_(_self, _cmd, _searchBar):
	searchBar.resignFirstResponder()
	
def searchBarCancelButtonClicked_(_self, _cmd, _searchBar):
	searchBar.resignFirstResponder()
	
if __name__ == '__main__':
	main()

