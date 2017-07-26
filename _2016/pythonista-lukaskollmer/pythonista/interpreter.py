# https://github.com/lukaskollmer/pythonista

"""
Interact with the interpreter

Use the `run` function to execute a python file
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import _utils

_utils.guard_objc_util()

import objc_util


PythonInterpreter = objc_util.ObjCClass('PythonInterpreter')

def run(file):
	script = open(file).read()
	interpreter = PythonInterpreter.sharedInterpreter()
	interpreter.run_asFile_(script, file)
