# coding: utf-8
from __future__ import print_function
from struct import unpack
import math, Image, ImageDraw, ui, scene, sys, sqlite3
from timeit import default_timer as timer
from StringIO import StringIO

class ShapeRender(object):
	def __init__(self, config):
		#start = timer()
		self.shape_type_def = {0: 'Null Shape',1: 'Point', 3: 'PolyLine', 5: 'Polygon', 8: 'MultiPoint', 11: 'PointZ', 13: 'PolyLineZ', 15: 'PolygonZ', 18: 'MultiPointZ', 21: 'PointM', 23: 'PolyLineM', 25: 'PolygonM', 28: 'MultiPointM', 31: 'MultiPatch'}
		
		#create an image depending on the screen size
		#scr = ui.get_screen_size() * scene.get_screen_scale()
		#self.scr_width = scr[0]
		#self.scr_height = scr[1] - 64.0    #title bar = 64px
		self.scr_width = config[0]
		self.scr_height = config[1]
		self.sqlcon = None
		self.sqlcur = None
		
		self.read_db()
		xmin = config[2]
		ymin = config[3]
		xmax = config[4]
		ymax = config[5]
		self.xoffset = 180.0
		self.yoffset = 90.0
		if xmin < 0 and xmax > 0:
			self.xdelta = abs(xmax) + abs(xmin)
		elif xmin < 0 and xmax < 0:
			self.xdelta = abs(xmin) - abs(xmax)
		else:
			self.xdelta = abs(xmax) - abs(xmin)
		if ymin < 0 and ymax > 0:
			self.ydelta = abs(ymax) + abs(ymin)
		elif ymin < 0 and ymax < 0:
			self.ydelta = abs(ymin) - abs(ymax)
		else:
			self.ydelta = abs(ymax) - abs(ymin)
		print(str(self.xdelta) + ' / ' + str(self.ydelta))
		self.imagebuffer = None
		self.drawbuffer = None
		self.linewidth = config[6]
		self.dotsize = config[7]
		self.bgcolor = config[8]
		self.color = None
		
		self.pixel = self.scr_width / self.xdelta
		print('pixel = ' + str(self.pixel))
		img_height = self.scr_width / (self.xdelta / self.ydelta)
		self.imagebuffer = Image.new('RGBA', (int(self.scr_width),int(img_height)), self.bgcolor)
		self.drawbuffer = ImageDraw.Draw(self.imagebuffer)
		if xmin != -180.0:
			self.xoffset = xmin * -1
		print('xoffset = ' + str(self.xoffset))
		if ymin != -90.0:
			self.yoffset = ymax
		print('yoffset = ' + str(self.yoffset))
		for i in range(9, len(config), 2):
			self.color = config[i]
			self.read_data(config[i+1])
			
		self.imagebuffer.show()
		#end = timer()
		#print 'time for select: ' + str(end-start)
		
	def read_data(self, shapefile):
		cursor = self.sqlcur.execute("SELECT ID_Shape FROM Shapes WHERE Name = ?", (shapefile,))
		id_shape = cursor.fetchone()
		if len(id_shape) > 0:
			print('Shape ID = ' + str(id_shape[0]))
		else:
			print('No id_shape')
			return
			
		cursor = self.sqlcur.execute("SELECT ID_Poly FROM Polys WHERE ID_Shape = ?",id_shape)
		id_poly = cursor.fetchall()
		min_id_poly = min(id_poly)[0]
		max_id_poly = max(id_poly)[0]
		print('Poly IDs = ' + str(min_id_poly) + ' - ' + str(max_id_poly))
		
		cursor = self.sqlcur.execute("SELECT ShapeType FROM Polys WHERE ID_Shape = ?",id_shape)
		shape_type = cursor.fetchone()[0]
		print('ShapeType = ' + str(shape_type))
		
		cursor = self.sqlcur.execute("SELECT ID_Poly, ID_Point, X, Y FROM Points WHERE ID_Poly >= ? AND ID_Poly <= ? ORDER BY ID_Poly, ID_Point", (min_id_poly, max_id_poly))
		points = cursor.fetchall()
		print('length points: ' + str(len(points)))
		
		id_poly = min_id_poly
		drawpoints = []
		for j in xrange(len(points)):
			if points[j][0] == id_poly:
				x = (points[j][2] + self.xoffset) * self.pixel
				y = ((points[j][3] - self.yoffset) * -1) * self.pixel
				if self.shape_type_def[shape_type] == 'Point':
					self.drawbuffer.ellipse((x - self.dotsize, y - self.dotsize, x + self.dotsize, y + self.dotsize), fill=self.color)
				else:
					drawpoints.append((x, y))
			else:
				if self.shape_type_def[shape_type] == 'PolyLine':
					self.drawbuffer.line(drawpoints, fill=self.color, width=self.linewidth)
				elif self.shape_type_def[shape_type] == 'Polygon':
					self.drawbuffer.polygon(drawpoints, fill=self.color)
				else:
					print('ShapeType ' + str(shape_type) + ' is not supported.')
					break
				id_poly += 1
				drawpoints = []
				x = (points[j][2] + self.xoffset) * self.pixel
				y = ((points[j][3] - self.yoffset) * -1) * self.pixel
				drawpoints.append((x, y))
			if j == len(points) - 1:
				if self.shape_type_def[shape_type] == 'PolyLine':
					self.drawbuffer.line(drawpoints, fill=self.color, width=self.linewidth)
				elif self.shape_type_def[shape_type] == 'Polygon':
					self.drawbuffer.polygon(drawpoints, fill=self.color)
					
	def read_db(self):
		self.sqlcon = sqlite3.connect('earth.db')
		self.sqlcur = self.sqlcon.cursor()
		
		cursor = self.sqlcur.execute("SELECT Name FROM Shapes")
		shapes = cursor.fetchall()
		if len(shapes) > 0:
			print(shapes)
		else:
			print('No shapes')
			
