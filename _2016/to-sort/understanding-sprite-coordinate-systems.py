# https://forum.omz-software.com/topic/3184/understanding-sprite-coordinate-systems

def drawSeg(self, touchPosition):
	segPath = ui.Path()
	segPath.move_to(0, 0)
	dx = randint(-100, 100)
	dy = randint(-100, 100)
	segPath.line_to(dx, dy)
	seg = ShapeNode(path = segPath, position = touchPosition)
	seg.stroke_color = (255,255,255)
	seg.fill_color = "clear"
	if dx >= 0:
		if dy >= 0:
			seg.anchor_point = (0, 1)
		else:
			seg.anchor_point = (0, 0)
	else:
		if dy >= 0:
			seg.anchor_point = (1, 1)
		else:
			seg.anchor_point = (1, 0)
			
	self.add_child(seg)
	
# --------------------

segPath.line_to(dx,-dy)
seg=ShapeNode(path=segPath, position=touchPosition)
seg.anchor_point=((dx<=0),(dy<=0))

