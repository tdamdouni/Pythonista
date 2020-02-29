'''Functional math module.
ARGS ARE NOT INCLUDED IN MODULE DOCSTRING. For those, see the function/classmethod docstring.
If sympy is available, it will be used.  Otherwise, the math module is used as a base.
Vars, functions, and classes:

    Vars

        pi_acc            Pi accurate to 311 digits
        e_acc             Euler's number accurate to 311 digits
        pi_str            String version of pi_acc
        e_str             String version of e_acc
        m                 builtin math module
        cm                builtin cmath module
        fr                builtin fractions module
        has_sympy         Boolean; whether the sympy module is installed

    Functions

        Sequences

            fibo()            Fibonacci sequence lister
            tri()             Triangular number lister
            tetra()           Tetrahedral number lister
            hexagonal()       Hexagonal number lister
            pentatope()       Pentatope number lister
            catalan()         Catalan number lister

        Algebraic

            foil()            Distribute (a + b) * (c + d)

        Trigonometric

            sin2()            sin^2
            cos2()            cos^2
            cot()             cotangent
            acot()            arc cotangent
            sec()             secant
            asec()            arc secant
            csc()             cosecant
            exsec()           exsecant
            excsc()           excosecant
            versin()          versed sine
            cvs()             coversin

        Misc

            egypt()           Find egyptian fractions
            root()            Take the nth root of a number
            frac_root()       Take fractional roots of a number
            avg()             Average of a set of numbers
            ack()             Ackermann function for m, n
            factors()         Find the factors of a number
            factorial()       Factorial of a number
            dist()            Distance between two points
            midpoint()        Middle point of two points
            diag()            Number of diagonals for a n-gon
            angle()           Interior angle measure of a regular n-gon
            numlen()          How many digits are in a number

        Tests

            is_even()         Test if a number is even
            is_prime()        Test if a number is prime
            is_divisible()    Test if x is divisible by y
            is_square()       Test if a number is a perfect square


    Classes&methods

        rectangle()            Make a rectangle
            .area()            Find the area
            .perimeter()       Find the perimeter
            .scale()           Rescale the rectangle
            .diagonal()        Find the diagonal length
            .info()            Displays information about a rectangle.

        square()               Make a square
            All methods
            inherited from
            rectangle

        st_quadrat()           Solve a quadratic equation fron standard form
            .is_real()         Test if the equation has real roots
            .calcz()           Calculate the zeros of the equation
            .calcall()         Calculate lots of information about the given quadratic
            .info()            Displays the information from .calcall()
            .solve()           Given x, calculate the y value along the given quadratic

        vf_quadrat()           Solve a quadrat from vertex form
            All methods
            inherited from
            st_quadrat

        circle_equ()           Solve a circle from general form
            .solve()           Solve for a y value from a given x
            .calcall()         Calculate general information about the circle

        circle_points          Solve a circle from 2 coordinate pairs
            All methods
            inherited from
            circle_equ
'''
from __future__ import print_function

__all__ = []
__author__ = '671620616'
__version__ = '0.8'

import sys
has_sympy = 'sympy' in sys.modules
del sys

import math as m
import cmath as cm
import fractions as fr
if has_sympy:
	from sympy import sin, asin, sinh, cos, acos, cosh, tan, atan, tanh, sqrt
else:
	from math import sin, asin, sinh, cos, acos, cosh, tan, atan, tanh, sqrt
pi_acc = 3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006
e_acc = 2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427427466391932003059921817413596629043572900334295260595630738132328627943490763233829880753195251019011573834187930702154089149934884167509244761460668082264800168477411853742345442437107539077744992069551702761
pi_str = '3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006'
e_str = '2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427427466391932003059921817413596629043572900334295260595630738132328627943490763233829880753195251019011573834187930702154089149934884167509244761460668082264800168477411853742345442437107539077744992069551702761'

def fibo(n):
	'''Lists the first n numbers of the fibonacci sequence.\nARGS: ({n})'''
	fseq = []
	a = 0
	b = 1
	n1 = 0
	while n1 < n:
		fseq.append(a)
		a, b = b, a + b
		n1 += 1
	return fseq
__all__.append('fibo')

def tri(n):
	'''List the first n numbers of the triangular numbers.\nARGS: ({n})'''
	seq = []
	n1 = 0
	while n1 < n:
		i = (n1*(n1 + 1)) / 2
		seq.append(i)
		n1 += 1
	return seq
__all__.append('tri')

def tetra(n):
	'''List the first n numbers of the tetrahedral sequence.\nARGS: ({n})'''
	seq = []
	n1 = 0
	while n1 < n:
		i = (n1*(n1 + 1)*(n1 + 2)) / 6
		seq.append(i)
		n1 += 1
	return seq
__all__.append('tetra')

