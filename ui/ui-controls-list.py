#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/1764/getting-a-list-of-all-ui-gui-classes-programmatically/11

from __future__ import print_function
import ui

x = [cls for cls in vars(ui).values() if hasattr(cls, 'alpha') and not issubclass(cls, ui.TableViewCell)]
print(x, len(x))

