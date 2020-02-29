# -*- coding: utf-8 -*-

# https://gist.github.com/anonymous/70b4a6bb0d2a818cb2ce

from __future__ import print_function
from scene import *
from PIL import Image
import urllib, os
from random import randint, choice
from math import radians, sin, cos

ssize = Size(96, 128)
speed = 0.15
speedMonsters = .15
boost = 3
frames = [0, 1, 2, 1] #4 frames per walk cycle
dirs = [0, 3, 9, 6]	#start frame for direction
moveamt = 32 #Size of the sprites
mov = [(0, -moveamt), (-moveamt, 0), (0, moveamt), (moveamt, 0)]

north = 0
south = 2
east = 1
west = 3
hitRange=10

#Constants.
GOAL=0
KAKUNA=1 #Includes KAKUNA and BEEDRILL
KINGDRA=2
ZUBAT=3
EKANS=4
ESPEON=5
CHAR=6 #Includes CHARMANDER, CHARMELEON and CHARIZARD
NINJ=7 #Includes NINCANDA, NINJASK and SHEDINJA
SAND=8 #Includes SANDSHREW and SANDSLASH
ENTEI=9
KENGIS=10 #Includes KENGIS, KENGIS BABY and CUBONE
MAGNET=11 #Includes MAGNETITE and MAGNETON
GOLEM=12

#For talking with the GUI.
def stringType(m):
	if m.type==KAKUNA:
		if m.evo==0: s="Kakuna"
		else: s="Beedrill"
	elif m.type==KINGDRA: s="Kingdra"
	elif m.type==ZUBAT: s="Zubat"
	elif m.type==EKANS: s="Ekans"
	elif m.type==ESPEON: s="Espeon"
	elif m.type==CHAR:
		if m.evo==0: s="Charmander"
		elif m.evo==1: s="Charmeleon"
		else: s="Charizard"
	elif m.type==NINJ:
		if m.evo==0: s="Nincanda"
		elif m.evo==1: s="Ninjask"
		else: s="Shedinja"
	elif m.type==SAND:
		if m.evo==0: s="Sandshrew"
		else: s="Sandslash"
	elif m.type==ENTEI: s="Entei"
	elif m.type==KENGIS:
		if m.evo==0: s="Kengiskan"
		elif m.evo==1: s="Kengiskan baby"
		else: s="Cubone"
	elif m.type==MAGNET:
		if m.evo==0: s="Magnetite"
		else: s="Magneton"
	elif m.type==GOLEM: s="Golem"
	else: s="Unknown"
	return s

class collision (object):
	def __init__(self, location, size, type):
		self.location=location
		self.size=size
		self.type=type
		
class monster (object):
	def __init__(self, location, size, type):
		self.location=location
		self.size=size
		self.type=type
		self.dir=0 		#Direction
		self.start=0  #Frame start
		self.evo=0	  #Evolution
		self.special=0#Used for fireballs, special powers, etc
		self.delay=speedMonsters
		self.movlen=0 #used as a counter before the monster changes direction
		
#The following array contains all data for walls and pushable objects, sorted by level
#wall format: [[xy location], [xy size], type]
#types: 0=safe spawn site, 1=mons spawn site, 2=wall, 3=pushable        
levels=[[[[0,0],    [306,256],2], [[459,0],  [306,384],2], [[153,384],[153,256],2],
         [[459,512],[306,256],2], [[306,256],[153,256], 3]],
        [[[0, 0],   [256,256],2], [[0,384],  [256,128],2], [[0,640],  [256,128],2],
         [[512,0],  [256,128],2], [[512,256],[256,128],2], [[512,512],[256,128],2],
				 [[256,108],[256,640],3]],
				[[[0,256],  [768,32], 0], [[0,512],  [768,32], 0], [[240,0],  [32,768], 0],
         [[496,0],  [32,768], 0], [[240,0],  [32,710], 2], [[48,256], [311,32], 2], 
         [[48,512], [682,32], 2], [[496,48], [32,662], 2], [[407,256],[323,32], 2]],
        [[[0,0],    [48,768],2],  [[0,0],    [336,144],2], [[432,0],  [336,144],2],
         [[720,144],[48,768], 2], [[192,288],[384,288], 2],[[0,720],  [768,48], 2],
         [[96,192], [576,48], 0], [[96,192], [48,480], 0], [[96,624], [576,48], 0],
         [[624,192],[48,480], 0]],
        [[[192,192],[480,96], 2], [[192,192],[96,480], 2], [[480,96], [96,288], 2],
         [[96, 480],[288,96], 2], [[480,480],[288,288],2]],
        [[[240,96],[48,192],  0], [[96,240], [144,48], 0], [[528,96], [96,48],  0],
         [[480,96], [48,192], 0], [[624,96], [48,192], 0], [[528,240],[96,48],  0],
         [[144,480],[96,48],  0], [[528,480],[96,48],  0], [[144,624],[96,48],  0],
         [[528,624],[96,48],  0], [[96,480], [48,192], 0], [[480,480],[48,192], 0],
         [[240,480],[48,192],  0], [[624,480],[48,192], 0]]]
mvm=moveamt/2
monsSpawn=[Point(688,448),Point(50,550),Point(384,384),Point(384,432),Point(336,336),
           Point(192,192)]
selfSpawn=[Point(382.5,32),Point(384,64),Point(128,128),Point(384,48),Point(48,48),
           Point(384,384)]
for level in range(len(levels)): #Turns all items into collision objects
	for i in range(len(levels[level])):
		levels[level][i]=collision(Point(levels[level][i][0][0],levels[level][i][0][1]),
		                           Point(levels[level][i][1][0],levels[level][i][1][1]),
		                           levels[level][i][2])
	#This gives level boundries, and the safe spawn sites for player and monsters.
	selfSpawn[level].x-=mvm; selfSpawn[level].y-=mvm
	monsSpawn[level].x-=mvm; monsSpawn[level].y-=mvm
	tempSpawn=Point(selfSpawn[level].x-25,selfSpawn[level].y-25)
	levels[level].append(collision(tempSpawn,Point(moveamt+50,moveamt+50),0))
	levels[level].append(collision(monsSpawn[level],Point(32,32),1))
	levels[level].append(collision(Point(-80,0),Point(100,1024),2)) #Left
	levels[level].append(collision(Point(0,-80),Point(768,100),2))  #Bottom
	levels[level].append(collision(Point(758,0),Point(100,1024),2)) #Right
	levels[level].append(collision(Point(0,738),Point(768,100),2))  #Top