def hexagonal(n):
	'''List the first n numbers of the hexagonal sequence.\nARGS: ({n})'''
	seq = []
	n1 = 0
	while n1 < n:
		i = 2*n1**2 - n1
		seq.append(i)
		n1 += 1
	return seq
__all__.append('hexagonal')

def pentatope(n):
	'''List the first n numbers of the pentatope sequence.\nARGS: ({n})'''
	seq = []
	n1 = 0
	while n1 < n:
		i = (n1*(n1 + 1)*(n1 + 2)*(n1 + 3)) / 24
		seq.append(i)
		n1 += 1
	return seq
__all__.append('pentatope')

def catalan(n):
	'''List the first n numbers of the catalan sequence.\nARGS: ({n})'''
	seq = []
	n1 = 1 # start at 1 for this sequence
	while n1 < n:
		i = factorial(2*n1) / ( factorial(n1 + 1) * factorial(n1) )
		seq.append(i)
		n1 += 1
	return seq
__all__.append('catalan')

def egypt(n,d):
	'''Egyptian fractions.\nARGS: ({numerator},{denominator})'''
	f = fr.Fraction(n,d)
	e = int(f)
	f -= e
	parts = [e]
	while(f.numerator>1):
		e = fr.Fraction(1, int(m.ceil(1/f)))
		parts.append(e)
		f -= e
	parts.append(f)
	return parts
__all__.append('egypt')

def is_even(n):
	'''Returns True if n is even, False if n is odd.\nARGS: ({number to test})'''
	return not n%2
__all__.append('is_even')

def is_prime(n):
	'''Tests if a number is prime.\nARGS: ({number to be tested})'''
	tf = []
	for i in range(2,n-1):
		if n % i == 0:
			tf.append('y')
		else:
			tf.append('n')
	if 'y' in tf:
		return False
	else:
		return True
__all__.append('is_prime')

def is_square(n):
	"""Whether or not n is a square number, or perfect square.\nARGS: ({n})"""
	if not has_sympy:
		return isinstance(sqrt(n), int)
	return sqrt(n).evalf() == int(m.sqrt(n))
__all__.append('is_square')

def is_divisible(n,d):
	'''Tests if a number is divisible by another.\nARGX: ({is this number},{divisible by this})'''
	return not n%d
__all__.append('is_divisible')

def root(x,y):
	'''Takes the nth root of a number\nARGS: ({number to be rooted},{root})'''
	return pow(x, fr.Fraction(1,y))
__all__.append('root')

def frac_root(x,n,d):
	'''Takes a fractional root of a number.\nARGS: ({number to be rooted},{root numerator},{root denominator})'''
	degree = fr.Fraction(n,d)
	ans = pow(x,degree)
	return ans
__all__.append('frac_root')

def avg(x):
	'''Averages a list of numbers.\nARGS: ({list of numbers})'''
	total = 0
	for i in x:
		i = float(i)
		total += i
	ans = total / len(x)
	return ans
__all__.append('avg')

def ack(m, n):
	'''Ackermann function for m and n.\nARGS: ({m}, {n})
	
	/ n + 1                  m = 0
	A(m, n) = | A(m - 1, 1)            m > 0 and n = 0
	\ A(m - 1, A(m, n - 1))  m > 0 and n > 0'''
	if m == 0:
		return n + 1
	elif m > 0 and n == 0:
		return ack(m-1, 1)
	elif m > 0 and n > 0:
		return ack(m-1, ack(m, n-1))
__all__.append('ack')

def is_square(n,acc=1):
	'''Tests if a number is a perfect square.\nARGS: ({number to test})'''
	allowed = range(acc)
	found = 0
	step = 1
	while found == 0:
		if n - step**2 in allowed:
			return True
			found = 1
		elif step < n:
			found = 0
			step += 1
		else:
			return False
			found = 1
__all__.append('is_square')

def factors(n):
	'''Returns a list of factors for a number.\nARGS: ({number to factor})'''
	top_list = []
	for i in range(1,n-(n/2)):
		if is_prime(n):
			return "Prime"
			break
		if n % i == 0:
			factor_set = [i, n/i]
			factor_set.reverse()
			if factor_set not in top_list:
				if i**2 == n and m.sqrt(n) == i:
					top_list.append('{}^2'.format(i))
				else:
					factor_set.reverse()
					top_list.append(factor_set)
			else:
				pass
		else:
			pass
	return top_list
__all__.append('factors')

def numlen(n):
	'''Return the length of number n.  eg- 500 -> 3 2 -> 1\nARGS: ({n})'''
	return len(str(n))
__all__.append('numlen')

def diag(sides):
	'''How many diagonals are in a polygon with n sides.\nARGS: ({number of sides})'''
	return (sides**2 - 3*sides) / 2
__all__.append('diag')

