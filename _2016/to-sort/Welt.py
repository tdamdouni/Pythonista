class Welt(object):

	# Konstruktor
	def __init__(self,laenge=10,breite=10,hoehe=10):
		self.Laenge = laenge
		self.Breite = breite
		self.Hoehe  = hoehe
		
		# eine zweidimensionale Liste anlegen und mit Nullen fuellen
		self.Ziegel = [[0 for i in range(breite)] for j in range(laenge)]
		
	# Anzahl der Ziegel an einer bestimmten Position direkt eingeben
	def setZiegel(self,x,y,anzahl):
		self.Ziegel[x][y] = anzahl
		
	# Anzahl der Ziegel an einer bestimmten Position um 1 erhoehen
	def hinlegenZiegel(self,x,y):
		if self.Ziegel[x][y] < self.Hoehe:
			self.Ziegel[x][y] += 1
			
	# Anzahl der Ziegel an einer bestimmten Position um 1 erniedrigen
	def aufhebenZiegel(self,x,y):
		if self.Ziegel[x][y] > 0:
			self.Ziegel[x][y] -= 1
			
			
class Roboter(object):

	# Konstruktor
	def __init__(self,welt,posx=0,posy=0,richtung=[1,0]):
		self.Welt = welt
		self.Posx = posx
		self.Posy = posy
		self.Richtung = richtung
		
	# ein Feld nach vorne gehen, falls moeglich
	def schritt(self):
		self.Posx += self.Richtung[0]
		if self.Posx < 0: self.Posx = 0
		if self.Posx > self.Welt.Laenge - 1:
			self.Posx = self.Welt.Laenge - 1
		self.Posy += self.Richtung[1]
		if self.Posy < 0: self.Posy = 0
		if self.Posy > self.Welt.Breite - 1:
			self.Posy = self.Welt.Breite - 1
			
	# nach rechts drehen
	def rechtsDrehen(self):
		if self.Richtung == [1,0]:
			self.Richtung = [0,1]
		elif self.Richtung == [0,1]:
			self.Richtung = [-1,0]
		elif self.Richtung == [-1,0]:
			self.Richtung = [0,-1]
		else:
			self.Richtung = [1,0]
			
	# nach links drehen
	def linksDrehen(self):
		if self.Richtung == [1,0]:
			self.Richtung = [0,-1]
		elif self.Richtung == [0,1]:
			self.Richtung = [1,0]
		elif self.Richtung == [-1,0]:
			self.Richtung = [0,1]
		else:
			self.Richtung = [-1,0]
			
	# einen Ziegel vor den Roboter legen falls moeglich
	def hinlegen(self):
		ziegelposx = self.Posx + self.Richtung[0]
		ziegelposy = self.Posy + self.Richtung[1]
		if 0 <= ziegelposx < self.Welt.Laenge and 0<= ziegelposy < self.Welt.Breite:
			self.Welt.hinlegenZiegel(ziegelposx,ziegelposy)
			return True
		else:
			return False
			
	# einen Ziegel vor dem Roboter aufheben falls moeglich
	def aufheben(self):
		ziegelposx = self.Posx + self.Richtung[0]
		ziegelposy = self.Posy + self.Richtung[1]
		if 0 <= ziegelposx < self.Welt.Laenge and 0<= ziegelposy < self.Welt.Breite:
			self.Welt.aufhebenZiegel(ziegelposx,ziegelposy)
			return True
		else:
			return False

