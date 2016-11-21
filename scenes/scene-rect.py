# https://forum.omz-software.com/topic/3268/pythonista-3-rect-attributes/2

import scene, ui
print(scene.Rect() == ui.Rect())  # True
print(scene.Rect == ui.Rect)      # True
print(scene.Rect is ui.Rect)      # True

