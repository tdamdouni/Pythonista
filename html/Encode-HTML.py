# -*- coding: utf-8 -*-
from __future__ import print_function
import clipboard
text = clipboard.get()
from bs4.dammit import EntitySubstitution
print(EntitySubstitution.substitute_html(text))

