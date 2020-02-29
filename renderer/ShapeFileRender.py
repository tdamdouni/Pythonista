# coding: utf-8

# https://github.com/humberry/ShapeFileRender

# Create an image from shape file(s). I recommend small files, because of the limited power. Suitable files (.shp) you can find http://www.naturalearthdata.com/downloads/110m-physical-vectors/

# At the moment only polylines (Number of Parts = 1 & Index = 0) and polygons are supported.

from __future__ import print_function
from struct import unpack
import math, Image, ImageDraw, ui, scene, sys

class ShapeFileRender(object):
	def __init__(self, config):
		self.shape_type_def = {0: 'Null Shape',1: 'Point', 3: 'PolyLine', 5: 'Polygon', 8: 'MultiPoint', 11: 'PointZ', 13: 'PolyLineZ', 15: 'PolygonZ', 18: 'MultiPointZ', 21: 'PointM', 23: 'PolyLineM', 25: 'PolygonM', 28: 'MultiPointM', 31: 'MultiPatch'}
		
		#create an image depending on the screen size
		scr = ui.get_screen_size() * scene.get_screen_scale()
		self.scr_width = scr[0]
		self.scr_height = scr[1] - 64.0    #title bar = 64px
		
		if len(config) < 5:
			print('Error: You need at least 5 parameter (xdelta, ydelta, background color, shape file, shape color)')
			sys.exit()
			
		self.xdelta = config[0]
		self.ydelta = config[1]
		self.bgcolor = config[2]
		self.pixel = 0
		self.imagebuffer = None
		self.drawbuffer = None
		self.linewidth = 1
		
		self.data = []
		
		for i in range(3, len(config), 2):
			self.read_file(config[i])
			self.color = config[i+1]
			self.convert_data(config[i])
			
		self.imagebuffer.show()
		
	def get_record_header(self, header_bytes):
		header = []    #whole header, depending on shape_tape
		shape_type = unpack('<i', ''.join(header_bytes[0:4]))[0]
		header.append(shape_type)
		if self.shape_type_def[shape_type] == 'Null Shape':
			return header
		elif self.shape_type_def[shape_type] == 'PolyLine' or self.shape_type_def[shape_type] == 'Polygon':
			for i in range(4):
				header.append(unpack('<d', ''.join(header_bytes[i*8+4:i*8+12]))[0])    #bounding_box
			header.append(unpack('<i', ''.join(header_bytes[36:40]))[0])    #NumParts
			header.append(unpack('<i', ''.join(header_bytes[40:44]))[0])    #NumPoints
			numParts = header[5]
			if numParts > 1:
				for i in range(0, numParts):
					header.append(unpack('<i', ''.join(header_bytes[i*4+44:i*4+48]))[0])    #Parts
			else:
				header.append(unpack('<i', ''.join(header_bytes[44:48]))[0])    #Parts
			return header
		else:
			return None
			
	def get_polyline(self, data):
		header = self.get_record_header(data[0:48])
		points = []
		for i in range(header[6]*2):
			pt = unpack('<d', ''.join(data[i*8+48:i*8+56]))[0]
			if (i & 0x1) == 0:    #even = longitude = x
				pt = (pt + 180) * self.pixel
			else:                #odd = latitude = y
				pt = ((pt - 90) * -1) * self.pixel
			points.append(pt)
		self.draw_polyline(points)
		
	def get_polygon(self, data):
		header = self.get_record_header(data)
		points = []
		if header[5] > 1:
			h_length = len(header)
			h_length = (h_length - 4) * 4 + 32
			header.append(header[6])    #last index
			for j in range(0, header[5]):    #amount of rings
				points = []
				for i in range(header[j+7]*2,header[j+8]*2):    #start/stop index
					pt = unpack('<d', ''.join(data[(i*8)+h_length:(i*8)+h_length+8]))[0]
					if (i & 0x1) == 0:    #even = longitude = x
						pt = (pt + 180) * self.pixel
					else:                #odd = latitude = y
						pt = ((pt - 90) * -1) * self.pixel
					points.append(pt)
				self.draw_polygon(points)
		else:
			for i in range(header[6]*2):
				pt = unpack('<d', ''.join(data[i*8+48:i*8+56]))[0]
				if (i & 0x1) == 0:    #even = longitude = x
					pt = (pt + 180) * self.pixel
				else:                #odd = latitude = y
					pt = ((pt - 90) * -1) * self.pixel
				points.append(pt)
			self.draw_polygon(points)
			
	def draw_polygon(self, points):
		for j in range(0, len(points)):
			self.drawbuffer.polygon(points, fill=self.color)
			
	def draw_polyline(self, points):
		for j in range(0, len(points)):
			self.drawbuffer.line(points, fill=self.color, width=self.linewidth)
			
	def read_file(self, file):
		f = open(file, 'rb')
		self.data = f.read() #read all
		f.close()
		
	def convert_data(self, filename):
		verbose = 'HEADER of ' + filename + ':\n'
		file_code = unpack('>i', ''.join(self.data[0:4]))[0]    #4byte integer big endian
		if file_code != 9994:
			print('sorry, no shape file - ' + filename)
			sys.exit()
		file_length = unpack('>i', ''.join(self.data[24:28]))[0] * 2  #4byte integer big endian
		verbose += 'file length = ' + str(file_length) + ' Bytes\n'
		version = unpack('<i', ''.join(self.data[28:32]))[0]    #4byte integer little endian
		verbose += 'version = ' + str(version) + '\n'
		shape_type = self.shape_type_def[unpack('<i', ''.join(self.data[32:36]))[0]]  #4byte integer little endian
		verbose += 'shape type = ' + str(shape_type) + '\n'
		verbose += 'bounding box = '
		for i in range(8):
			n = unpack('<d', ''.join(self.data[i*8+36:i*8+44]))[0]    #8byte double little endian
			if i == 0:
				xmin = n
			elif i == 1:
				ymin = n
			elif i == 2:
				xmax = n
			elif i == 3:
				ymax = n
		verbose += str(xmin) + ', ' + str(ymin) + ', ' + str(xmax) + ', ' + str(ymax) + '\n'
		#print verbose
		if self.xdelta == -1.0 or self.ydelta == -1.0:
			self.xdelta = abs(xmin) + abs(xmax)
			self.ydelta = abs(ymin) + abs(ymax)
			self.pixel = self.scr_width / self.xdelta
			img_height = self.scr_width / (self.xdelta / self.ydelta)
			self.imagebuffer = Image.new('RGBA', (int(self.scr_width),int(img_height)), self.bgcolor)
			self.drawbuffer = ImageDraw.Draw(self.imagebuffer)
		elif self.imagebuffer == None:
			self.pixel = self.scr_width / self.xdelta
			img_height = self.scr_width / (self.xdelta / self.ydelta)
			self.imagebuffer = Image.new('RGBA', (int(self.scr_width),int(img_height)), self.bgcolor)
			self.drawbuffer = ImageDraw.Draw(self.imagebuffer)
		i = 100    #index of records = 100
		while i < file_length:
			record_nr = unpack('>i', ''.join(self.data[i:i+4]))[0]    #big endian
			content_length = unpack('>i', ''.join(self.data[i+4:i+8]))[0] * 2
			shape_type = unpack('<i', ''.join(self.data[i+8:i+12]))[0]    #little endian
			if shape_type == 3:
				self.get_polyline(self.data[i+8:i+8+content_length])
			elif shape_type == 5:
				self.get_polygon(self.data[i+8:i+8+content_length])
			else:
				print('--- ' + self.shape_type_def[shape_type] + ' ---')
			i += content_length + 8
			
if __name__ == '__main__':
	config1 = []
	config1.append(360.0)    #[0] xdelta = 360.0 degree for the whole earth
	config1.append(180.0)    #[1] ydelta = 180.0 degree for the whole earth
	config1.append('white')  #[2] image background color
	config1.append('ne_110m_coastline.shp') #[3] first shape file
	config1.append('black')    #[4] polygon or polyline color for first shape file
	#add additional shape files (file name and color!) see config 2
	
	config2 = []
	config2.append(-1.0)    #-1.0 = read bounding box from first shape file
	config2.append(-1.0)
	config2.append('lightblue')
	config2.append('ne_110m_land.shp')
	config2.append('brown')
	config2.append('ne_110m_lakes.shp')
	config2.append('lightblue')
	config2.append('ne_110m_coastline.shp')
	config2.append('black')
	
	ShapeFileRender(config1)

