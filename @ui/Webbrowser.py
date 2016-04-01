# coding: utf-8

import ui

favorites_html = '''<HTML><HEAD></HEAD><BODY><H1><P>
    <a href="http://www.yahoo.com">Yahoo</a><br>
    <a href="http://www.cnn.com">CNN</a> News<br>
    <a href="http://www.google.com/search?&tbm=nws&as_q=python+language">Google News (Python)</a><br>
    <a href="http://www.picsearch.com">picsearch</a><br>
    <a href="http://omz-forums.appspot.com/pythonista">Pythonista Forum</a><br>
</P></H1></BODY></HTML>'''

def make_button_item(action, image_name):
    return ui.ButtonItem(action=action, image=ui.Image.named(image_name))

class Webbrowser(ui.View):
    def __init__(self):
        back     = make_button_item(self.bt_back,     'ionicons-arrow-left-b-32')
        forward  = make_button_item(self.bt_forward,  'ionicons-arrow-right-b-32')
        home     = make_button_item(self.bt_home,     'ionicons-home-32')
        favorite = make_button_item(self.bt_favorite, 'ionicons-bookmark-32')
        self.url = ''
        self.new_url = ''
        self.left_button_items = [back, forward]
        self.right_button_items = [home, favorite]
        self.name = 'Webbrowser'
        self.present()

    def did_load(self):
        self['textfield1'].clear_button_mode = 'while_editing'
        self['textfield1'].delegate = self['webview1'].delegate = self
        self.bt_home(None)

    def load_url(self):
        self['webview1'].load_url(self.url)

    def bt_back(self, sender):
        self['textfield1'].text = ''
        self['webview1'].go_back()

    def bt_forward(self, sender):
        self['textfield1'].text = ''
        self['webview1'].go_forward()

    def bt_home(self, sender):
        self.url = 'http://www.google.com'
        self.load_url()

    def bt_favorite(self, sender):
        self['textfield1'].text = 'Favorites'
        self['webview1'].load_html(favorites_html)

    def textfield_did_begin_editing(self, textfield):
        self['webview1'].stop()

    def textfield_did_end_editing(self, textfield):
        url = self['textfield1'].text
        pos = url.find('://') # ftp://, http://, https:// >> 3-5
        if pos > 2 and pos < 6:
            self.url = url
        else:
            self.url = 'http://' + url
        self.load_url()

    def webview_did_start_load(self, webview):
        self['textfield1'].text_color = 'orange'

    def webview_did_finish_load(self, webview):
        self.new_url = self['webview1'].evaluate_javascript('window.location.href')
        if self.url != self.new_url:
            self['textfield1'].text = self.new_url
            self.url = self.new_url
        self['textfield1'].text_color = 'black'

    def webview_did_fail_load(self, webview, error_code, error_msg):
        if error_code < -999:
            error_html = "<HTML><HEAD></HEAD><BODY><span style='color:#FF0000'><H1><P>error_code: " + str(error_code) + ", " + error_msg + " <br></P></H1></BODY></HTML>"
            self['webview1'].load_html(error_html)
        #error_code: -1009, The Internet connection appears to be offline.
        #error_code: -1003, A server with the specified hostname could not be found. 

ui.load_view('Webbrowser')  # Custom View Class in the .pyui file must be set to Webbrowser