#like before, it's xy loc, xy size, then type
#Need at least three of type 0 (GOAL) to complete lvl
levelsMonsters=[[monster(Point(688,448),Point(32,32),1),
                 monster(Point(688,448),Point(32,32),2),
                 monster(Point(688,448),Point(32,32),3),
                 monster(Point(688,448),Point(32,32),4),
                 monster(Point(688,448),Point(32,32),5),
                 monster(Point(688,448),Point(32,32),6),
                 monster(Point(688,448),Point(32,32),7),
                 monster(Point(688,448),Point(32,32),8),
                 monster(Point(688,448),Point(32,32),9),
                 monster(Point(688,448),Point(32,32),10),
                 monster(Point(688,448),Point(32,32),11),
                 monster(Point(688,448),Point(32,32),12),
                 monster(Point(366,526),Point(32,32),GOAL),
                 monster(Point(366,526),Point(32,32),GOAL),
                 monster(Point(366,526),Point(32,32),GOAL)],
                
                [monster(Point(128,560),Point(32,32),GOAL),
                 monster(Point(128,304),Point(32,32),GOAL),
                 monster(Point(612,672),Point(32,32),GOAL),
                 monster(Point(640,176),Point(32,32),GOLEM),
                 monster(Point(640,176),Point(32,32),GOLEM),
                 monster(Point(640,176),Point(32,32),GOLEM),
                 monster(Point(640,176),Point(32,32),GOLEM),
                 monster(Point(128,368),Point(32,32),KENGIS),
                 monster(Point(640,432),Point(32,32),KENGIS),
                 monster(Point(128,624),Point(32,32),KENGIS)],
                
                [monster(Point(128,384),Point(32,32),GOAL),
                 monster(Point(368,300),Point(32,32),GOAL),
                 monster(Point(608,384),Point(32,32),GOAL),
                 monster(Point(128,384),Point(32,32),KAKUNA),
                 monster(Point(128,384),Point(32,32),KAKUNA),
                 monster(Point(128,384),Point(32,32),KAKUNA),
                 monster(Point(128,640),Point(32,32),MAGNET),
                 monster(Point(128,640),Point(32,32),MAGNET),
                 monster(Point(128,640),Point(32,32),MAGNET),
                 monster(Point(384,640),Point(32,32),KENGIS),
                 monster(Point(640,640),Point(32,32),SAND),
                 monster(Point(640,640),Point(32,32),SAND),
                 monster(Point(640,640),Point(32,32),SAND),
                 monster(Point(640,640),Point(32,32),SAND),
                 monster(Point(640,384),Point(32,32),NINJ),
                 monster(Point(640,384),Point(32,32),NINJ),
                 monster(Point(640,384),Point(32,32),NINJ),
                 monster(Point(640,384),Point(32,32),NINJ),
                 monster(Point(640,128),Point(32,32),CHAR),
                 monster(Point(640,128),Point(32,32),CHAR),
                 monster(Point(384,128),Point(32,32),ZUBAT),
                 monster(Point(384,128),Point(32,32),ZUBAT),
                 monster(Point(384,128),Point(32,32),ZUBAT)],
                
                [monster(Point(168,432),Point(32,32),NINJ),
                 monster(Point(168,432),Point(32,32),NINJ),
                 monster(Point(168,432),Point(32,32),NINJ),
                 monster(Point(168,432),Point(32,32),MAGNET),
                 monster(Point(168,432),Point(32,32),MAGNET),
                 monster(Point(168,432),Point(32,32),MAGNET),
                 monster(Point(600,432),Point(32,32),NINJ),
                 monster(Point(600,432),Point(32,32),NINJ),
                 monster(Point(600,432),Point(32,32),NINJ),
                 monster(Point(600,432),Point(32,32),MAGNET),
                 monster(Point(600,432),Point(32,32),MAGNET),
                 monster(Point(600,432),Point(32,32),MAGNET),
                 monster(Point(384,264),Point(32,32),NINJ),
                 monster(Point(384,264),Point(32,32),NINJ),
                 monster(Point(384,264),Point(32,32),NINJ),
                 monster(Point(384,264),Point(32,32),MAGNET),
                 monster(Point(384,264),Point(32,32),MAGNET),
                 monster(Point(56,416), Point(32,32),GOAL),
                 monster(Point(368,680),Point(32,32),GOAL),
                 monster(Point(680,416),Point(32,32),GOAL)],
                 
                 [monster(Point(128,128),Point(32,32),GOAL),
                  monster(Point(320,608),Point(32,32),GOAL),
                  monster(Point(608,320),Point(32,32),GOAL),
                  monster(Point(704,416),Point(32,32),KINGDRA),
                  monster(Point(704,416),Point(32,32),KENGIS),
                  monster(Point(704,416),Point(32,32),ZUBAT),
                  monster(Point(416,704),Point(32,32),KINGDRA),
                  monster(Point(416,704),Point(32,32),SAND),
                  monster(Point(416,704),Point(32,32),MAGNET)],
                  
                  [monster(Point(32,704), Point(32,32),GOAL),
                   monster(Point(704,704),Point(32,32),GOAL),
                   monster(Point(704,32), Point(32,32),GOAL),
                   monster(Point(560,176), Point(32,32),NINJ),
                   monster(Point(560,176), Point(32,32),NINJ),
                   monster(Point(560,176), Point(32,32),NINJ),
                   monster(Point(560,176), Point(32,32),MAGNET),
                   monster(Point(560,176), Point(32,32),MAGNET),
                   monster(Point(560,176), Point(32,32),MAGNET),
                   monster(Point(560,176), Point(32,32),MAGNET),
                   monster(Point(560,560), Point(32,32),MAGNET),
                   monster(Point(176,560), Point(32,32),NINJ),
                   monster(Point(176,560), Point(32,32),NINJ),
                   monster(Point(176,560), Point(32,32),NINJ),
                   monster(Point(176,560), Point(32,32),MAGNET),
                   monster(Point(176,560), Point(32,32),MAGNET),
                   monster(Point(176,560), Point(32,32),MAGNET),
                   monster(Point(176,560), Point(32,32),MAGNET),
                   monster(Point(176,560), Point(32,32),MAGNET),
                   monster(Point(560,560), Point(32,32),NINJ),
                   monster(Point(560,560), Point(32,32),MAGNET),
                   monster(Point(560,560), Point(32,32),MAGNET),
                   monster(Point(560,560), Point(32,32),MAGNET),
                   monster(Point(560,560), Point(32,32),MAGNET),
                   monster(Point(560,560), Point(32,32),MAGNET)]]

scoreButtons= [[Point(0,0),Point(30,30)],
               [Point(40,0),Point(30,30)],
               [Point(80,0),Point(30,30)],
               [Point(120,0),Point(30,30)]]
             
def talk(stringIn,s):
	del s[0]
	s.append(stringIn)
	return s

