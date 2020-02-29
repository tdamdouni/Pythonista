# coding: utf-8

# https://gist.github.com/PKHG/4039885

from __future__ import print_function
from scene import *
#from random import random
from time import ctime
from os import listdir, path, stat
from os.path import isdir, isfile, sep, abspath
interesting_dirs = {0:'.', 1:'/',2:'/Applications',3: '/Applications/Maps.app'}
#t=  '/Applications/Maps.app/Japanese.lproj/Localizable.strings'

def dir_contents(path):
	"""get all dirs and files from path"""
	try:
		contents = listdir(path)
	except:
		print('***ERROR with ', path)
		sys.exit()
#	print(contents)
#	tmp = [isfile(path + "\\" + el) for el in contents]
#	print(tmp)
	files = []
	folders = []
	for i, item in enumerate(contents):
		if isfile(path+sep+contents[i]):
			files += [item]
		elif isdir(path+sep+contents[i]):
			folders += [item]
	return files, folders

def prepare_all_data(dir_path, st):
	""" returns a dictionary with (img,size), nr of dirs, nr of files, """
	files, folders = dir_contents(dir_path)
	info = {}
	counter = 0
	all_names = {}
	if folders:
		#directories get Dir: prefixed ;-)
		for el in folders:
			img, size = render_text('Dir:' + el, font_size = 30)
			info[counter] = (img, size)
			all_names[img] = dir_path + sep + el
			counter += 1
	nr_dirs = counter			
	if files:
		for el in files:
			img, size = render_text(el, font_size = 30)
			info[counter] = (img, size)
			all_names[img]= dir_path + sep + el
			counter += 1
	nr_files = counter - nr_dirs
	dir_name_layers = []
	for i in range(counter):
		take = i % st
		lay = new_txt_layer(i, info, take * 35)
		lay.stroke_weight = 1
		if i < nr_dirs:
			#lay.stroke_weight = 1
			lay.stroke = Color(1,0,0)
		dir_name_layers.append(lay)
	return dir_name_layers, nr_dirs, nr_files, all_names

def range_split(total, st):
	nst = total / st
	nst_rest = total % st
	result = [range(i * st,i * st + st) for i in range(nst)]
	if nst_rest:
		result.append(range(st * nst, total))
	return result

def new_txt_layer(nr, alldata, where):
	img, size = alldata[nr]
	lay = Layer(Rect(10, where, size.w, size.h + 5))
	lay.image = img
	return lay

def m_one_txt_layer(txt,x,y, col= Color(1,0,0), extra = 0):#strw = 0):
	img, size = render_text(txt, font_size = 30)
	lay = Layer(Rect(x, y, size.w, size.h + extra))
	lay.image = img
	lay.background = col
	#if strw > 0 :
		#lay.stroke_width = strw
	return lay



