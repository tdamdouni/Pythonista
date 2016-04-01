import sys
import getpass

# console.login_alert('enter credentials for ' + urlparse.urlparse(result.url).netloc)
# console.login_alert(title[, message, login, password, ok_button_title])
def login_alert(title, message = None, login = None, password = None, ok_button_title = None):
    print title
    user = raw_input('Username ({0}):'.format(login))
    if login and not user:
        user = login

    if not user:
        return (None, None)

    pw = getpass.getpass('Password for {0}: '.format(user))
    return (user, pw)

def clear():
    raise NotImplementedError()

def set_font(name = None, size = None):
    raise NotImplementedError()

def set_color(r, g, b):
    raise NotImplementedError()

def secure_input(prompt = None):
    raise NotImplementedError()

def show_image(image_path):
    raise NotImplementedError()

def alert(title, message = None, button1 = None, button2 = None, button3 = None, hide_cancel_button = False):
    raise NotImplementedError()

def input_alert(title, message = None, input = None, ok_button_title = None, hide_cancel_button=False):
    raise NotImplementedError()

def password_alert(title, message = None, password = None, ok_button_title = None, hide_cancel_button=False):
    raise NotImplementedError()

def show_activity():
    raise NotImplementedError()

def hide_activity():
    raise NotImplementedError()

def hud_alert(message, icon = None, duration = None):
    raise NotImplementedError()

def write_link(title, link_url):
    raise NotImplementedError()

def hide_output():
    raise NotImplementedError()

def quicklook(file_path):
    raise NotImplementedError()

def open_in(file_path):
    raise NotImplementedError()

def set_idle_timer_disabled(flag):
    raise NotImplementedError()
