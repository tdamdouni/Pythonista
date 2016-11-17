# https://forum.omz-software.com/topic/1961/putting-a-matplotlib-plot-image-into-a-ui-imageview

import matplotlib.pyplot as plt
from io import BytesIO
import ui 

plt.plot([1, 2, 3])

b = BytesIO()
plt.savefig(b)
img = ui.Image.from_data(b.getvalue())

img_view = ui.ImageView(background_color='white')
img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
img_view.image = img
img_view.present()
# --------------------
# coding: utf-8
import matplotlib.pyplot as plt
import io, math, ui

# plt must be matplotlib.pyplot or its alias
def plot_to_scrollable_image_view(plt):
    img_view = ui.ImageView()
    b = io.BytesIO()
    plt.savefig(b)
    img_view.image = ui.Image.from_data(b.getvalue())
    view = ui.ScrollView()
    view.add_subview(img_view)
    return view

plt.plot([math.sin(x/10.0) for x in xrange(95)])
plt.xlim(0, 94.2)
view = plot_to_scrollable_image_view(plt)
view.present()
img_view = view.subviews[0]
img_view.frame = view.bounds
img_view.width *= 2
img_view.height *= 2
view.content_size = img_view.width, img_view.height
# --------------------

# coding: utf-8
import matplotlib.pyplot as plt
import io, math, ui


def plot_to_scrollable_image_view(plt):
    img_view = ui.ImageView()
    b = io.BytesIO()
    plt.savefig(b,format='png',dpi=160)
    img_view.image = ui.Image.from_data(b.getvalue())
    view = ui.ScrollView()
    view.add_subview(img_view)
    view.dx=0
    view.ready=True
    view.bounces=False
    return view
class delegate(object):
   #@ui.in_background  #ui.delay called from backgrounded was unreliable.
   def scrollview_did_scroll(self,sender):
      ui.cancel_delays()
      d = sender.content_offset[0]-5.0
      sender.content_offset=(5,5)
      sender.dx=d+sender.dx
      def hq():
        sender.ready=False
        dx=sender.dx
        sender.dx=0
        xl=plt.xlim()
        xl=[x+dx for x in xl]
        plt.xlim(xl)
        b = io.BytesIO()
        plt.savefig(b,format='jpeg',dpi=160)
        sender.subviews[0].image = ui.Image.from_data(b.getvalue())
        sender.ready=True
      if sender.ready:
        sender.ready=False
        dx=sender.dx
        sender.dx=0
        xl=plt.xlim()
        xl=[x+dx for x in xl]
        plt.xlim(xl)
        b = io.BytesIO()
        plt.savefig(b,format='jpeg',dpi=16)
        sender.subviews[0].image = ui.Image.from_data(b.getvalue())
        sender.ready=True
      ui.delay(hq,0.2)

        
plt.plot([math.sin(x/10.0) for x in xrange(95)])
plt.xlim(0, 94.2)
view = plot_to_scrollable_image_view(plt)
view.present()
view.subviews[0].frame = view.bounds
view.subviews[0].x,view.subviews[0].y=(5,5)
view.content_size=tuple(view.subviews[0].bounds.size+(11,11))
view.content_offset=(5,5)
view.delegate=delegate()
# --------------------

# coding: utf-8
import matplotlib.pyplot as plt
import io, math, ui

def plot_to_scrollable_image_view(plt):
    img_view = ui.ImageView()
    b = io.BytesIO()
    plt.savefig(b, format='png', dpi=160)
    img_view.image = ui.Image.from_data(b.getvalue())
    view = ui.ScrollView()
    view.add_subview(img_view)
    view.delegate = delegate()
    view.dx = 0
    view.ready = True;
    view.bounces = False
    return view

class delegate(object):
   #@ui.in_background  #ui.delay called from backgrounded was unreliable.
   def scrollview_did_scroll(self,sender):
      ui.cancel_delays()
      sender.dx += sender.content_offset[0] - 5.0
      sender.content_offset = (5, 5)
      def hq(dpi=160):
        sender.ready=False
        dx, sender.dx = sender.dx, 0
        plt.xlim([x + dx for x in plt.xlim()])
        b = io.BytesIO()
        plt.savefig(b, format='jpeg', dpi=dpi)
        sender.subviews[0].image = ui.Image.from_data(b.getvalue())
        sender.ready = True
      if sender.ready:
        hq(16)
      ui.delay(hq, 0)

plt.plot([math.sin(x/10.0) for x in xrange(950)])
plt.xlim(0, 95)  # approx 1 cycle of the sin wave
plt.subplots_adjust(left=0.06, bottom=0.05, right=0.98, top=0.97)
view = plot_to_scrollable_image_view(plt)
view.hidden = True  # wait until view is setup before displaying
view.present()
img_view = view.subviews[0]
img_view.frame = view.bounds
img_view.x, img_view.y = view.content_offset = (5, 5)
view.content_size = tuple(img_view.bounds.size + (11, 11))
view.hidden = False
# --------------------

# coding: utf-8
import matplotlib.pyplot as plt
import io, math, ui

def plot_to_scrollable_image_view(plt):
    img_view = ui.ImageView()
    b = io.BytesIO()
    plt.savefig(b, format='png', dpi=160)
    img_view.image = ui.Image.from_data(b.getvalue())
    view = ui.ScrollView()
    view.add_subview(img_view)
    view.delegate = delegate()
    view.dx = 0
    view.ready = True;
    view.bounces = False
    return view

class delegate(object):
   #@ui.in_background  #ui.delay called from backgrounded was unreliable.
   def scrollview_did_scroll(self,sender):
      ui.cancel_delays()
      sender.dx += sender.content_offset[0] - 5.0
      sender.content_offset = (5, 5)
      def hq(dpi=160):
        sender.ready=False
        dx, sender.dx = sender.dx, 0
        plt.xlim([x + dx for x in plt.xlim()])
        b = io.BytesIO()
        plt.savefig(b, format='jpeg', dpi=dpi)
        sender.subviews[0].image = ui.Image.from_data(b.getvalue())
        sender.ready = True
      if sender.ready:
        hq(16)
      ui.delay(hq, 0)

plt.plot([math.sin(x/10.0) for x in xrange(950)])
plt.xlim(0, 95)  # approx 1 cycle of the sin wave
plt.subplots_adjust(left=0.06, bottom=0.05, right=0.98, top=0.97)
view = plot_to_scrollable_image_view(plt)
view.hidden = True  # wait until view is setup before displaying
view.present()
img_view = view.subviews[0]
img_view.frame = view.bounds
img_view.x, img_view.y = view.content_offset = (5, 5)
view.content_size = tuple(img_view.bounds.size + (11, 11))
view.hidden = False
# --------------------