def score(self): #Draws the score for the level.  Also contains some tools for testing.
		strings=['Score: '+str(self.score)+' Lives: '+str(self.lives),
		         'Monsters: '+str(len(self.monsters)),
		         'Type: '+str(self.type)+' Evo: '+str(self.evo),
		         'Delay: '+str(round(self.dt,3)),
		         stringType(self),
		         'Level: '+str(self.level+1),
		         self.talkS[5],self.talkS[4],self.talkS[3],
		         self.talkS[2],self.talkS[1],self.talkS[0]]
		posX,posY=[],[]
		for i in range(len(strings)):
			posX.append(0)
			posY.append(0)
		fill(.15,0,.15) #Rectangle color
		if self.size.w>768: 	 #Alignment is to the right
			rect(768,0,256,1024) #Background rectangle. 'Working space' for scoreboard
			for i in range(len(scoreButtons)):
				fill(.15,0,.55)
				rect(scoreButtons[i][0].x+775,scoreButtons[i][0].y+650,
				     scoreButtons[i][1].x,scoreButtons[i][1].y)
			for i in range(len(posX)): posX[i]=775
			startY=10
			for i in range(len(posY)):
				if i==6: startY+=40
				elif i>6: startY+=18
				else: startY+=35        
				posY[i]=startY
		else: 								 #Alignment is to the top
			rect(0,768,1024,256) #Background rectangle. 'Working space'
			for i in range(len(scoreButtons)):
				fill(.15,0,.55)
				rect(scoreButtons[i][0].x+650,scoreButtons[i][0].y+775,
				     scoreButtons[i][1].x,scoreButtons[i][1].y)
			startX,startY=0,0
			for i in range(len(posY)):
				if i>=6: startY+=18
				else: startY+=35
				if startY>220: 
					startY=35
					startX+=400
				posX[i],posY[i]=35+startX,startY+768
		tint(0,1,1,1)
		for i in range(len(strings)): 
			if i>=6: text(strings[i], 'Futura', 13, posX[i], posY[i], 3)
			else: text(strings[i], 'Futura', 30, posX[i], posY[i], 3)
		tint(1,1,1,1)
		
#Reacts to a hit and returns a modified loc1 and loc2 for
#the two objects being tested
def hitReact(loc1,loc2,type,hit,speed,mons=False):
	#if type==0: 
		#loc1.y+=speed
		#loc1.y-=speed
	if type==0 and mons==True or type==1 and mons==False or type==2 or type==3 and mons==True:
		if hit==1: loc1.x-=speed#z.location.x+=10
		elif hit==2: loc1.x+=speed#z.location.x-=10
		elif hit==3: loc1.y-=speed#z.location.y+=10
		elif hit==4: loc1.y+=speed#z.location.y-=10
	elif type==3:
		if hit==1: loc2.x+=20
		elif hit==2: loc2.x-=20
		elif hit==3: loc2.y+=20
		elif hit==4: loc2.y-=20
	return [loc1,loc2]
	
def hitCorner(loc1,loc2,size2):
	if loc1.x>loc2.x and loc1.x<loc2.x+size2.x:
		if loc1.y>loc2.y and loc1.y<loc2.y+size2.y:
			return True
	
def hitTest2(loc1,size1,loc2,size2,output=0):
	if loc1.x+size1.x>=loc2.x and loc1.x<=loc2.x+size2.x:
				if loc1.y+size1.y>=loc2.y and loc1.y<=loc2.y+size2.y:
					output=1
	if output:
		#Rectangle alert
		if size1.x!=size1.y or size2.x!=size2.y:
			c1=hitCorner(loc1,loc2,size2)
			c2=hitCorner(Point(loc1.x,loc1.y+size1.y),loc2,size2)
			c3=hitCorner(Point(loc1.x+size1.x,loc1.y+size1.y),loc2,size2)
			c4=hitCorner(Point(loc1.x+size1.x,loc1.y),loc2,size2)
			if c1 and c2: return 2#l
			elif c2 and c3: return 3#t
			elif c3 and c4: return 1#r
			elif c4 and c1: return 4#b
		#Difference between origins to locate the direction
		difx=(loc1.x+size1.x/2)-(loc2.x+size2.x/2)
		dify=(loc1.y+size1.y/2)-(loc2.y+size2.y/2)
		if difx<=0: output1=1#hit from r
		else: output1=2#hit from l
		if dify<=0: output2=1#hit from t
		else: output2=2#hit from b
		if dify<0:dify*=-1#check which is most important
		if difx<0:difx*=-1
		if difx>dify: output=output1
		else: output=output2+2
	return output
	
#This function is used to rotate a sprite (magnetite) around player.
def findRotation(origin,loc,rotationAngle):
    angle=radians(rotationAngle)
    x2=origin.x+(cos(angle)*(loc.x-origin.x)-sin(angle)*(loc.y-origin.y))
    y2=origin.y+(sin(angle)*(loc.x-origin.x)+cos(angle)*(loc.y-origin.y))
    return Point(x2,y2)

#Used on Magnetite as a lightning bolt effect.
def lightning(loc1,loc2):
	stroke(1,1,1,0.3)
	stroke_weight(1)#randint(1,2))
	point1=Point(loc1.x,loc1.y)
	point4=Point(loc2.x,loc2.y)
	if loc1.x>loc2.x:
		temp=loc1.x
		loc1.x=loc2.x
		loc2.x=temp
	if loc1.y>loc2.y:
		temp=loc1.y
		loc1.y=loc2.y
		loc2.y=temp
	point2=Point(randint(loc1.x,loc2.x),randint(loc1.y,loc2.y))
	point3=Point(randint(loc1.x,loc2.x),randint(loc1.y,loc2.y))
	line(point1.x,point1.y,point2.x,point2.y)
	line(point2.x,point2.y,point3.x,point3.y)
	line(point3.x,point3.y,point4.x,point4.y)
	stroke(1,1,1,0)
	return
    
def dif(loc1,loc2):
 if loc1.x>loc2.x: difx=loc1.x-loc2.x
 else: difx=loc2.x-loc1.x
 if loc1.y>loc2.y: dify=loc1.y-loc2.y
 else: dify=loc2.y-loc1.y
 return difx+dify

def loadImage(folderPath,imgPath,urlPath):
	if not os.path.exists(folderPath): os.mkdir(folderPath)
	if not os.path.exists(folderPath+"/"+imgPath):		
		url = urllib.urlopen(urlPath)
		with open(folderPath+"/"+imgPath, "wb") as output:
			output.write(url.read())
	img = Image.open(folderPath+"/"+imgPath).convert('RGBA')
	return img
	
def replaceImage(folderPath,imgPath,urlPath):
	url = urllib.urlopen(urlPath)
	with open(folderPath+"/"+imgPath, "wb") as output:
		output.write(url.read())
	
