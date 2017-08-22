# https://forum.omz-software.com/topic/4175/stash-is-it-possible-to-get-color-output-from-a-script-to-the-stash-console/28

graphics# --------------------
        30: "black",
        31: "red",
        32: "green",
        33: "brown",
        34: "blue",
        35: "magenta",
        36: "cyan",
        37: "white",
        39: "default",  # white.
        50: "gray",
        51: "yellow",
        52: "smoke",
# --------------------
class stashansi:
    fore_red = "\x9b31m"
    fore_blue = "\x9b34m"
    fore_end = "\x9b39m"
    back_red = "\x9b41m"
    back_blue = "\x9b44m"
    back_end = "\x9b49m"
    bold = "\x9b1m"
    underline = "\x9b4m"
    all_end = "\9x0m"

print(stashansi.back_blue + stashansi.fore_red + "Hello world" + back_end + "This is just red with no blue background" + fore_end + "Now it's all just normal text...")
# --------------------
def getTerminalColorClass():
    if _stash != None:
        return StashTerminalColors()
    
    return TerminalColors()
    

class TerminalColors(object):
    """
    here is a good url for the different colors and things:
        http://blog.taylormcgann.com/tag/prompt-color/
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    DARK_BLUE = '\033[34m'
    GREEN = '\033[92m'
    DARK_GREEN = '\033[32m'
    YELLOW = '\033[93m'
    DARK_YELLOW = '\033[33m'
    RED = '\033[91m'
    DARK_RED = '\033[31m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    WHITE = '\033[97m'
    PURPLE = '\033[95m'
    DARK_PURPLE = '\033[35m'
    END = '\033[0m'

    def __init__(self):
        pass

    def simple_print(self, color, str_msg):
        print( "%s%s" % (self.get_color_string(color, str_msg), self.END))

    def complex_print(self, color, str_format, data):
        str_msg = str_format % data
        self.simple_print( color, str_msg )
        
    def multi_color_print(self, color_str_tuple_list):
        str_msg = ""
        for clr, str in color_str_tuple_list:
            str_msg += self.get_color_string(clr, str)
        self.println(str_msg)
        
    def get_color_string(self, color, str_msg):
        return "%s%s" % (color, str_msg)
        
    def println(self, str_msg):
        print( "%s%s" % (str_msg, self.END) )


class StashTerminalColors (object):
    
    # from shcommon.py in stash code
    
    HEADER = 'UNDERLINE'
    BLACK = 'black'
    RED = 'red'
    GREEN = 'green'
    BROWN = 'brown'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    PURPLE = 'magenta'
    CYAN = 'cyan'
    WHITE = 'white'
    GRAY = 'gray'
    YELLOW = 'yellow'
    SMOKE = 'smoke'
    DEFAULT = 'white'
    STRIKE = 'STRIKE'
    BOLD = 'BOLD'
    UNDERLINE = 'UNDERLINE'
    BOLD_ITALIC = 'BOLD_ITALIC'
    ITALIC = 'ITALIC'
    END = 'END'
        
    def __init__(self):
        self._stash = _stash
        
    def simple_print(self, color, str_msg): 
        print("%s" % self.get_color_string(color, str_msg))
        
    def get_color_string(self, color, str_msg):
        if color == self.BOLD:
            prn_str = _stash.text_bold(str_msg)
        elif color == self.UNDERLINE:
            prn_str = _stash.text_underline(str_msg)
        elif color == self.BOLD_ITALIC:
            prn_str = _stash.text_bold_italic(str_msg)
        elif color == self.ITALIC:
            prn_str = _stash.text_italic(str_msg)
        elif color == self.STRIKE:
            prn_str = _stash.text_strikethrough(str_msg)
        else:
            prn_str = _stash.text_color(str_msg, color)
            
        return prn_str
        
    def multi_color_print(self, color_str_tuple_list):
        str_msg = ""
        for clr, str in color_str_tuple_list:
            str_msg += self.get_color_string(clr, str)
        print(str_msg)
        
# --------------------
tc = getTerminalColorClass()

tc.simple_print(tc.BLUE, "this should be BLUE")
print("hopefully, this is NOT blue")
tc.simple_print(tc.DEFAULT, "this is the DEFAULT color (white)")
tc.simple_print(tc.BROWN, "this is BROWN text")
tc.simple_print(tc.BOLD, "this should be BOLD")
tc.simple_print(tc.UNDERLINE, "this should be UNDERLINE")
tc.simple_print(tc.STRIKE, "this should be STRIKETHROUGH")
tc.simple_print(tc.ITALIC, "this should be ITALIC")
tc.simple_print(tc.BOLD_ITALIC, "this should be BOLD ITALIC")
   

# will combine multiple effects
msg = '\n  ID  Status   Date(-t)           Owner(-u)   Description (-d)\n'
tc.simple_print(self.tc.BOLD + self.tc.UNDERLINE, msg)
# --------------------
def print_status_footer():
    tc = getTerminalColorClass()

    # statusLine = "Status: [+]add [@]block [-]reject [*]accept [#]workon [.]finish"
    prn_list = [
        (tc.WHITE,      "Status: "),
        (get_color_for_status('+'), "[+]add "),
        (get_color_for_status('@'), "[@]block "),
        (get_color_for_status('-'), "[-]reject "),
        (get_color_for_status('*'), "[*]accept "),
        (get_color_for_status('#'), "[#]workon "),
        (get_color_for_status('.'), "[.]finish ")
    ]
    tc.multi_color_print(prn_list)
    tc.simple_print(tc.WHITE, "        ST=status  PR=priority")
# --------------------
def getTerminalColorClass():
    if '_stash' in globals() or '_stash' in locals():
        if _stash != None:
            return StashTerminalColors()
    
    return TerminalColors()
# --------------------