class MyScene (Scene):

	def change_dir_to(self,td):
		self.dir_name_layers, self.nr_dirs, self.nr_files, self.all_names = prepare_all_data(td, self.st)
		#print self.nr_dirs, self.nr_files
		self.total = len(self.dir_name_layers)
		if not self.total:
			print('***IMPOSSIBLE TD =', td)
			sys.exit(1)
		print('***DBG CHANGE_DIR_TO TOTAL = ', self.total)
		#list of ranges to do			
		self.my_ranges = range_split(self.total, 18)
		#print self.my_ranges
		self.nr_ranges = len(self.my_ranges)
		#if something went wrong, an error is printed in the console
		#otherwise take the firs possibility of items:
		for el in self.my_ranges[0]:
			self.root.add_layer(self.dir_name_layers[el])
		#used_range is a counter used to implement
		#the NEXT button action
		self.used_range = 0
		self.is_DIR = False
		self.nr_menus = 7

	def make_menu(self):
		#a menu always to be  printed at lower left of the screen
		self.Next = m_one_txt_layer('Next	   ', 750,10)
		self.Next.stroke = Color(0,0,1)
		self.root.add_layer(self.Next)
		self.zero = m_one_txt_layer(' 0 ' +  interesting_dirs[0] + ' start pythonista',750, 50\
									,Color(0,0,1))
		self.root.add_layer(self.zero)
		self.one = m_one_txt_layer(' 1 ' + interesting_dirs[1] + ' start Ipad', 750, 100, Color(0,1,0))
		self.root.add_layer(self.one)
		self.two = m_one_txt_layer(' 2 ' + interesting_dirs[2], 750 ,150, Color(0,1,1))
		self.root.add_layer(self.two)
		self.rotate = m_one_txt_layer(' ROTATE down', 750, 200, Color(.5, .5, 0), 20)
		self.root.add_layer(self.rotate)
		self.new_dir = m_one_txt_layer(' this DIR   ', 750, 260, Color(.5,.5,.5),10)
		self.root.add_layer(self.new_dir)
		self.txt_file = m_one_txt_layer(' text to console', 750, 320, Color(0,0.5,1),10)
		self.root.add_layer(self.txt_file)
		self.nr_menus = 7 

	def setup(self):
		self.all_names = []
		# This will be called before the first frame is drawn.
		# Set up the root layer and one other layer:
		self.root = Layer(self.bounds)
		td = interesting_dirs[1]
		#some possibilities for direct change:
		#td = '/Applications/Maps.app'
		#td = '/Applicatios/Utilities'
		#td = '/Applications/Maps.app/Japanese.lproj'
		self.st = 18 #number of max antal names in root
		self.change_dir_to(td)
		self.nr_menus = 5 #will be overwritten by make_menu
		self.make_menu()
		self.is_DIR = False

	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0, 0, 0)
		self.root.update(self.dt)
		self.root.draw()

	def add_menu(self):
		#because of deleting evt. all layers this is easily painted again
		self.root.add_layer(self.Next)
		self.root.add_layer(self.zero)
		self.root.add_layer(self.one)
		self.root.add_layer(self.two)
		self.root.add_layer(self.rotate)
		self.root.add_layer(self.new_dir)
		self.root.add_layer(self.txt_file)


	def touch_began(self, touch):
		def which_item():
			result = None
			self.is_DIR = ''
			#PKHG.dbg print len(self.root.sublayers),self.my_ranges[self.used_range]
			for el in self.my_ranges[self.used_range]:
				el = el % self.st
				if touch.location in self.root.sublayers[el].frame: 
					self.is_DIR = self.root.sublayers[el]
					self.is_DIR.stroke == Color(1,0,0)
					#self.new_dir.stroke = Color(0,1,0)
					print('I am ', self.is_DIR)
					self.root.sublayers[el].stroke = Color(1,1,1)
					#print 'found ',el
					result = self.all_names[self.root.sublayers[el].image]
					self.is_DIR = result
			return result

		def show_next():
			if self.nr_ranges > 0:
				self.root.sublayers = []
				self.used_range = (self.used_range + 1) % self.nr_ranges
				for el in self.my_ranges[self.used_range]:
					self.root.add_layer(self.dir_name_layers[el])

		def rotate_down():
			#the relvant frames are moved below
			#the lowest on goes to the top
			nsublayers = []
			el0 = self.root.sublayers.pop(0) #this is the lowest one
			for lay in self.root.sublayers[:(- self.nr_menus)]:
				#lay's frame has to be adjusted, not chaning the img!
				r,img,stcol,str= lay.frame,lay.image,lay.stroke,lay.stroke_weight
				nr = Rect(r.x, r.y -35, r.w, r.h)
				nl = Layer(nr)
				nl.stroke_weight = str
				nl.stroke = stcol
				nl.image = img
				nsublayers.append(nl)
			r = el0.frame
			img = el0.image
			strcol= el0.stroke
			strw = el0.stroke_weight
			nr = Rect(r.x, 35 *(1 + len(nsublayers)),r.w,r.h)
			nl = Layer(nr)
			nl.image = img
			nl.stroke = strcol
			nl.stroke_weight = strw
			nsublayers.append(nl)
			self.root.sublayers = nsublayers
		#print touch.location
		go_on = True
		#Check where a touch is done!
		if touch.location in self.Next.frame:
			#self.root.sublayers = []
			show_next()
		elif touch.location in self.zero.frame:
			self.root.sublayers = []
			self.td = 0
			#ok print 'td now', self.td
			dir_ch = interesting_dirs[self.td]
			self.change_dir_to(dir_ch)
		elif touch.location in self.one.frame:
			self.root.sublayers = []
			self.td = 1
			dir_ch = interesting_dirs[self.td]
			self.change_dir_to(dir_ch)
		elif touch.location in self.two.frame:
			self.root.sublayers = []
			self.td = 2
			dir_ch = interesting_dirs[self.td]
			self.change_dir_to(dir_ch)
		elif touch.location in self.rotate.frame:		
			rotate_down()
		elif touch.location in self.new_dir.frame:
			if self.is_DIR:
				if path.isdir(self.is_DIR):
					print('new_dir ==>', self.is_DIR)
					self.root.sublayers = []
					self.change_dir_to(self.is_DIR)
				else:
					print('***INFO ', self.is_DIR, ' is not a directory!')
			else:
				print('***ERROR no dir chosen')
		elif touch.location in self.txt_file.frame:
			if self.is_DIR:
				if path.isfile(self.is_DIR):
					fd = open(self.is_DIR)
					try:
						for line in fd:
							print(line)
					finally:
						fd.close()
		elif touch.location.x < 600:
			#print 'item at' , touch.location
			res = which_item()
			print(res)
			if res:
				stat_info = stat(res)
				print('ctime= ', ctime(stat_info.st_ctime))
				#print 'atime= ', ctime(stat_info.st_atime)
				print('size =', int(stat_info.st_size), ' bytes')
		else:
			go_on = False 
		if go_on:
			self.add_menu()
		else:
			pass
			#sys.exit()

	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		#self.root.sublayers=[]
		#self.root.remove_layer(self.my_Layers[1])
		pass

run(MyScene())