def angle(sides):
	'''How many degrees are in a polygon with n sides.\nARGS: ({number of sides})'''
	return (sides-2) * 180
__all__.append('angle')

def dist(c1,c2):
	'''Find the distance between two given coordinates.\nARGS: ({coord 1},{coord 2})'''
	if c1[1] == c2[1]:
		return abs(c2[1] - c1[1])
	elif c1[0] == c2[0]:
		return abs(c2[0] - c1[0])
	else:
		dx = abs(c2[0] - c1[0])
		dy = abs(c2[1] - c1[1])
		d = m.sqrt(dx**2 + dy**2)
		return d
__all__.append('dist')

def midpoint(c1,c2):
	'''Give the midpoint between two coordinates.\nARGS: ({coord 1},{coord 2})'''
	if c1[1] == c2[1]:
		d = abs(c2[1] - c1[1])
		return (c1[0], d/2.)
	else:
		x = (c2[0] - c1[0]) / 2.
		y = (c2[1] - c1[1]) / 2.
		return (x, y)
__all__.append('midpoint')

def factorial(n):
	'''Take the factorial of n.\nARGS: ({n})'''
	n1 = f = 1
	while n1 <= n:
		f *= n1; n1 += 1
	return f
__all__.append('factorial')

def summation(f, stop, start=0):
	'''N-ary summation.\nARGS: ({f}, {n}, [start])
	:param f: can be func, str or number.'''
	sum = start
	def sample_func(): pass
	sample_str = " "
	for i in xrange(start, stop):
		if type(f) == type(sample_func):
			sum += f(i)
		elif type(f) == type(sample_str):
			exec "sum += {}".format(f)
		elif type(f) in (type(1), type(2.5)):
			sum += f
	return sum
__all__.append('summation')

def foil(l, r):
	"""Given two tuples (a, b) and (c, d) return (a + b) * (c + d)."""
	return l[0]*r[0] + l[0]*r[1] + l[1]*r[0] + l[1]*r[1]
__all__.append('foil')

def sin2(th):
	"""sin^2(theta) for given theta.\nARGS: ({theta})"""
	return 0.5 - (0.5*cos(2*th))
__all__.append('sin2')

def cos2(th):
	"""cos^2(theta) for a given theta.\nARGS: ({theta})"""
	return 0.5 + (0.5*cos(2*th))
__all__.append('cos2')

def cot(th):
	"""Cotangent of a given number.\nARGS: ({theta})"""
	return -sin(2*th) / cos(2*th) - 1
__all__.append('cot')

def acot(th):
	"""Arc cotangent of a given number.\nARGS: ({theta})"""
	return atan(1/th)
__all__.append('acot')

def sec(th):
	"""Secant of a given number.\nARGS: ({theta})"""
	return (2*cos(th)) / (cos(2*th) + 1)
__all__.append('sec')

def asec(th):
	"""Arc secant of a given number.\nARGS: ({theta})"""
	return acos(1/th)
__all__.append('asec')

def csc(th):
	"""Cosecant of a given number.\nARGS: ({theta})"""
	return -(2*sin(th)) / (cos(2*th) - 1)
__all__.append('csc')

def exsec(th):
	"""Exsecant of a given number.\nARGS: ({theta})"""
	return (1 - cos(th)) * sec(th)
__all__.append('exsec')

def excsc(th):
	"""Excosecant of a given number.\nARGS: ({theta})"""
	return (1 - sin(th)) * csc(th)
__all__.append('excsc')

def versin(th):
	"""Versed sine of a given number.\nARGS: ({theta})"""
	return 1 - cos(th)
__all__.append('versin')

def cvs(th):
	"""Coversin of a given number.\nARGS: ({theta})"""
	try:
		from sympy import pi
	except ImportError:
		from math import pi
	return 2 * sin2( (pi/4) - (th/2) )
__all__.append('cvs')

class rectangle (object):
	'''Makes a rectangle of specified dimensions.\nARGS: ({width},{height})'''
	def __init__(self,w,h):
		self.w = float(w)
		self.h = float(h)
		
	def area(self):
		'''Calculates the area of a rectangle.'''
		self.area = self.w * self.h
		return self.area
		
	def perimeter(self):
		'''Calculates the perimeter of a rectangle'''
		self.perimeter = (2 * self.w) + (2 * self.h)
		return self.perimeter
		
	def scale(self, factor):
		'''Rescales the rectangle by a certain amount,\nARGS: ({rescale factor})'''
		self.w = self.w * factor
		self.h = self.h * factor
		
	def diagonal(self):
		'''Calculates the diagonal length of a shape.'''
		self.diag_len = m.sqrt(self.w**2 + self.h**2)
		return self.diag_len
		
	def info(self):
		'''Prints basic info about a shape.'''
		area = self.area()
		perimeter = self.perimeter()
		print("Width: {}\nHeight: {}\nArea: {}\nPerimeter: {}".format(self.w, self.h, area, perimeter))
