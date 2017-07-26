	def hide_close(self, state=True):
		from objc_util import ObjCInstance
		v = ObjCInstance(self.view)
		for x in v.subviews():
			#if 'UIButton' in x.description():
			if str(x.description()).find('UIButton') >= 0:
				x.setHidden(state)