if __name__ == '__main__':
	config1 = []
	config1.append(3840)    #[0] image width
	config1.append(2160)    #[1] image height (height will be adjusted)
	#whole world
	config1.append(-180.0)    #[2] xmin (smallest longitude)
	config1.append(-90.0)    #[3] ymin (smallest latitude)
	config1.append(180.0)    #[4] xmax (biggest longitude)
	config1.append(90.0)    #[5] ymax (biggest latitude)
	config1.append(1)    #[6] linewidth
	config1.append(5)    #[7] dotsize
	config1.append('lightblue')  #[8] image background color
	config1.append('brown')    #[9] color for first shape
	config1.append('ne_50m_land') #[10] first shape
	#config[0] - config[10] is mandatory
	
	config2 = []
	config2.append(3840)    #[0] image width
	config2.append(2160)    #[1] image height (height will be adjusted)
	#USA
	config2.append(-129.8)    #[2] xmin (smallest longitude)
	config2.append(22.7)    #[3] ymin (smallest latitude)
	config2.append(-63.5)    #[4] xmax (biggest longitude)
	config2.append(49.7)    #[5] ymax (biggest latitude)
	config2.append(1)    #[6] linewidth
	config2.append(5)    #[7] dotsize
	config2.append('white')  #[8] image background color
	config2.append('black')    #[9] color for first shape
	config2.append('ne_50m_coastline') #[10] first shape
	config2.append('lightgreen')    #[11] color
	config2.append('ne_50m_urban_areas') #[12] shape
	config2.append('lightblue')    #[13] color
	config2.append('ne_50m_lakes') #[14] shape
	config2.append('red')    #[15] color
	config2.append('ne_50m_populated_places_simple') #[16] shape
	
	config3 = []
	config3.append(3840)    #[0] image width
	config3.append(2160)    #[1] image height (height will be adjusted)
	#Europe
	config3.append(-15.4)    #[2] xmin (smallest longitude)
	config3.append(35.0)    #[3] ymin (smallest latitude)
	config3.append(37.5)    #[4] xmax (biggest longitude)
	config3.append(72.0)    #[5] ymax (biggest latitude)
	config3.append(2)    #[6] linewidth
	config3.append(5)    #[7] dotsize
	config3.append('white')  #[8] image background color
	config3.append('black')    #[9] color for first shape
	config3.append('ne_50m_coastline') #[10] first shape
	config3.append('red')    #[11] color
	config3.append('ne_50m_admin_0_boundary_lines_land') #[12] shape
	
	ShapeRender(config1)

