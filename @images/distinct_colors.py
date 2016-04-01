# https://gist.github.com/upwart/ede14e200fbeeb331786
# module distinct_colors
# vs 1.0.0
# based on: www.8bittobot.com/2011/09/16/n-distinct-colors/

# vs 1.0.1
# improved the algorithm by applying the minimum number of segements and then increasing the
# number of segments if needed (only when colors are to be excluded)
# improved stability

import itertools

def distinct_colors(number,excludecolors=[]):
	'''returns a list of distinct color tuples
	
	arguments:
	number -- number of colors required
	excludecolors -- list of color tuples to be excluded
	'''

	def MidSort(lst):
		if len(lst) <= 1:
			return lst
		i = int(len(lst)/2)
		ret = [lst.pop(i)]
		left = MidSort(lst[0:i])
		right = MidSort(lst[i:])
		interleaved = [item for items in itertools.izip_longest(left, right)
		for item in items if item != None]
		ret.extend(interleaved)
 	 	return ret

	if number<=0:
		return([])

	max = 1.
	if number==1:
		segs=1
	else:
		segs=int((number-0.001)**(1.0/3.0))
		
	while True:
		step = max/segs
		p=[]
		for i in range(1,segs):
			p.append(i*step)

		points = [0,max]
		points.extend(MidSort(p))

		colors = []
		total = 0
		
		for endrange in range (1,len(points)+1):
			for c0 in range(endrange):
				for c1 in range(endrange):
					for c2 in range(endrange):
						c=(points[c0], points[c1], points[c2])
						if c not in colors:
							if c not in excludecolors:
								colors.append(c)
								total += 1
								if total==number:
									return colors
				
		segs=segs+1


def main():
	
	import canvas
	canvas.set_size(1000,1000)
	x=0
	y=0
	colors=distinct_colors(1,[(0,0,0),(1,1,1)])
	for c in colors:
		canvas.set_fill_color(*c)
		canvas.fill_rect(x,y,50,50)
		x=x+60
		if x>900:
			x=0
			y=y+60	

if 	__name__ == "__main__":
	main()

# cclauss commented on Jul 13, 2014
# Suggestions:

#if number==1:
#   segs=1
#else:
#   segs=int((number-0.001)**(1.0/3.0))
#segs = 1 if number == 1 else int((number-0.001)**(1.0/3.0))
#p=[]
#for i in range(1,segs):
#   p.append(i*step)
#p = [i * step for i in range(1, segs)]
#if c not in colors:
#   if c not in excludecolors:
#if (c not in colors
#and c not in excludecolors):
#x=0
#y=0
#x = y = 0
#colors=distinct_colors(1,[(0,0,0),(1,1,1)])
#colors=distinct_colors(256,[(0,0,0),(1,1,1)])
#And in various places:

#segs=segs+1
#segs += 1

#x=x+60
#x += 60

#y=y+60
#y += 60