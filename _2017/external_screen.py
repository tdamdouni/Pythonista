# https://gist.github.com/zrzka/8b83d3f8cb998e185c482b3d5b116267

import objc_util
import logging

_logger = None

# External screen notifications listener
_listener = None

# External screen (UIScreen) if available
_screen = None

# External screen window (UIWindow) if external screen is available
_window = None

# Handlers user can add/remove to be informed about external screen connection changes
_connected_handlers = []
_disconnected_handlers = []

__all__ = [
	'register_connected_handler',
	'unregister_connected_handler',
	'register_disconnected_handler',
	'unregister_disconnected_handler',
	'present',
	'dismiss',
	'init',
	'terminate'
]

def register_connected_handler(handler):
	'''Registers external screen connection handler which will be called upon screen connection.
	'''
	_connected_handlers.append(handler)
	
	
def unregister_connected_handler(handler):
	'''Removes previously registered screen connection handler.
	'''
	_connected_handlers.remove(handler)


def register_disconnected_handler(handler):
	'''Register external screen connection handler which will be called upon screen disconnection.
	'''
	_disconnected_handlers.append(handler)
	

def unregister_disconnected_handler(handler):
	'''Removes previously registered screen disconnection handler.
	'''
	_disconnected_handlers.remove(handler)


@objc_util.on_main_thread
def _configure_window():
	'''Returns external screen window (UIWindow) if available. Otherwise it returns None.
	'''
	global _screen, _window
	
	if _screen is None:
		# Useful during initialization where external screen is already connected
		#  -> notification will not fire
		
		screens = objc_util.ObjCClass('UIScreen').screens()
		if len(screens) > 1:
			_screen = screens[1]
		else:
			_logger.debug('Unable to configure window, external screen not available')
			return None
			
	if _screen == None:
		_logger.debug('Unable to configure window, external screen not available')
		return None
		
	if _window is None:
			UIWindow = objc_util.ObjCClass('UIWindow')
			_window = UIWindow.alloc().initWithFrame(_screen.bounds())
			_window.setScreen(_screen)
			_window.setHidden(False)
			_logger.debug('External screen window configured')
			
	return _window
	

@objc_util.on_main_thread	
def _discard_window():
	global _window
	
	if _window is not None:
		_window.setScreen(None)
		_window.setHidden(True)
		_window = None
		_logger.debug('External screen window discarded')	
		
		
@objc_util.on_main_thread		
def _discard_screen():
	global _screen
	_discard_window()
	_screen = None
			

def screenDidConnectNotification_(self, cmd, note):
	global _screen
	_logger.debug('External screen connected')
	_screen = objc_util.ObjCInstance(note).object()
	
	for handler in _connected_handlers:
		handler()


def screenDidDisconnectNotification_(self, cmd, note):
	_logger.debug('External screen disconnected')
	_discard_screen()
	
	for handler in _disconnected_handlers:
		handler()


@objc_util.on_main_thread
def _start_notification_listener():
	global _listener
	if _listener is not None:
		_logger.debug('External screen notification listener is already running')
		return
		
	methods = [screenDidConnectNotification_, screenDidDisconnectNotification_]
	listener_class = objc_util.create_objc_class('ExternalScreenListener', methods=methods)
	_listener = listener_class.alloc().init()
	
	NSNotificationCenter = objc_util.ObjCClass('NSNotificationCenter')
	default_center = NSNotificationCenter.defaultCenter()
	
	default_center.addObserver_selector_name_object_(_listener, objc_util.sel('screenDidConnectNotification:'),
		'UIScreenDidConnectNotification', None)
	default_center.addObserver_selector_name_object_(_listener, objc_util.sel('screenDidDisconnectNotification:'),
		'UIScreenDidDisconnectNotification', None)	
	
	_logger.debug('External screen notification listener started')
	

@objc_util.on_main_thread
def _stop_notification_listener():
	global _listener
	if _listener is None:
		_logger.debug('External screen notification listener is not running')
		return
		
	NSNotificationCenter = objc_util.ObjCClass('NSNotificationCenter')
	default_center = NSNotificationCenter.defaultCenter()
	default_center.removeObserver(_listener)
	_listener = None	
	
	_logger.debug('External screen notification listener stopped')


@objc_util.on_main_thread
def present(view):
	'''Presents view (ui.View) on external screen.
	
	Returns True if view was presented or False if external screen is not
	available.
	'''
	window = _configure_window()
	if window is None:
		_logger.debug('Unable to present view, external screen is not available')
		return False

	view.flex = 'WH'
	view_objc = objc_util.ObjCInstance(view)
	view_objc.setFrame(window.bounds())

	window.subviews().makeObjectsPerformSelector(objc_util.sel('removeFromSuperview'))
	window.addSubview(view_objc)
	
	_logger.debug('View presented on external screen')
	return True
	
	
@objc_util.on_main_thread
def dismiss(view):
	'''Dismisses view (ui.View) from external screen.
	
	View must be presented on external screen otherwise nothing happens.
	'''
	view_objc = objc_util.ObjCInstance(view)
	
	if view_objc.superview() == _window:
		view_objc.removeFromSuperview()
		_logger.debug('View dismissed from external screen')
	else:
		_logger.debug('View is not presented on external screen, skipping dismiss')


def init(log_level=logging.NOTSET):
	'''Starts notification listener and setups logging facility.
	'''
	global _logger
	_logger = logging.getLogger('external_screen')
	_logger.addHandler(logging.StreamHandler())
	_logger.setLevel(log_level)
	_start_notification_listener()

def terminate():
	'''Stops notification listener, discards screen, handlers and logging facility.
	'''
	global _logger
	_stop_notification_listener()
	_discard_screen()
	del _connected_handlers[:]
	del _disconnected_handlers[:]
	_logger.handlers = []
	_logger = None
	
