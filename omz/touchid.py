# coding: utf-8

# https://forum.omz-software.com/topic/2156/share-code-touch-id-authentication-in-pythonista

# https://gist.github.com/omz/66a763a9db15dc847690

from __future__ import print_function
from objc_util import * 
import threading

NSBundle = ObjCClass('NSBundle')
LocalAuthentication = NSBundle.bundleWithPath_('/System/Library/Frameworks/LocalAuthentication.framework')
LocalAuthentication.load()
LAContext = ObjCClass('LAContext')

# authenticate() will raise one of these exceptions when authentication
# fails. They all derive from AuthFailedException, so you can catch that
# if you don't care about the failure reason, but you could also handle
# cancellation differently, for example.
class AuthFailedException (Exception): pass
class AuthCancelledException (AuthFailedException): pass
class AuthTimeoutException (AuthFailedException): pass
class AuthNotAvailableException (AuthFailedException): pass
class AuthFallbackMechanismSelectedException (AuthFailedException): pass

def is_available():
	'''Return True if TouchID authentication is available, False otherwise'''
	context = LAContext.new().autorelease()
	return bool(context.canEvaluatePolicy_error_(1, None))

def authenticate(reason='', allow_passcode=True, timeout=None):
	'''Authenticate the user via TouchID or passcode. Returns True on success, raises AuthFailedException (or a subclass) otherwise.'''
	if not is_available():
		raise AuthNotAvailableException('Touch ID is not available.')
	policy = 2 if allow_passcode else 1
	context = LAContext.new().autorelease()
	event = threading.Event()
	result = {}
	def callback(_cmd, success, _error):
		result['success'] = success
		if _error:
			error = ObjCInstance(_error)
			result['error'] = error
		event.set()
	handler = ObjCBlock(callback, restype=None, argtypes=[c_void_p, c_bool, c_void_p])
	context.evaluatePolicy_localizedReason_reply_(policy, reason, handler)
	if not event.wait(timeout):
		#NOTE: invalidate() is a private method (there's apparently no public API to cancel the TouchID dialog)
		context.invalidate()
		raise AuthTimeoutException('Timeout')
	success = result.get('success', False)
	error = result.get('error')
	if success:
		return True
	elif error:
		error_code = error.code()
		if error_code == -2:
			raise AuthCancelledException('Cancelled by user')
		elif error_code == -3:
			raise AuthFallbackMechanismSelectedException('Fallback authentication mechanism selected')
		else:
			desc = error.localizedDescription() or 'Unknown error'
			raise AuthFailedException(desc)
	else:
		raise AuthFailedException('Unknown error')

# Demo:
def main():
	try:
		reason = 'We need you fingerprint to ste...ehm... to log you in. You have 10 seconds.'
		authenticate(reason, allow_passcode=True, timeout=10)
		print('Success!')
	except AuthFailedException as e:
		print(e)

if __name__ == '__main__':
	main()
