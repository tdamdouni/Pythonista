#!/usr/bin/env python

# https://forum.omz-software.com/topic/3826/tool-extension-arguments-not-in-sys-argv

import sys
import editor
print(sys.argv)

if sys.argv[-1] == editor.get_path():
	args = parser.parse_args(sys.argv[1:-1])
else:
	args = parser.parse_args()
