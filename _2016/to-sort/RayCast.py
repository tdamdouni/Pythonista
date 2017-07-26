# RayCast
# Simple raycasting based renderer
# Touch the left part to rotate, and touch the right part to move forward
# Coded in a few hours during my holidays, July 2014, straight from my iPhone - thanks Pythonista !!!
# Feel free to upgrade !
# Enjoy !
# Emmanuel ICART
# eicart@momorprods.com

from scene import *
from math import *

# rendering step - 1=best(slower)
RENDERING_STEP=2

# level data
# 1 = wall, 0 = empty
level = [[1,1,1,1,1,1,1,1],
         [1,1,0,0,0,0,0,1],
         [1,0,0,0,0,1,0,1],
         [1,0,1,0,0,0,0,1],
         [1,1,0,0,0,1,0,1],
         [1,0,0,1,1,0,0,1],
         [1,0,0,0,0,0,0,1],
         [1,1,1,1,1,1,1,1]]         
LX=len(level[0])
LZ=len(level)

CellSize=128
scan=10


# player
xo=CellSize*LX/2
zo=CellSize*LZ/2
angle=45.0
fov=80

class RayCastScene (Scene):
	def setup(self):
		# preload the texture
		self.texture='PC_Chest_Closed'
		self.screenWidth=int(self.size.w)
		self.screenHeight=int(self.size.h)
		self.xTouchStart=0
		self.yTouchStart=0
		load_image(self.texture)
		pass
	
	def draw(self):
		global angle
		global xo
		global zo
		# This will be called for every frame (typically 60 times per second).
		
		# clear background 
		background(0, 0, 0)

		focale=0.5*self.screenWidth/tan(radians(fov/2))
		
		# compute each screen column
		for column in xrange(0,self.screenWidth,RENDERING_STEP):
			scan_angle=angle+((float(column)-self.screenWidth/2)*fov)/self.screenWidth
			c=cos(radians(scan_angle))
			s=sin(radians(scan_angle))
			if abs(c)<0.001:
				if c>0:
					c=0.001
				else:
					c=-0.001
				
			if abs(s)<0.001:
				if s>0:
					s=0.001
				else:
					s=-0.001
				
			t2=s/c
			t1=c/s
			ok1=True
			ok2=True
				
			#Initialization of ray casting
			pz1=t2*CellSize
			if c>0:
				px1=CellSize
				ini=0
			else:
				px1=-CellSize
				pz1=-pz1
				ini=CellSize-1
				
			xp1=ini+(((int)(xo/CellSize))*CellSize)
			zp1=zo+((xp1-xo)*pz1)/px1
				
			px2=t1*CellSize
			if s>0:
				pz2=CellSize
				ini=0
			else:
				pz2=-CellSize
				px2=-px2
				ini=CellSize-1
				
			zp2=ini+(((int)(zo/CellSize))*CellSize)
			xp2=xo+((zp2-zo)*px2)/pz2
			
			#****** cast a ray for z walls ******
			compteur=0
			while True:
				xp1+=px1
				zp1+=pz1
				compteur+=1
				xd=(int)(xp1/CellSize) % LX
				zd=(int)(zp1/CellSize) % LZ
				if (xd<0): xd=0
				if (zd<0): zd=0
				
				if level[xd][zd]!=0 or compteur>=scan: break
			
			if (compteur==scan):ok1=False
			distance1=(xp1-xo)/c
			col1=(zp1 % CellSize)
			if (px1<=0): col1=CellSize-1-col1
			
			#****** cast a ray for x walls ****** 
			compteur=0
			while True:
				xp2+=px2
				zp2+=pz2
				compteur+=1
				xd=(int)(xp2/CellSize) % LX
				zd=(int)(zp2/CellSize) % LZ
				if (xd<0):xd=0
				if (zd<0):zd=0
				if level[xd][zd]!=0 or compteur>=scan: break
			
			if (compteur==scan): ok2=False
			distance2=(zp2-zo)/s
			col2=(xp2 % CellSize)
			if (pz2>=0):col2=CellSize-1-col2
			
			#Choose the nearest wall (x or z)
			if (distance1<distance2):
				distance=1+(distance1)
				colonne=col1
			else:
				distance=1+(distance2)
				colonne=col2
			
			if ok1 or ok2:
				# fix the fishbowl effect
				distance=distance*cos(radians(angle-scan_angle))
				
				#compute the wall screen height
				hauteur = ((CellSize*focale)/distance)

			# draw the column
			ximage=(colonne*128)/CellSize # 101 x 171 tile
			image(self.texture,column,(self.screenHeight-hauteur)/2,RENDERING_STEP,hauteur,ximage,0,RENDERING_STEP,171)
		
		
		# display fingers
		fill(1, 0, 0)
		for touch in self.touches.values():
			ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)
	
			# rotation control
			if (touch.location.x<self.screenWidth/2):
				angle += 0.04*(touch.location.x-self.xTouchStart)
			else:
			# displacement control
				speed=(touch.location.y-self.yTouchStart)*0.2
				dx=speed*cos(radians(angle))
				dz=speed*sin(radians(angle))
				if level[int((xo+dx)/CellSize)][int(zo/CellSize)]!=0:dx=0
				if level[int(xo/CellSize)][int((zo+dz)/CellSize)]!=0:dz=0
				xo+=dx
				zo+=dz
	
	def touch_began(self, touch):
		global angle
		self.angleStart=angle
		if touch.location.x<self.screenWidth/2:self.xTouchStart=touch.location.x
		else:
			self.yTouchStart=touch.location.y
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

run(RayCastScene(),LANDSCAPE)
