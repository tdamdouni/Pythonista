#!/usr/bin/env python
########################################################################.......
"""filenav for Pythonista, version 2, by dgelessus.
This script automatically runs the version of filenav best for the
current resolution, i. e. `full.py` on width >= 768 and `slim.py` on
anything smaller than that.
"""

from __future__ import division, print_function

import sys
import ui

def main(args):
    if ui.get_screen_size()[0] >= 768:
        from filenav import full
        full.main(args)
    else:
        from filenav import slim
        slim.main(args)

if __name__ == "__main__":
    main(sys.argv[1:])
