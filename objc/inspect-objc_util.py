# coding: utf-8

import objc_util

{name for name in dir(objc_util) if not name.startswith("_")} - {
    "ctypes",
    "inspect",
    "itertools",
    "os",
    "pp",
    "re",
    "string",
    "sys",
    "ui", 
    "weakref",
}

#==============================

import objc_util

{name for name in dir(objc_util)
      if not name.startswith("_") and
         not inspect.ismodule(getattr(objc_util, name))
}

