# http://stackoverflow.com/questions/20924085/python-conversion-between-coordinates

import math

def rect(r, theta):
	"""theta in degrees
	
	returns tuple; (float, float); (x,y)
	"""
	x = r * math.cos(math.radians(theta))
	y = r * math.sin(math.radians(theta))
	return x,y
	
def polar(x, y):
	"""returns r, theta(degrees)
	"""
	r = (x ** 2 + y ** 2) ** .5
	if y == 0:
		theta = 180 if x < 0 else 0
	elif x == 0:
		theta = 90 if y > 0 else 270
	else:
		theta = math.degrees(math.atan(float(y) / x))
	return r, theta
	
class Point(object):
	def __init__(self, x=None, y=None, r=None, theta=None):
		"""x and y or r and theta(degrees)
		"""
		if x and y:
			self.c_polar(x, y)
		elif r and theta:
			self.c_rect(r, theta)
		else:
			raise ValueError('Must specify x and y or r and theta')
	def c_polar(self, x, y, f = polar):
		self._x = x
		self._y = y
		self._r, self._theta = f(self._x, self._y)
		self._theta_radians = math.radians(self._theta)
	def c_rect(self, r, theta, f = rect):
		"""theta in degrees
		"""
		self._r = r
		self._theta = theta
		self._theta_radians = math.radians(theta)
		self._x, self._y = f(self._r, self._theta)
	def setx(self, x):
		self.c_polar(x, self._y)
	def getx(self):
		return self._x
	x = property(fget = getx, fset = setx)
	def sety(self, y):
		self.c_polar(self._x, y)
	def gety(self):
		return self._y
	y = property(fget = gety, fset = sety)
	def setxy(self, x, y):
		self.c_polar(x, y)
	def getxy(self):
		return self._x, self._y
	xy = property(fget = getxy, fset = setxy)
	def setr(self, r):
		self.c_rect(r, self._theta)
	def getr(self):
		return self._r
	r = property(fget = getr, fset = setr)
	def settheta(self, theta):
		"""theta in degrees
		"""
		self.c_rect(self._r, theta)
	def gettheta(self):
		return self._theta
	theta = property(fget = gettheta, fset = settheta)
	def set_r_theta(self, r, theta):
		"""theta in degrees
		"""
		self.c_rect(r, theta)
	def get_r_theta(self):
		return self._r, self._theta
	r_theta = property(fget = get_r_theta, fset = set_r_theta)
	def __str__(self):
		return '({},{})'.format(self._x, self._y)

