# coding: utf-8

# https://forum.omz-software.com/topic/2729/omz-dropboxfilepicker-synchronous-version/2

def run_async(func):
   from threading import Thread
   from functools import wraps

   @wraps(func)
   def async_func(*args, **kwargs):
      func_hl = Thread(target = func, args = args, kwargs = kwargs)
      func_hl.start()
      return func_hl

   return async_func

#==============================

_USE_ASYNC = False

def cond_decorator(func):
    from threading import Thread
    from functools import wraps
    
    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl
    
    if _USE_ASYNC:
        return async_func
    else:
        return ui.in_background(func)
