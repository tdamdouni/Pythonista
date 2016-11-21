# coding: utf-8

# https://forum.omz-software.com/topic/2869/putting-doctests-into-a-separate-file/2

import doctest, editor
doctest.testfile(editor.get_path(), module_relative=False)

