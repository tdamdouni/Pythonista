# https://gist.github.com/anonymous/cbc554a5aab2350b847d

# Motion control demo
from scene import *

def hitTest(x1,y1,size1,x2,y2,size2,output=0):
	if x1+size1>=x2 and x1<=x2+size2:
				if y1+size1>=y2 and y1<=y2+size2:
					output=1
	if output:
		#Calculate origins
		ox1=x1+(size1/2)
		oy1=y1+(size1/2)
		ox2=x2+size2/2
		oy2=y2+size2/2
		#Difference between origins to locate the direction
		difx=ox1-ox2
		dify=oy1-oy2
		if difx<=0: output1=1#hit from r
		else: output1=2#hit from l
		if dify<=0: output2=1#hit from t
		else: output2=2#hit from b
		#check which is most important
		if dify<0:dify*=-1
		if difx<0:difx*=-1
		if difx>dify: output=output1
		else: output=output2+2
	return output


class MyScene (Scene):
	def setup(self):
		self.x = 0
		self.y = 0
		self.smallx=self.size.w * 0.5
		self.smally=self.size.h * 0.5
	def draw(self):
		background(0, 0, 0)
		fill(1, 0, 0)
		g = gravity()
		textOut='x='+str(round(g.x,1))+' y='+str(round(g.y,1))+' z='+str(round(g.z,1))
		text(textOut,'Futura',40,*self.bounds.center().as_tuple())
		size=((g.z*-1)+2)*10
		self.x += g.x * 10
		self.y += g.y * 10
		self.x = min(self.size.w - size, max(0, self.x))
		self.y = min(self.size.h - size, max(0, self.y))
		rect(self.x, self.y, size, size)
		#self.smallx+=g.x*25
		#self.smally+=g.y*25
		self.smallx = min(self.size.w - size/2, max(0, self.smallx))
		self.smally = min(self.size.h - size/2, max(0, self.smally))
		#if self.smallx+size/2>=self.x and self.smallx<=self.x+size:
		#		if self.smally+size/2>=self.y and self.smally<=self.y+size:
		#			fill(0,1,1)
		test=hitTest(self.smallx,self.smally,size/2,self.x,self.y,size)
		if test:
			textOut=''
			if test==1: 
				textOut='Hit from R'
				self.smallx-=10
			elif test==2: 
				textOut='Hit from L'
				self.smallx+=10
			elif test==3: 
				textOut='Hit from T'
				self.smally-=10
			else: 
				textOut='Hit from B'
				self.smally+=10
			text(textOut,'Futura',40,100,40)
			fill(0,1,1)
		rect(self.smallx, self.smally, size/2, size/2)
run(MyScene())