__all__.append('rectangle')


class square (rectangle):
	'''Makes a square of a certain length.\nARGS: ({length of square})'''
	def __init__(self,w):
		self.w = w
		self.h = w
__all__.append('square')


class st_quadrat (object):
	'''Quadratic solver.  Takes in a standard form quadratic.\nARGS: ({a},{b},{c}'''
	def __init__(self,a,b,c):
		self.a = float(a)
		self.b = float(b)
		self.c = float(c)
		self.format = "ax^2+bx+c"
		
	def is_real(self):
		'''Tests whether the quadratic has real roots.'''
		self.discrim = self.b**2 - 4 * self.a * self.c
		if self.discrim == 0:
			self.numz = 1
		elif self.discrim > 0:
			self.numz = 2
		elif self.discrim < 0:
			self.numz = -2
		return self.numz
		
	def calcz(self):
		'''Calculate the zeroes of a quadratic.'''
		self.is_real()
		a = self.a
		b = self.b
		c = self.c
		self.zeroes = []
		if self.numz == 1:
			z = (-b + m.sqrt(b**2-4*a*c))/(2*a)
			self.zeroes += z
		elif self.numz == 2:
			z1 = (-b + m.sqrt(b**2-4*a*c))/(2*a)
			z2 = (-b - m.sqrt(b**2-4*a*c))/(2*a)
			self.zeroes += z1,z2
		elif self.numz == -2:
			z1 = (-b + m.sqrt(-(b**2-4*a*c)))/(2*a)
			z2 = (-b - m.sqrt(-(b**2-4*a*c)))/(2*a)
			self.zeroes += z1,z2
			
	def calcall(self):
		'''Calculate lots of information about a quadratic'''
		a = self.a
		b = self.b
		c = self.c
		self.calcz()
		self.aos = aos = -(b / (2 * a))
		self.expr = "{}x^2 + {}x + {}".format(a,b,c)
		self.vertex = (aos, a*aos**2 + b*aos + c)
		self.h = b / -2
		self.k = b*aos + c
		self.vexpr = "{}(x - {})^2 + {}".format(a,self.h,self.k)
		
	def info(self):
		'''Display information about a quadratic'''
		self.calcall()
		print(self.expr)
		print(self.vexpr)
		print("Vertex: ({}, {})".format(self.vertex[0],self.vertex[1]))
		if self.numz == 1:
			print("One zero at: ({}, 0)".format(self.zeroes[0]))
		elif self.numz == 2:
			print("Two zeroes at: \n({}, 0), \n({}, 0)".format(self.zeroes[0], self.zeroes[1]))
		elif self.numz == -2:
			print("Two nonreal zeroes at: \n({}i, 0), \n({}i, 0)".format(self.zeroes[0], self.zeroes[1]))
		print("Axis of symmetry: {}".format(self.aos))
		
		
	def solve(self,x):
		'''Solves the quadratic for a value.\nARGS: ({x value})'''
		a = self.a
		b = self.b
		c = self.c
		y = a*x**2 + b*x + c
		return y
__all__.append('st_quadrat')

class vf_quadrat(st_quadrat):
	'''Quadratic module.  Takes in a vertex for quadratic.\nARGS: ({a},{h},{k})'''
	def __init__(self,a,h,k):
		self.format = "a(x-h)+k"
		self.a = float(a)
		self.b = float(-2 * h)
		self.c = float(k + h**2)
__all__.append('vf_quadrat')


class circle_equ (object):
	'''Solves a circle from an equation.\nARGS: ({r^2},{h},{k})'''
	def __init__(self,r2,h,k):
		self.r2 = r2
		self.h = h
		self.k = k
		self.mode = 'from equ'
		
	def solve(self,x):
		'''Solves a circle for a certain value'''
		r2 = self.r2
		h = self.h
		k = self.k
		r = sqrt(r2)
		sols = [k - sqrt((-h + r + x)*(h + r - x)), k + sqrt((-h + r + x)*(h + r - x))]
		return sols
		
	def calcall(self):
		'''Calculates general information about the circle.'''
		self.r = m.sqrt(self.r2)
		self.d = 2 * self.r
		self.c = pi * self.d
		self.a = pi * self.r2
__all__.append('circle_equ')


class circle_points (circle_equ):
	def __init__(self,p1x,p2x,p1y,p2y):
		self.p1x = float(p1x)
		self.p2x = float(p2x)
		self.p1y = float(p1y)
		self.p2y = float(p2y)
		self.mode = 'from points'
		d = m.sqrt((p2x-p1x)**2 + (p2y-p1y)**2)
		r = d/2
		self.r2 = r**2
		self.h = avg([p1x,p2x])
		self.k = avg([p1y,p2y])
__all__.append('circle_points')

