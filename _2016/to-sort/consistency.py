# coding: utf-8

# https://forum.omz-software.com/topic/2919/making-arcs-and-filling-them-with-in-ui-path

# @omz The default ui.View doesn't seem to have a draw method. I assume this is special-cased internally to not cause errors, but it would be nice to have a default draw method (even if empty) so we can always use super in the draw method.

# For example, this code currently fails, because ui.View doesn't have a draw method:

import ui

class CustomView(ui.View):
    def draw(self):
        super().draw()
        ui.Path.rect(5, 5, 45, 45).fill()

# But if we'd write a subclass of CustomView, we would need to call super().draw(), otherwise the custom drawing code in CustomView.draw wouldn't be executed.

# This isn't a big issue - currently you just have to leave out the super call when the base class is ui.View - but I am a fan of consistency. :)
