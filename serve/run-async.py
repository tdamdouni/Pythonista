def run_async(func):
	from threading import Thread
	from functools import wraps
	
	@wraps(func)
	def async_func(*args, **kwargs):
		func_hl = Thread(target = func, args = args, kwargs = kwargs)
		func_hl.start()
		return func_hl
		
	return async_func

