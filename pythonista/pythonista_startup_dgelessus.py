# https://gist.github.com/dgelessus/fe8e267149862eb67127f4fff7e017be

# This is an example pythonista_startup.py script.
# The code below is from https://github.com/dgelessus/pythonista_startup/blob/master/enable_faulthandler.py

from __future__ import absolute_import, division, print_function

def enable_faulthandler():
	import ctypes
	import datetime
	import errno
	import io
	import objc_util
	import os
	import shutil
	import sys
	
	try:
		unicode
	except NameError:
		unicode = str
		
	print(u"Enabling fault handler and Objective-C exception handler...")
	
	LOGDIR = os.path.expanduser(u"~/Documents/faultlog")
	LOGNAME_TEMPLATE = u"faultlog-{:%Y-%m-%d-%H-%M-%S}.txt"
	LOGNAME_DEFAULT = u"faultlog-temp.txt"
	EXCEPTIONLOGNAME_DEFAULT = u"exceptionlog-temp.txt"
	
	# Create the faultlog directory if necessary
	try:
		os.mkdir(LOGDIR)
	except (IOError, OSError) as err:
		if err.errno != errno.EEXIST:
			raise
			
	# Check whether an Objective-C exception log exists and append it to the fault log
	try:
		fin = io.open(os.path.join(LOGDIR, EXCEPTIONLOGNAME_DEFAULT), "rb")
	except (IOError, OSError) as err:
		if err.errno != errno.ENOENT:
			raise
	else:
		with fin:
			data = fin.read()
			
		if data:
			with io.open(os.path.join(LOGDIR, LOGNAME_DEFAULT), "ab") as fout:
				# If the faultlog is not empty, add a separator
				if fout.tell() != 0:
					fout.write(b"\n" + b"-"*72 + b"\n\n")
					
				fout.write(data)
				
		os.remove(os.path.join(LOGDIR, EXCEPTIONLOGNAME_DEFAULT))
		
	# Check whether a faultlog was written
	did_fault = False
	
	try:
		f = io.open(os.path.join(LOGDIR, LOGNAME_DEFAULT), "rb")
	except (IOError, OSError) as err:
		if err.errno != errno.ENOENT:
			raise
	else:
		with f:
			if f.read(1):
				did_fault = True
				
	# Notify the user that a crash has happened
	if did_fault:
		print(u"Pythonista quit abnormally last time.", file=sys.stderr)
		
		stamped_name = LOGNAME_TEMPLATE.format(datetime.datetime.fromtimestamp(os.stat(os.path.join(LOGDIR, LOGNAME_DEFAULT)).st_mtime))
		shutil.move(os.path.join(LOGDIR, LOGNAME_DEFAULT), os.path.join(LOGDIR, stamped_name))
		print(u"For details, see the log file '{}'.".format(stamped_name), file=sys.stderr)
		
	if sys.version_info < (3,):
		print(u"Setting exception handler.")
		# Set the Objective-C exception handler only under Python 2.
		# Otherwise under Pythonista 3 it would be set twice - once by Python 2 and once by Python 3.
		# This way the exception handler is set exactly once and works under Pythonista 2 and 3.
		
		# typedef void (*objc_uncaught_exception_handler)(id exception);
		objc_uncaught_exception_handler = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
		
		# objc_uncaught_exception_handler objc_setUncaughtExceptionHandler(objc_uncaught_exception_handler fn);
		objc_util.c.objc_setUncaughtExceptionHandler.argtypes = [objc_uncaught_exception_handler]
		objc_util.c.objc_setUncaughtExceptionHandler.restype = objc_uncaught_exception_handler
		
		# Set Objective-C uncaught exception handler
		@objc_uncaught_exception_handler
		def handler(exc_pointer):
			exc = objc_util.ObjCInstance(exc_pointer)
			
			name = exc.name()
			reason = exc.reason()
			user_info = exc.userInfo()
			
			call_stack_symbols = exc.callStackSymbols()
			
			with io.open(os.path.join(LOGDIR, EXCEPTIONLOGNAME_DEFAULT), "wb") as f:
				try:
					f.write(b"Objective-C exception details:\n\n")
					
					if reason is None:
						f.write(str(name).encode("utf-8") + b"\n")
					else:
						f.write(str(name).encode("utf-8") + b": " + str(reason).encode("utf-8") + b"\n")
						
					if user_info is not None:
						f.write(str(user_info).encode("utf-8") + b"\n")
						
					f.write(b"\nStack trace:\n\n")
					
					for sym in call_stack_symbols:
						f.write(str(sym).encode("utf-8") + b"\n")
						
					f.write(b"\nEnd of exception details.\n")
				except Exception as err:
					import traceback
					f.write(b"I messed up! Python exception:\n")
					f.write(traceback.format_exc().encode("utf-8"))
					raise
					
		# The exception handler must be kept in some kind of permanent location, otherwise it will be collected by the garbage collector, because there are no more references to it from Python.
		objc_util._dgelessus_pythonista_startup_exception_handler = handler
		objc_util.c.objc_setUncaughtExceptionHandler(handler)
	else:
		# The faulthandler module is only available under Python 3.
		print("Setting fault handler.")
		
		import faulthandler
		
		logfile = io.open(os.path.join(LOGDIR, LOGNAME_DEFAULT), "wb")
		faulthandler.enable(logfile)
		
	print(u"Done enabling fault handler and Objective-C exception handler.")
	
enable_faulthandler()

