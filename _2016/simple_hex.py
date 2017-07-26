# https://gist.github.com/zacbir/e50d14bf9559e7e03feb2f0e80adb834

from geometer import *

c = CoreGraphicsCanvas('test', 500, 500)

background, stroke = base03, base1

c.set_stroke_color(stroke)
c.set_fill_color(background)

c.fill_background()

s = HorizontalHexagon(c.center(), 120)

s.draw(c)

c.save()