def cropImage(img,start):
	strt = Point(start.x * ssize.w, start.y * ssize.h)
	img = img.crop((strt.x,strt.y,strt.x+ssize.w-1,strt.y+ssize.h-1))
	d = img.load()
	keycolor = d[0,0] #1st pixel is used as keycolor.
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			p = d[x, y]
			if p == keycolor: #if keycolor set alpha to 0.
				d[x, y] = (p[0], p[1], p[2], 0)
	return img
 
def wrap(v, size):
	if size.h>size.w: ext=size.w
	else: ext=size.h
	if v < 0: return ext + v
	elif v >= ext: return v - ext
	return v
	
def reverseDir(dir):
	if dir==0:   dir=2
	elif dir==1: dir=3
	elif dir==2: dir=0
	else:        dir=1
	return dir

#This function loads the images based on the player/monster's type.
def drawSprite(m,self):
	if m.type==0: img=self.imagesTarget[0]
	elif m.type==KAKUNA: 
		if m.evo==0: img=self.imagesKakun[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesBeedr[dirs[m.dir]+frames[m.start]]
	elif m.type==KINGDRA: img=self.imagesKingd[dirs[m.dir]+frames[m.start]]
	elif m.type==ZUBAT: img=self.imagesZubat[dirs[m.dir]+frames[m.start]]
	elif m.type==EKANS: img=self.imagesEkans[dirs[m.dir]+frames[m.start]]
	elif m.type==ESPEON:img=self.imagesEspeo[dirs[m.dir]+frames[m.start]]
	elif m.type==CHAR: 
		if m.evo==0: img=self.imagesCharm[dirs[m.dir]+frames[m.start]]
		elif m.evo==1: img=self.imagesChara[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesChari[dirs[m.dir]+frames[m.start]]
	elif m.type==NINJ:
		if m.evo==0: img=self.imagesNinca[dirs[m.dir]+frames[m.start]]
		elif m.evo==1: img=self.imagesNinja[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesShedi[dirs[m.dir]+frames[m.start]]
	elif m.type==SAND:
		if m.evo==0: img=self.imagesShrew[dirs[m.dir]+frames[m.start]]
		elif m.evo==1: img=self.imagesSlash[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesTarget[3]
	elif m.type==ENTEI: img=self.imagesEntei[dirs[m.dir]+frames[m.start]]
	elif m.type==KENGIS: 
		if m.evo==0: img=self.imagesKengi[dirs[m.dir]+frames[m.start]]
		elif m.evo==1: img=self.imagesKengB[dirs[m.dir]+frames[m.start]]
		elif m.evo==2: img=self.imagesCubon[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesCubTh[dirs[m.dir]+frames[m.start]]
	elif m.type==MAGNET:
		if m.evo==0: img=self.imagesMagni[dirs[m.dir]+frames[m.start]]
		elif m.evo==1: img=self.imagesMagne[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesMagn2[dirs[m.dir]+frames[m.start]]
	elif m.type==GOLEM: 
		if m.evo==0: img=self.imagesGolem[dirs[m.dir]+frames[m.start]]
		else: img=self.imagesAura1[frames[m.start]]
	else: img=self.imagesTarget[dirs[m.dir]+frames[m.start]]
	try: image(img, m.location.x, m.location.y, 32, 32)
	except: image(img, m.x, m.y, 32, 32)
	return

#Direction the touch is leading.  Also used to make some monsters follow player.
def touchdirections(dir, source):
	dx,dy=dir.x-source.x,dir.y-source.y
	if dx<0:dx*=-1
	if dy<0:dy*=-1
	if dx>dy:
		if dir.x > source.x: output=3 #Right
		else: output=1 								#Left
	else:
		if dir.y>source.y: output=2		#Up
		else: output=0								#Down
	return output
	
def moveNormal(location, size, speed, dt, mvm, boost=1):
	location.x = wrap((location.x+(mvm[0]*(1-speed)*boost*dt)), size)
	location.y = wrap((location.y+(mvm[1] *(1-speed)*boost* dt)), size)
	return location

#Resets position, and if necessary also kills
def resetPosition(self, kill=False):
	self.talkS=talk("Resetting Position?",self.talkS)
	self.x = selfSpawn[self.level].x
	self.y = selfSpawn[self.level].y
	self.target=Point(self.x,self.y)
	if kill: self.lives-=1
	return self
	
def getframe(x, y, image):
	return load_pil_image(image.crop((x * 32, y * 32, (x+1) * 32, (y+1) * 32)))
	
def getframes(image):
	return [getframe(x,y,image) for y in xrange(4) for x in xrange(3)]

class MyScene (Scene):
	def should_rotate(self,orientation):
		print(orientation)
		return False
	def setup(self):
		img=loadImage('Images','soldier2.png',
		              'http://i766.photobucket.com/albums/xx303/TurtleSoupguild/iPadGame_Sprites2-3.png')
		#img.show()
		bg=loadImage('Images','gameBG.png',
		             'http://i766.photobucket.com/albums/xx303/TurtleSoupguild/iPadGame_BG-2.png')
		splash=loadImage('Images','gameSplash',
		                 'http://i766.photobucket.com/albums/xx303/TurtleSoupguild/iPadGame_Splash.png')
		self.imagesKingd=getframes(cropImage(img,Point(0, 0)))
		self.imagesGolem=getframes(cropImage(img,Point(1, 0))) #New Golem
		self.imagesEkans=getframes(cropImage(img,Point(2, 0)))
		self.imagesChari=getframes(cropImage(img,Point(3, 0))) #CHAR
		self.imagesChara=getframes(cropImage(img,Point(4, 0))) #CHAR
		self.imagesEntei=getframes(cropImage(img,Point(0, 1)))
		self.imagesZubat=getframes(cropImage(img,Point(1, 1)))
		self.imagesEspeo=getframes(cropImage(img,Point(2, 1)))
		self.imagesNinca=getframes(cropImage(img,Point(3, 1)))
		self.imagesCharm=getframes(cropImage(img,Point(4, 1))) #CHAR
		self.imagesShrew=getframes(cropImage(img,Point(0, 2)))
		self.imagesSlash=getframes(cropImage(img,Point(1, 2)))
		self.imagesNinja=getframes(cropImage(img,Point(2, 2)))
		self.imagesShedi=getframes(cropImage(img,Point(3, 2)))
		self.imagesAura1=getframes(cropImage(img,Point(4, 2))) #golem aura block
		self.imagesKakun=getframes(cropImage(img,Point(0, 3)))
		self.imagesBeedr=getframes(cropImage(img,Point(1, 3))) #New Beedril
		self.imagesMagni=getframes(cropImage(img,Point(2, 3))) #New Magnetite
		self.imagesMagn2=getframes(cropImage(img,Point(3, 3))) #New Magnetite+
		self.imagesMagne=getframes(cropImage(img,Point(4, 3))) #New Magneton
		self.imagesCubon=getframes(cropImage(img,Point(0, 4))) #New Cubone
		self.imagesKengB=getframes(cropImage(img,Point(1, 4))) #New Kengiskan Baby
		self.imagesCubTh=getframes(cropImage(img,Point(2, 4))) #New Cubone Throwing
		self.imagesKengi=getframes(cropImage(img,Point(3, 4))) #New Kengiskan
		self.imagesTarget=getframes(cropImage(img,Point(4, 4))) #New
		#self.imagesTarget=getframes(cropImage(img,Point(4, 2)))
		self.splash=[load_pil_image(splash),splash.size]
		self.bg=load_pil_image(bg)
		self.startScreen=True
		self.talkS=["Welcome to my game, made by eliskan.",
             		"Sprites from Pokémon Mystery Dungeon",
             		"Try to collect Pokéballs, but if you",
             		"are hit you will de-evolve or die!",
             		"\n","\n"]
		self.type=MAGNET
		self.special=0 #For special abilities, like fireballs.
		self.evoAura=1.
		self.evo  =0   #Keeps track of pokemon evolution level.
		self.start=0   
		self.base =0
		self.dir  =0   #Tells which direction we're facing
		self.score=0   #Keeps track of score.  At score==3, level ends.
		self.lives=3   #Lives
		self.level=0   #Level
		self.delay = speed
		#resetPosition(self, False)
		self.x = selfSpawn[self.level].x
		self.y = selfSpawn[self.level].y
		self.target=Point(self.x,self.y)
		self.collisions=set() #set up collision objects like walls
		for box in levels[self.level]: self.collisions.add(box)
		self.monsters=set() #set up monsters
		for mons in levelsMonsters[self.level]: self.monsters.add(mons)
		
	#def touch_moved(self, touch):
		#self.dir = touchdirections(touch.location,self)
		#d = self.dir
	def touch_ended(self, touch):
		if self.startScreen==True:
			self.startScreen=False
			return
		hit=-1
		#Buttons in scoreboard:
		if touch.location.x>768:
			for i in range(len(scoreButtons)):
				if hitTest2(touch.location,Point(1,1),Point(scoreButtons[i][0].x+775,
				                                            scoreButtons[i][0].y+650),scoreButtons[i][1]):hit=i
		elif touch.location.y>768:
			for i in range(len(scoreButtons)):
				if hitTest2(touch.location,Point(1,1),Point(scoreButtons[i][0].x+650,
				                                            scoreButtons[i][0].y+775),scoreButtons[i][1]):hit=i
		else:
			self.dir = touchdirections(touch.location,self) 
			self.target.x=touch.location.x-mvm
			self.target.y=touch.location.y-mvm
			if self.target.x<0:self.target.x=0
			if self.target.y<0:self.target.y=0
			#If we're Char, shoot a fireball.
			if self.type==CHAR and self.special==0:
				self.special=[mov[self.dir],Point(self.x,self.y),self.evo]
			#If we're Sandslash, we can turn into invincible but unmoveable
			if self.type==SAND and self.evo!=0:
				if hitTest2(touch.location,Point(1,1),Point(self.x,self.y),Point(moveamt,moveamt)):
					if self.evo==1: self.evo+=1
					else: self.evo-=1
		if hit==0:
			self.talkS=talk("Debug: Changing Type",self.talkS)
			if self.type<13:
				self.type+=1
			else: self.type=1
			self.evo=0
			self.special=0
		elif hit==1: 
			self.talkS=talk("Debug: Forcing Evolution",self.talkS)
			if self.type==NINJ:
				self.special=monster(Point(self.x,self.y),Point(32,32),NINJ)
				self.special.evo=3
			self.evo+=1
			self.evoAura+=1
		elif hit==2:
			self.talkS=talk("Debug: Going forward one level",self.talkS)
			self.score=0
			self.level+=1
			if self.level>len(levels)-1:self.level=0
			self=resetPosition(self, False)
			self.monsters=set()
			self.collisions=levels[self.level]
			for i in levelsMonsters[self.level]: self.monsters.add(i)
		elif hit==3: 
			self.talkS=talk("Debug: Killing all monsters",self.talkS)
			self.monsters=set()

		
 
	def draw(self):
		if self.startScreen==True: #This is the start screen
			fill(0,0,0)
			rect(0,0,self.size.w,self.size.h)
			image(self.splash[0], self.bounds.center().x-self.splash[1][0]/2,
			      self.bounds.center().y-self.splash[1][1]/4,self.splash[1][0], self.splash[1][1])
			text('Touch the screen to begin.',
			     'Futura', 40, self.bounds.center().x,self.bounds.center().y-self.splash[1][1])
			return #Return is used to force draw to stop.  So if it's a start screen, it ends.
		image(self.bg, 0, 0, 768, 768) #Draw the background
		mv = mov[self.dir]
		if self.type==SAND and self.evo==2: pass
		elif self.target.x>self.x+hitRange or self.target.x<self.x-hitRange:
			if self.target.x>self.x+hitRange:self.dir=3
			else:self.dir=1
			self.x += mv[0] *boost* self.dt
			self.x = wrap(self.x, self.size)
		elif self.target.y>self.y+hitRange or self.target.y<self.y-hitRange:
			self.dir=touchdirections(self.target,self)
			self.y += mv[1] *boost* self.dt
			self.y = wrap(self.y, self.size)
		self.delay -= self.dt
		if self.delay <= 0:
			self.delay += speed
			self.start += 1
			if self.start >= len(frames): self.start = 0
		dead=set()
		for z in self.collisions:
			if z.type==0: fill(0,0,1,0.1) #Alpha=0
			elif z.type==1: fill(1,0,0)
			elif z.type==2: fill(.15,0,.15)
			else: fill(0,1,0)
			rect(z.location.x,z.location.y,z.size.x,z.size.y)
			hitz=hitTest2(Point((self.x+moveamt/3),
			                    (self.y+moveamt/3)),
			                    Point(hitRange,hitRange),z.location,z.size)
			if hitz!=0: #If we hit a wall, react to the hit
				r=hitReact(Point(self.x,self.y),z.location,z.type,hitz,boost)
				z.location=r[1]	
				self.x,self.y=r[0].x,r[0].y
				if z.type==2:# or z.type==3:
					self.target.x,self.target.y=self.x,self.y
			for m in self.monsters:
				hitz=hitTest2(m.location,m.size,z.location,z.size)
				if hitz!=0:
					r=hitReact(m.location,Point(z.location.x,z.location.y),z.type,hitz,1,True)
					m.location=r[0]
					#z.location=r[1]
					if m.type==GOLEM:
						for i in range(m.evo+1): #Golem runs through walls without this evo loop
							m.location=hitReact(m.location,z.location,z.type,hitz,1,True)[0]
					if z.type!=1:
						r=randint(0,3)
						while r==m.dir:r=randint(0,3)
						m.dir=r
		newMonster=[]
		for m in self.monsters:
			if m.type!=0:#Only moving monsters
				m.movlen+=1
				if m.movlen>100:
					m.movlen=0
					m.dir=randint(0,3)
				mvm=mov[m.dir]
				if not m.type==CHAR and not m.type==SAND and not m.type==KENGIS:
					m.location=moveNormal(m.location,self.size,speedMonsters,self.dt,mvm)
				m.delay -= self.dt
				if m.delay <= 0:
					m.delay += speedMonsters
					m.start += 1
				if m.start >= len(frames): m.start = 0
				
				if m.type==KAKUNA: #Kakuna runs towards.  Beedrill has a larger range.
					if m.evo==0:
						if randint(0,2000)==1: m.evo+=1
						dist=70
						big=130
					else:
						dist=50
						big=160
					tempX=self.x-m.location.x
					tempY=self.y-m.location.y
					if tempX>dist or tempX<dist*-1 or tempY>dist or tempY<dist*-1:
						if not tempX>big and not tempX<big*-1 and not tempY>big and not tempY<big*-1:
							tempX/=120
							tempY/=120
						else: tempX,tempY=0,0
					else: tempX,tempY=0,0
					m.location.x+=tempX
					m.location.y+=tempY
					img=self.imagesKakun[dirs[m.dir]+frames[m.start]]
					
				elif m.type==KINGDRA: #Kingdra runs 2x fast
					m.location=moveNormal(m.location,self.size,speedMonsters,self.dt,mvm,boost)
					
				elif m.type==ZUBAT: #Zubat runs away
					dist=200
					tempX=self.x-m.location.x
					tempY=self.y-m.location.y
					if tempX<dist and tempX>dist*-1 and tempY<dist and tempY>dist*-1:
						m.location.x+=(m.location.x-self.x)/500
						m.location.y+=(m.location.y-self.y)/500
				
				elif m.type==EKANS: img=self.imagesEkans[dirs[m.dir]+frames[m.start]]
				
				elif m.type==ESPEON: #Espeon slowly stalks from any distance
					m.location.x+=(self.x-m.location.x)/2000
					m.location.y+=(self.y-m.location.y)/2000
					
				elif m.type==CHAR: #Char evolves when you get too close and throws fireballs.
					dist=200				 #If it's Charizard, he actively follows the target while firing.
					tempX=self.x-m.location.x	#Fireballs also rebound from the walls.
					tempY=self.y-m.location.y
					if m.special!=0: #If Char is shooting a fireball...
						reset=0
						mvm2=m.special[0]
						m.special[1].x+=mvm2[0] *(1+(m.special[2]*2))* self.dt
						m.special[1].y+=mvm2[1] *(1+(m.special[2]*2))* self.dt
						img=self.imagesTarget[6]
						image(img,m.special[1].x,m.special[1].y,32,32) #Load fireball
						if m.special[1].x<0 or m.special[1].x>self.size.w or m.special[1].y<0 or m.special[1].y>self.size.h: reset=1 #Kill fireball if it goes offscreen
						elif hitTest2(m.special[1],Point(moveamt,moveamt),
						              Point(self.x,self.y),Point(moveamt,moveamt)):
							if self.evo>0:
								if self.type==SAND and self.evo>=2: pass
								else:
									self=resetPosition(self, False)
									self.evo-=1
									self.special=0
							else: self=resetPosition(self,True)
							reset=1
							self.talkS=talk("Hit by a fireball.",self.talkS)
						hitSet.add(m)
						self.special=0
						if m.evo<2: m.evo+=1
						else:
							for z in self.collisions:
								if hitTest2(m.special[1],Point(moveamt,moveamt),z.location,z.size): 
									if randint(0,1)==1: reset=1
									else: m.special[0]=[(mvm2[0]*-1),(mvm2[1]*-1)]
						if reset: m.special=0
					if tempX<dist and tempX>dist*-1 and tempY<dist and tempY>dist*-1: #Char burns
						if m.special==0: m.special=[mov[m.dir],Point(m.location.x,m.location.y),m.evo]
						if m.evo<2 and randint(0,1000*(m.evo+1))==1: m.evo+=1
						if self.type==SAND and self.evo>=2: pass
						else: m.dir=touchdirections(Point(self.x,self.y),m.location)
						img=self.imagesTarget[6+frames[m.start]] #Load Aura
						image(img, m.location.x, m.location.y, 32, 32)
						dist=0
					elif m.evo<2 and randint(0,10000*(m.evo+1))==1: m.evo+=1
					if dist==200 or m.evo==2: 
						m.location=moveNormal(m.location,self.size,speedMonsters,self.dt,mvm)
						
				elif m.type==NINJ: #Nincanda splits apart.  Also uses stringshot.
					dist=200
					tempX=self.x-m.location.x
					tempY=self.y-m.location.y
					if tempX<dist and tempX>dist*-1 and tempY<dist and tempY>dist*-1:
						stroke(1,1,1,0.3)
						stroke_weight(randint(1,2))
						tempX=(self.x-m.location.x)/3000
						tempY=(self.y-m.location.y)/3000
						for i in range((m.evo+1)*2):
							self.x-=tempX
							self.target.x-=tempX
							self.y-=tempY
							self.target.y-=tempY
							tempX2=self.x+moveamt/2+(randint(1,14)-7)
							tempY2=self.y+moveamt/2+(randint(1,14)-7)
							line(tempX2,tempY2,m.location.x+moveamt/2,m.location.y+moveamt/2)
						stroke(1,1,1,0)
					if m.evo==0:
						if randint(0,10000)==1:
							shedinja=monster(Point(m.location.x,m.location.y),Point(32,32),NINJ)
							shedinja.evo=3
							newMonster=(shedinja)
							m.evo+=1 
							
				elif m.type==SAND: #Sandslash and sandshrew.  Sandslash curls into a ball.
					if m.evo==0: 
						if randint(0,1000)==1: m.evo+=1
					elif m.evo==1: 
						if randint(0,1000)==1: m.evo+=1
					else: #This 'third' evolution is just Sandslash in a ball
						if randint(0,1000)==1: m.evo-=1
					if not m.evo==2: m.location=moveNormal(m.location,self.size,speedMonsters,self.dt,mvm)
					
				elif m.type==ENTEI: #Entei's direction changes towards player.
					tempInt=randint(0,100)
					if tempInt==1: m.dir=touchdirections(Point(self.x,self.y),Point(m.location.x,self.y))
					elif tempInt==2: m.dir=touchdirections(Point(self.x,self.y),Point(self.x,m.location.y))
					
				elif m.type==KENGIS: #Kengis babies follow momma around.  If mom dies, a baby becomes Cubone
					if not m.evo==3: m.location=moveNormal(m.location,self.size,speedMonsters,self.dt,mvm)
					if m.evo==0: #0 is Kengiskan
						if m.special==0: m.special=[0,m]
						if m.special[0]<5 and randint(0,100)==1: #Spawns babies.
							m.special[0]+=1
							babyKengis=monster(Point(m.location.x,m.location.y),Point(32,32),KENGIS)
							babyKengis.evo=1
							babyKengis.special=[0,m]
							newMonster=(babyKengis)
					elif m.evo==1: #1 is Kengis baby.
						tempM=m.special[1]
						tempInt=randint(0,5)
						if tempInt==1:  m.dir=touchdirections(Point(tempM.location.x,tempM.location.y),m.location)
						if not m.special[1] in self.monsters and randint(0,100)==1: #If mother is dead...
							m.evo+=1
							m.special=0
					elif m.evo==2: #2 is a Cubone
						dist=200
						tempX=self.x-m.location.x
						tempY=self.y-m.location.y
						if tempX>dist or tempX<dist*-1 or tempY>dist or tempY<dist*-1: pass
						else: 
							m.evo+=1
							m.special=0
					else: #3 is Cubone throwing a bone
						if m.start>2:m.start=2
						m.dir=touchdirections(Point(self.x,self.y),m.location)
						if m.special==0: 
							m.special=[Point(m.location.x,m.location.y),
							           Point(self.x,self.y),
							           Point((m.location.x-self.x)/200,(m.location.y-self.y)/200),0]
						img=self.imagesTarget[4]
						image(img,m.special[0].x,m.special[0].y,32,32) #Load bone
						m.special[0].x-=m.special[2].x
						m.special[0].y-=m.special[2].y
						if hitTest2(m.special[0],Point(2,2),
						            m.special[1],Point(5,5)):
							m.special[2]=Point((m.special[1].x-m.location.x)/10,(m.special[1].y-m.location.y)/10)
							m.special[3]=1
						elif m.special[3]!=0 and hitTest2(m.special[0],Point(32,32),
						              m.location,Point(32,32)): m.evo-=1
						elif hitTest2(Point(m.special[0].x+moveamt/2-8,m.special[0].y+moveamt/2-8),Point(16,16),
						              Point(self.x+moveamt/2-4,self.y+moveamt/2-4),Point(8,8)):
							self.talkS=talk("Hit by a Cubones' bone",self.talkS)
							if self.evo>0: 
								if not self.type==SAND and not self.evo>=2:
									self=resetPosition(self, False)
									self.evo-=1
									self.special=0
							else: self=resetPosition(self,True)
							
				elif m.type==GOLEM: #Golem runs really fast when 'evolved' into a ball
					if m.evo==0:
						if randint(0,500)==1: m.evo+=1
					else:
						if m.evo<2 and randint(0,100)==1: m.evo+=1
						elif randint(0,200)==1: m.evo-=1
						for i in range(m.evo): 
							m.location=moveNormal(m.location,self.size,speedMonsters,self.dt,mvm,boost)
							
				elif m.type==MAGNET: #MAGNET zaps the player periodically, messing up their direction
					if m.special==0: m.special=[0,0,0] #[Timer until zap, Timer until zap ends, evo Timer]
					dist=125+m.evo*20 #Range of zap.  Evolved versions zap further
					tempX=self.x-m.location.x
					tempY=self.y-m.location.y
					if tempX<dist and tempX>dist*-1 and tempY<dist and tempY>dist*-1: #If within range:
						if m.special[0]>50: #If it's time to zap:
							m.special[0]=0 						#Reset timer
							m.special[1]=10+m.evo*15  #Length of zap
							if m.evo==0: 
								m.special[2]+=1
								if m.special[2]>2: m.evo+=1 #Evolve by zapping the player >:D
						else: m.special[0]+=1 #Otherwise increase zap timer
						if m.special[1]>0:
							m.special[1]-=1
							if self.type==SAND and self.evo>=2: pass 
							else: 
								self.dir=choice([touchdirections(m.location,Point(self.x,self.y)),randint(0,3)])
							lightning(Point(int(round(self.x+moveamt/2)),
						 		             int(round(self.y+moveamt/2))),
						   		           Point(int(round(m.location.x+moveamt/2)),
						     		         int(round(m.location.y+moveamt/2))))
					elif m.special[1]>0: m.special[1]=0 #Force the zap to end if we're out of range
						
			drawSprite(m,self)
			hit=hitTest2(Point(self.x+moveamt/3,self.y+moveamt/3),Point(hitRange,hitRange),m.location,m.size)
			hitSet=set()
			if hit!=0:
				if m.type!=0:
					if self.type==SAND and self.evo>=2:
						self.talkS=talk("Hit by "+stringType(m),self.talkS)
						difx,dify=(self.x-m.location.x)/10,(self.y-m.location.y)/10
						m.location=Point(m.location.x-difx,m.location.y-dify)
					else: 
						self.talkS=talk("Killed by "+stringType(m),self.talkS)
						hitSet.add(m)
						self=resetPosition(self, False)
						self.special=0
						
				else: 
					self.talkS=talk("Collected Pokéball.",self.talkS)
					self.score+=1
					dead.add(m)
			if self.evo<=0: self.lives-=len(hitSet)
			else: self.evo-=len(hitSet)
			
		#Add and remove monsters, also change level if score>3
		self.monsters-=dead 
		if newMonster: self.monsters.add(newMonster)
		if self.score>=3: # new level
			self.score=0
			if self.level<len(levels)-1: self.level+=1
			else: self.level=0
			self.talkS=talk("Completed Level "+str(self.level)+"!",self.talkS)
			self.monsters=set()
			self.collisions=levels[self.level]
			self=resetPosition(self, False)
			for i in levelsMonsters[self.level]: self.monsters.add(i)
		if len(self.monsters)<len(levelsMonsters[self.level]) and randint(1,100)==1:
			l=Point(monsSpawn[self.level].x,monsSpawn[self.level].y)
			self.monsters.add(monster(l,Point(32,32),choice([KAKUNA,ZUBAT,NINJ,CHAR,MAGNET])))
		
		
		#CHARACTER SCRIPTED BEHAVIORS
		if self.evoAura>0.0: #evoAura performs the effect when player evolves.
			tint(1,1,1,self.evoAura)
			img=self.imagesTarget[9+frames[self.start]] #Load Aura
			image(img, self.x, self.y, 32, 32)
			self.evoAura-=.01
			tint(1,1,1,1)
		if self.type==CHAR:   #SHOOTS FIREBALLS
			if self.special==0: #FIRE AURA
				img=self.imagesTarget[6+frames[self.start]] #Load Aura
				image(img, self.x, self.y, 32, 32)
			else:
				reset=0
				mvm2=self.special[0]
				self.special[1].x+=mvm2[0] *(4+(self.special[2]*2))* self.dt
				self.special[1].y+=mvm2[1] *(4+(self.special[2]*2))* self.dt
				img=self.imagesTarget[6]
				image(img,self.special[1].x,self.special[1].y,32,32) #Load fireball
				if self.special[1].x<0 or self.special[1].x>self.size.w or self.special[1].y<0 or self.special[1].y>self.size.h: reset=1 #Kill fireball if it goes offscreen
				else:
					dead=set()
					for m in self.monsters:
						if hitTest2(self.special[1],Point(moveamt,moveamt),m.location,m.size): 
							reset=1
							if not m.type==0:
								if m.type==SAND and m.evo==2: pass
								else:
									self.talkS=talk("Killed "+stringType(m)+" with a fireball",self.talkS)
									dead.add(m)
									if self.evo<2:
										self.evo+=1
										self.evoAura=1
					self.monsters-=dead
					for z in self.collisions:
						hitz=hitTest2(self.special[1],Point(moveamt,moveamt),z.location,z.size)
						if hitz: 
							r=hitReact(self.special[1],z.location,z.type,hitz,1,False)
							z.location=r[1] #This allows fireballs to push moveable walls
							reset=1
				if reset: self.special=0
		
		elif self.type==SAND: #SANDSHREW CAN BALL UP TO BECOME INVINCIBLE AND IMMOBILE
			if self.evo==0 and randint(0,100)==1: 
				self.evo+=1
				self.evoAura=1
			#if self.special==0: image(self.imagesTarget[9+frames[self.start]], self.x, self.y, 32, 32) #Aura
			
		elif self.type==NINJ: #SPAWNS A FRIENDLY SHEDINJA WHEN EVOLVED
			if self.evo==0:
				try:self.special+=1
				except:self.special=0
				if self.special==1000: self.evo+=1
			elif self.evo==1 and self.special==1000:
				self.evoAura=2
				self.special=monster(Point(self.x,self.y),Point(32,32),NINJ)
				self.special.evo=3
			else:
				mvm=mov[self.special.dir]
				tempInt=0
				for z in self.collisions:
					hitz=hitTest2(self.special.location,Point(moveamt,moveamt),z.location,z.size)
					if hitz:
						tempInt=1
						r=hitReact(self.special.location,z.location,z.type,hitz,1,True)
						self.special.location=r[0]
						z.location=r[1]
						#self.special.dir=reverseDir(self.special.dir)
				if not tempInt: 
					self.special.location=moveNormal(self.special.location,self.size,
				                                 speedMonsters,self.dt,mvm,boost)
				dead=set()
				for m in self.monsters:
					hitz=hitTest2(self.special.location,Point(moveamt,moveamt),m.location,Point(moveamt,moveamt))
					if hitz:
						if m.type==SAND and m.evo==2: pass
						elif m.type==0: pass
						else: 
							self.talkS=talk("Shedinja killed "+stringType(m),self.talkS)
							dead.add(m)
							self.special.dir=reverseDir(self.special.dir)
				self.monsters-=dead
				tempInt=randint(0,20)
				loc=self.special.location
				if tempInt==1:   self.special.dir=touchdirections(Point(self.x,loc.y),Point(loc.x,loc.y))
				elif tempInt==2: self.special.dir=touchdirections(Point(loc.x,self.y),Point(loc.x,loc.y))
				self.special.start=self.start
				drawSprite(self.special,self)
				
		elif self.type==MAGNET: #MAGNET spawns friendly balls around him.  His code is complex.
			remove=0
			if self.special==0: self.special=[0,[],[],0] #[population,[rotation],[monster],spawnCount]
			else:
				if self.special[0]>1 and self.evo==0 and randint(0,100)==1: #When evolving, removes 2
					self.special[0]-=2
					self.special[1].remove(self.special[1][0-1])
					self.special[2].remove(self.special[2][0-1])
					self.evo+=1
					self.evoAura+=2
				if self.special[0]<5: #If number of population is less than 5
					if self.special[3]<500: self.special[3]+=1 #Increase spawn counter by 1
					else:																			 #Spawn counter complete
						self.special[3]=0 											 #Reset the counter
						self.special[0]+=1											 #Increase population
						self.special[1].append(randint(5,15))		 #Append a new rotation amount
						magnetite = monster(Point(self.x+randint(-25,25),
						                          self.y+randint(-25,25)),Point(32,32),MAGNET)
						magnetite.evo+=2
						#if magnetite.evo!=2: magnetite.evo+=2
						self.special[2].append(magnetite)				 #Append a new monster
				if self.special[0]: #If there is a population
					dead=set() #Set up dead monsters
					for i in range(self.special[0]):
						self.special[1][i]+=.005									#Rotation
						difference=dif(self.special[2][i].location,Point(self.x,self.y))
						divAmount=0
						if difference>200:												#Force them to spawn on player
							self.special[2][i].location.x=self.x+randint(-25,25)
							self.special[2][i].location.y=self.y+randint(-25,25)
						elif difference>50:divAmount=12						#Force them to float around self
						elif difference>32: divAmount=150
						if divAmount:
							self.special[2][i].location.x-=(self.special[2][i].location.x-self.x)/divAmount
							self.special[2][i].location.y-=(self.special[2][i].location.y-self.y)/divAmount
						lightning(Point(int(round(self.x+moveamt/2)),
						                int(round(self.y+moveamt/2))),
						                Point(int(round(self.special[2][i].location.x+moveamt/2)),
						                int(round(self.special[2][i].location.y+moveamt/2))))
						if self.special[1][i]>360: self.special[1][i]=0
						self.special[2][i].location=findRotation(Point(self.x,self.y),
						                                         self.special[2][i].location, self.special[1][i])
						for m in self.monsters:
							if m.type==SAND and m.evo==2: pass #Ignores hitting Sandshrew in a ball
							elif m.type==0: pass							 #Ignores hitting the level's target
							else:
								hitz=hitTest2(self.special[2][i].location,
							              Point(moveamt,moveamt),m.location,Point(moveamt,moveamt))
								if hitz:
									self.talkS=talk("Magnetite killed "+stringType(m),self.talkS)
									dead.add(m)
									remove=1
									remove1=self.special[1][i]
									remove2=self.special[2][i]
						self.special[2][i].dir=touchdirections(Point(self.x,self.y),
						                        Point(self.special[2][i].location.x,
						                              self.special[2][i].location.y))
						self.special[2][i].start=self.start
						drawSprite(self.special[2][i],self)
					if remove:
						self.special[0]-=1
						self.special[1].remove(remove1)
						self.special[2].remove(remove2)
						self.monsters-=dead
						
		elif self.type==KAKUNA:
			if self.evo==0 and randint(0,100)==1: self.evo+=1
		drawSprite(self,self) #Finally draw the player
		score(self) #Draw the score board.  Also contains developer tools (aka game hax!)
run(MyScene(), LANDSCAPE)
