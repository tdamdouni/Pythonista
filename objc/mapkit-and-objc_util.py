from __future__ import print_function
# https://forum.omz-software.com/topic/1972/beta-fun-with-mapkit-and-objc_util/7

import os
p = os.path.abspath(os.path.join(os.__file__, '../../clearglobals.py'))
with open(p) as f:
	print(f.read())
# --------------------

# ...
existing_view = toolbar.viewWithTag_(42)
if existing_view:
	existing_view.removeFromSuperview()
ObjCInstance(replacement_view).setTag_(42)
toolbar.addSubview_(replacement_view)
# ...

