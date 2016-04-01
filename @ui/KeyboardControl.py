# -*- coding: utf-8 -*-

import ui

DEFAULT_TEXT = "w\n\nw w WWWW w w\n\nw"
DEFAULT_LEN = len(DEFAULT_TEXT)
DEFAULT_MID = DEFAULT_LEN/2
DEFAULT_RNG = (DEFAULT_MID, DEFAULT_MID)

class KBControlDelegate(object):
    def __init__(self):
        self.bksp = False
    
    def keypress(self, key):
        out.text += key + " "
    
    def textview_should_change(self, textview, range, replacement):
        if replacement == "":
            # some deletion
            if range == (DEFAULT_MID-1, DEFAULT_MID):
                self.keypress("bksp")
        elif len(replacement) > 1:
            # paste
            self.keypress("cmd-v")
        else:
            self.keypress(replacement)
        return False
    
    def textview_did_change_selection(self, textview):
        nop = False
        if len(ctrl.text) == DEFAULT_LEN:
            # no change to text, only selection
            if ctrl.selected_range == DEFAULT_RNG:
                # no important changes, cursor was likely reset by script
                nop = True
            elif ctrl.selected_range[0] == ctrl.selected_range[1]:
                # shift was not used
                if ctrl.selected_range == (0, 0):
                    # cursor is at the top
                    self.keypress("cmd-up")
                elif ctrl.selected_range in ((1, 1), (2, 2)):
                    # cursor is near the top
                    self.keypress("up")
                elif ctrl.selected_range == (3, 3):
                    # cursor is at the left
                    self.keypress("cmd-left")
                elif ctrl.selected_range == (DEFAULT_LEN/2-2, DEFAULT_LEN/2-2):
                    # cursor is exactly two chars to the left
                    self.keypress("alt-left")
                elif ctrl.selected_range == (DEFAULT_LEN/2-1, DEFAULT_LEN/2-1):
                    # cursor is exactly one char to the left
                    self.keypress("left")
                elif ctrl.selected_range == (DEFAULT_LEN/2+1, DEFAULT_LEN/2+1):
                    # cursor is exactly one char to the right
                    self.keypress("right")
                elif ctrl.selected_range == (DEFAULT_LEN/2+2, DEFAULT_LEN/2+2):
                    # cursor is exactly two chars to the right
                    self.keypress("alt-right")
                elif ctrl.selected_range == (DEFAULT_LEN-3, DEFAULT_LEN-3):
                    # cursor is at the right
                    self.keypress("cmd-right")
                elif ctrl.selected_range in ((DEFAULT_LEN-2, DEFAULT_LEN-2), (DEFAULT_LEN-1, DEFAULT_LEN-1)):
                    # cursor is near the bottom
                    self.keypress("down")
                elif ctrl.selected_range == (DEFAULT_LEN, DEFAULT_LEN):
                    # cursor is at the bottom
                    self.keypress("cmd-down")
                else:
                    # some unhandled movement
                    nop = True
                    self.keypress(str(ctrl.selected_range))
            else:
                # shift was used
                if ctrl.selected_range == (0, DEFAULT_MID):
                    # cursor is at the top
                    self.keypress("shift-cmd-up")
                elif ctrl.selected_range in ((1, DEFAULT_MID), (2, DEFAULT_MID)):
                    # cursor is near the top
                    self.keypress("shift-up")
                elif ctrl.selected_range == (3, DEFAULT_MID):
                    # cursor is at the left
                    self.keypress("shift-cmd-left")
                elif ctrl.selected_range == (DEFAULT_LEN/2-2, DEFAULT_MID):
                    # cursor is exactly two chars to the left
                    self.keypress("shift-alt-left")
                elif ctrl.selected_range == (DEFAULT_LEN/2-1, DEFAULT_MID):
                    # cursor is exactly one char to the left
                    self.keypress("shift-left")
                elif ctrl.selected_range == (DEFAULT_MID, DEFAULT_LEN/2+1):
                    # cursor is exactly one char to the right
                    self.keypress("shift-right")
                elif ctrl.selected_range == (DEFAULT_MID, DEFAULT_LEN/2+2):
                    # cursor is exactly two chars to the right
                    self.keypress("shift-alt-right")
                elif ctrl.selected_range == (DEFAULT_MID, DEFAULT_LEN-3):
                    # cursor is at the right
                    self.keypress("shift-cmd-right")
                elif ctrl.selected_range in ((DEFAULT_MID, DEFAULT_LEN-2), (DEFAULT_MID, DEFAULT_LEN-1)):
                    # cursor is near the bottom
                    self.keypress("shift-down")
                elif ctrl.selected_range == (DEFAULT_MID, DEFAULT_LEN):
                    # cursor is at the bottom
                    self.keypress("shift-cmd-down")
                else:
                    # some unhandled movement
                    nop = True
                    self.keypress(str(ctrl.selected_range))
            
        elif len(ctrl.text) == DEFAULT_LEN - 1:
            # exactly one character was removed
            # due to the nature of bksp, this is only triggered for delete (fn-bksp)
            self.keypress("del")
        elif len(ctrl.text) < DEFAULT_LEN:
            # more than one character was deleted, i. e. alt-bksp
            self.keypress("alt-bksp")
        elif len(ctrl.text) > DEFAULT_LEN:
            # one or more characters were added and not handled by should_change
            # i. e. sticky key/accentuation character, need manual reset of control field
            # accented chars can still be typed
            pass
        else:
            # some unknown situation
            out.text += "\nSome unhandled situation: " + ctrl.selected_range + "\n" + ctrl.text + "\n\n"
        
        if not nop:
            ctrl.text = DEFAULT_TEXT
            ctrl.selected_range = DEFAULT_RNG

def run():
    global root
    global ctrl
    global out
    root = ui.load_view()
    ctrl = root["ctrl"]
    out = root["out"]
    ctrl.delegate = KBControlDelegate()
    
    root.present("sheet")

if __name__ == "__main__":
    run()
