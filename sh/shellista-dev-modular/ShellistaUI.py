# -*- coding: utf-8 -*-

# change the module names to fit your Shellista installation
try:
    import shellista
    reload(shellista)
    from shellista import * # need to emulate the real Shellista for certain plugins to work correctly
except ImportError:
    print("Failed to import Shellista. Make sure that the module name is correct.")

shellista._check_for_plugins()

import sys
import ui

STDIN = sys.stdin
STDOUT = sys.stdout

SHELL_FONT = ("DejaVuSansMono", 12)

class ShellistaUI(object):
    root = None
    txts = None
    inp = None
    out = None
    hist_up = None
    hist_down = None
    
    input_did_return = False
    out_buf = ""
    in_prompt = ""
    in_hist = []
    in_hist_pos = 0
    
    sh = None
    
    old_precmd = None
    old_postcmd = None
    
    def _precmd(self, line):
        if line == "clear" or line.startswith("clear"):
            self.clear()
        # redirect stdin and stdout during command execution
        sys.stdin = self
        sys.stdout = self
        line = self.old_precmd(line)
        return line
    
    def _postcmd(self, stop, line):
        stop = self.old_postcmd(stop, line)
        # reset stdin and stdout
        sys.stdin = STDIN
        sys.stdout = STDOUT
        return stop
    
    def __init__(self):
        self.out_buf = ""
        
        # set up root view
        self.root = ui.View(name="Shellista", flex="WH")
        self.root.background_color = 0
        
        # set up text area wrapper view
        self.txts = ui.View(flex="WH")
        self.root.add_subview(self.txts)
        self.txts.background_color = 0
        #self.txts.border_width = 2
        #self.txts.border_color = 1
        
        # set up input text field
        self.inp = ui.TextField(flex="WT")
        self.txts.add_subview(self.inp)
        self.inp.height = SHELL_FONT[1] + 2
        self.inp.y = self.inp.superview.height - (self.inp.height + 14)
        self.inp.background_color = 0
        self.inp.bordered = False
        self.inp.clear_button_mode = "always"
        
        # set up output text view
        self.out = ui.TextView()
        self.txts.add_subview(self.out)
        self.out.height = self.out.superview.height - (self.inp.height + 14)
        self.out.flex = "WH"
        self.out.auto_content_inset = False # appears to be broken
        self.out.editable = False
        self.out.content_inset = (0, 0, -8, 0)
        self.out.indicator_style = "white"
        
        # set up common text area settings
        self.out.delegate = self.inp.delegate = self
        self.out.background_color = self.inp.background_color = 0.0
        self.out.text_color = self.inp.text_color = 0.9
        self.out.font = self.inp.font = SHELL_FONT
        self.out.autocapitalization_type = self.inp.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
        self.out.autocorrection_type = self.inp.autocorrection_type = False
        self.out.spellchecking_type = self.inp.spellchecking_type = False
        self.out.text = self.inp.text = ""
        
        # set up command history buttons
        self.hist_up = ui.Button()
        self.txts.add_subview(self.hist_up)
        self.hist_up.width = self.hist_up.height = 50
        self.hist_up.x = self.hist_up.superview.width - 105
        self.hist_up.y = self.hist_up.superview.height - self.inp.height - 70
        self.hist_up.flex = "TL"
        self.hist_up.action = self.do_hist_up
        self.hist_up.font = ("<system>", 48)
        self.hist_up.title = "🔼"
        
        self.hist_dn = ui.Button()
        self.txts.add_subview(self.hist_dn)
        self.hist_dn.width = self.hist_dn.height = 50
        self.hist_dn.x = self.hist_dn.superview.width - 55
        self.hist_dn.y = self.hist_dn.superview.height - self.inp.height - 70
        self.hist_dn.flex = "TL"
        self.hist_dn.action = self.do_hist_dn
        self.hist_dn.font = ("<system>", 48)
        self.hist_dn.title = "🔽"
        
        # set up Shellista
        self.sh = Shellista(stdin=self, stdout=self)
        self.sh.use_rawinput = False
        
        self.old_precmd = self.sh.precmd
        self.old_postcmd = self.sh.postcmd
        
        self.sh.precmd = self._precmd
        self.sh.postcmd = self._postcmd
    
    def run(self):
        self.root.present("panel")
        self.inp.begin_editing()
        try:
            self.sh.cmdloop()
        finally:
            sys.stdin = STDIN
            sys.stdout = STDOUT
            self.write("Connection closed.\n")
            self.flush()
            self.inp.enabled = False
            self.root.close()
    
    def do_hist_up(self, sender):
        if self.in_hist_pos < len(self.in_hist):
            self.in_hist_pos += 1
        
        hist = [""] + self.in_hist
        self.inp.text = self.in_prompt + hist[self.in_hist_pos]
    
    def do_hist_dn(self, sender):
        if self.in_hist_pos > 0:
            self.in_hist_pos -= 1
        
        hist = [""] + self.in_hist
        self.inp.text = self.in_prompt + hist[self.in_hist_pos]
    
    # input stream methods
    encoding = "utf8"
    
    def read(self):
        return self.readline()
    
    def readline(self, limit=-1):
        while not self.input_did_return:
            pass
        self.input_did_return = False
        
        if limit < 0:
            ret = self.inp.text[len(self.in_prompt):]
        else:
            ret = self.inp.text[len(self.in_prompt):int(limit)]
        
        self.in_hist[0:0] = [ret]
        self.in_hist_pos = 0
        self.inp.text = self.in_prompt
        self.write(ret + "\n")
        self.flush()
        return ret
    
    # output stream methods
    softspace = 0
    
    def clear(self):
        self.out.text = ""
        self.out_buf = ""
        self.in_prompt = ""
    
    def flush(self):
        lines = self.out_buf.splitlines(True)
        if lines[-1][-1] == "\n":
            self.in_prompt = ""
            self.inp.text = ""
            self.out.text = "".join(lines)[:-1]
        else:
            itext = self.inp.text[len(self.in_prompt):]
            self.in_prompt = lines[-1]
            self.out.text = "".join(lines[:-1])[:-1]
            self.inp.text = self.in_prompt + itext
        #self.out_buf = ""
        self.out.content_offset = (0, self.out.content_size[1] - self.out.height)
    
    def write(self, data):
        self.out_buf += data
    
    def writelines(self, lines):
        for line in lines:
            self.write(line + "\n")
    
    # ui.TextView.delegate methods
    def textview_should_begin_editing(self, textview):
        return True
    
    def textview_did_begin_editing(self, textview):
        pass
    
    def textview_did_end_editing(self, textview):
        pass
    
    def textview_should_change(self, textview, range, replacement):
        if range[0] < len(self.in_prompt) or range[1] < len(self.in_prompt):
            return False
        else:
            return True
    
    def textview_did_change(self, textview):
        pass
    
    def textview_did_change_selection(self, textview):
        pass
    
    # ui.TextField.delegate methods
    def textfield_should_begin_editing(self, textfield):
        return True
    
    def textfield_did_begin_editing(self, textfield):
        if textfield == self.inp:
            def _set_frame():
                kbf = ui.get_keyboard_frame()
                if kbf[1] > 0:
                    self.txts.height = self.root.height - kbf[3]
            ui.delay(_set_frame, 0.55) # wait for the keyboard to slide up
    
    def textfield_did_end_editing(self, textfield):
        pass
    
    def textfield_should_return(self, textfield):
        self.input_did_return = True
        return True
    
    def textfield_should_change(self, textfield, range, replacement):
        return True
    
    def textfield_did_change(self, textfield):
        self.out.content_offset = (0, self.out.content_size[1] - self.out.height)

if __name__ == "__main__":
    global shui
    
    shui = ShellistaUI()
    shui.run()
