# https://github.com/cclauss/Pythonista_scene/blob/master/remote_control_scene.py

#remote_control_scene.py -- A bottle hack...
# Combine a bottle server with a Pythonista scene.Scene to remotely control the scene

import bottle, contextlib, random, scene, socket, sys, threading

def get_local_ip_addr():
    with contextlib.closing(socket.socket(socket.AF_INET,
                                          socket.SOCK_DGRAM)) as s:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]

def random_color():
    return scene.Color(random.random(), random.random(), random.random())

local_ip_addr = get_local_ip_addr()
bg_color = random_color()

fmt = '''The current colors are:
    r={}
    g={}
    b={}'''
ip_fmt = '''To change them
    from a separate computer,
        open a web browser to:
            http://{}'''

def inverse_color(in_color):
    return scene.Color(1 - in_color.r, 1 - in_color.g, 1 - in_color.b)

def bottle_server():  # run a web server until interrupted
    bottle.run(host=local_ip_addr, port=80) # , debug=True, quiet=True)

class MyScene(scene.Scene):
    def __init__(self):  # This scene runs itself
        scene.run(self)  #, frame_interval=15)  # Lower the FPS
        
    def setup(self):
        self.x, self.y = self.bounds.center()
        threading.Thread(None, bottle_server).start()

    def draw(self):
        scene.background(bg_color.r, bg_color.g, bg_color.b)
        fg_color = inverse_color(bg_color)
        scene.tint(*fg_color) # .r, fg_color.g, fg_color.b)
        the_text = fmt.format(*bg_color)
        if local_ip_addr:  # if remote user has not yet connected
            the_text += '\n\n' + ip_fmt.format(local_ip_addr)
        scene.text(the_text, font_size=40, x=self.x, y=self.y)

def html_data_entry(*in_field_names):
    fmt = '<input type="number" name="{}" value="{}">'
    return { k : fmt.format(k, random.random()) for k in in_field_names }

@bottle.get('/')
def bottle_get_index():
    global local_ip_addr
    local_ip_addr = None  # Supress the connect message once the remote user connects.
    the_html = '''
<div style="text-align:center;">
    <h1>Remote control of the colors of a Pythonista scene</h1>
    <h3>Please enter values between 0.0 and 1.0 and then tap the "Submit" button.</h3>
    <form action="/" method="post">
        Red:   {R} &nbsp; &nbsp;
        Green: {G} &nbsp; &nbsp;
        Blue:  {B}
        <p>
        <input value="Submit" type="submit" />
    </form>
</div>'''.format(**html_data_entry('R', 'G', 'B'))
    #print(the_html)
    return the_html

@bottle.post('/')
def bottle_post_index():
    global bg_color
    bg_color = scene.Color(float(bottle.request.forms['R']),
                           float(bottle.request.forms['G']),
                           float(bottle.request.forms['B']))
    bottle.redirect('/')  # reload the bottle_get_index page

def main(argv):
    MyScene()
 
if __name__ == '__main__':
    sys.exit(main(sys.argv))
