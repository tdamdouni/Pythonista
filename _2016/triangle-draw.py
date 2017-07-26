# https://forum.omz-software.com/topic/3767/unwanted-black-lines-scene_drawing
	
	def draw(self):
		background(.3, .66, .9)
		stroke_weight(0)
		density = 50
		for i in range(density):
			fill(i/float(density), 0, 1)
			start = i/float(density)
			end = (i+.8)/float(density)
			smaller = min(self.terrain_func(start), self.terrain_func(end))
			rect(start*self.bounds.w, 0, (end-start)*game.bounds.w, smaller*self.bounds.h)
			if self.terrain_func(start) < self.terrain_func(end):
				v = [(start*self.bounds.w, self.terrain_func(start)*self.bounds.h), (end*self.bounds.w, self.bounds.h*self.terrain_func(start)), (end*self.bounds.w, self.bounds.h*self.terrain_func(end))]
			else:
				v = [(start*self.bounds.w, self.terrain_func(end)*self.bounds.h), (end*self.bounds.w, self.bounds.h*self.terrain_func(end)), (start*self.bounds.w, self.bounds.h*self.terrain_func(start))]
			triangle_strip(v)

