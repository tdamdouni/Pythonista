#!/usr/bin/env python
# Written by: DGC

# python imports

# local imports

#==============================================================================
class Box(object):
    
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("Box " + self.name + " Opened")
        return self

    def __exit__(self, exception_type, exception, traceback):
        all_none = all(
            arg is None for arg in [exception_type, exception, traceback]
            )
        if (not all_none):
            print("Exception: \"%s\" raised." %(str(exception)))
        print("Box Closed")
        print("")
        return all_none

#==============================================================================
if (__name__ == "__main__"):
    with Box("tupperware") as simple_box:
        print("Nothing in " + simple_box.name)
    with Box("Pandora's") as pandoras_box:
        raise Exception("All the evils in the world")
    print("end")
