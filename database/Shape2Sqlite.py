# coding: utf-8
from __future__ import print_function
import sqlite3
import shapefile

class Shape2Sqlite(object):
	def __init__(self, path, files):
		self.shape_type_def = {0: 'Null Shape',1: 'Point', 3: 'PolyLine', 5: 'Polygon', 8: 'MultiPoint', 11: 'PointZ', 13: 'PolyLineZ', 15: 'PolygonZ', 18: 'MultiPointZ', 21: 'PointM', 23: 'PolyLineM', 25: 'PolygonM', 28: 'MultiPointM', 31: 'MultiPatch'}
		
		self.path = path
		self.sqlcon = None
		self.sqlcur = None
		self.shapes = []
		self.shapes_count = 0
		self.polys = []
		self.polys_count = 0
		self.points = []
		self.points_count = 0
		
		self.check_tables()
		print(str(self.shapes_count) + ' shapes, ' + str(self.polys_count) + ' polys and ' + str(self.points_count) + ' points')
		print()
		self.shapes_count += 1
		self.polys_count += 1
		
		for i in range(len(files)):
			self.read_files(files[i])
		self.sqlcon.close()
		print('db closed')
		print('exit')
		
	def check_tables(self):
		self.sqlcon = sqlite3.connect('earth.db')
		self.sqlcur = self.sqlcon.cursor()
		
		#ID_Shape = For each shape(file/table)
		#ID_Poly = For each poly(line/gon or for many points like cities)
		#ID_Point = For each point per poly
		cursor = self.sqlcur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Shapes'")
		if cursor.fetchone()[0] == 0:
			self.sqlcur.execute("CREATE TABLE 'Shapes' ('ID_Shape' INTEGER, 'Name' TEXT)")
			#print 'Table Shapes is created'
		else:
			#print 'Table Shapes exists'
			cursor = self.sqlcur.execute("SELECT max(ID_Shape) FROM Shapes")
			self.shapes_count = cursor.fetchone()[0]
			if self.shapes_count == None:
				self.shapes_count = 0
				
		cursor = self.sqlcur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Polys'")
		if cursor.fetchone()[0] == 0:
			self.sqlcur.execute("CREATE TABLE 'Polys' ('ID_Shape' INTEGER, 'ID_Poly' INTEGER, 'ShapeType' INTEGER, 'Xmin' REAL, 'Ymin' REAL, 'Xmax' REAL, 'Ymax' REAL, 'NumParts' INTEGER, 'NumPoints' INTEGER, 'Name' TEXT)")
			self.sqlcon.commit()
			#print 'Table Polys is created'
		else:
			#print 'Table Polys exists'
			cursor = self.sqlcur.execute("SELECT max(ID_Poly) FROM Polys")
			self.polys_count = cursor.fetchone()[0]
			if self.polys_count == None:
				self.polys_count = 0
				
		cursor = self.sqlcur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Points'")
		if cursor.fetchone()[0] == 0:
			self.sqlcur.execute("CREATE TABLE 'Points' ('ID_Poly' INTEGER,'ID_Point' INTEGER,'X' REAL,'Y' REAL, 'Name' TEXT)")
			#print 'Table Points is created'
		else:
			#print 'Table Points exists'
			cursor = self.sqlcur.execute("SELECT COUNT(*) FROM Points")
			self.points_count = cursor.fetchone()[0]
			
	def get_points(self, shape, ShapeType):
		index = 1
		if len(shape.parts) > 1:    #NumParts > 1
			parts_nr = len(shape.parts)
			for k in range(parts_nr - 1):
				index = 1
				for l in range(shape.parts[k], shape.parts[k+1]):
					self.points.append((self.polys_count, index, shape.points[l][0], shape.points[l][1], None))
					index += 1
			k += 1
			index = 1
			self.polys_count += 1
			self.polys.append((self.shapes_count, self.polys_count, ShapeType, None, None, None, None, None, None, None))
			for l in range(shape.parts[k], len(shape.points)):
				self.points.append((self.polys_count, index, shape.points[l][0], shape.points[l][1], None))
				index += 1
		else:
			for k in range(len(shape.points)):
				self.points.append((self.polys_count, index, shape.points[k][0], shape.points[k][1], None))
				index += 1
				
	def read_files(self, file):
		self.shapes = []
		self.points = []
		self.polys = []
		myshp = open(self.path + file + ".shp", "rb")
		mydbf = open(self.path + file + ".dbf", "rb")
		r = shapefile.Reader(shp=myshp, dbf=mydbf)
		shapes = r.shapes()
		records = r.records()
		fields = r.fields
		self.shapes.append((self.shapes_count, file))
		ShapeType = shapes[0].shapeType
		print('ShapeType[0] = ' + self.shape_type_def[ShapeType])
		if self.shape_type_def[ShapeType] == 'Point':
			self.polys.append((self.shapes_count, self.polys_count, ShapeType, None, None, None, None, None, len(shapes), None))
		name_nr = -1
		for j in range(len(fields)):
			if fields[j][0] == 'name' or fields[j][0] == 'NAME':    #is a name field in .dbf?
				name_nr = j - 1            #get index of name field
		for i in range(len(shapes)):
			if name_nr > -1:
				if fields[name_nr + 1][0] == 'name': #old coding cp1252 or new coding utf8?
					name = (records[i][name_nr]).decode('cp1252')
				else:
					name = (records[i][name_nr]).decode('utf8')
			else:
				name = None
				
			if self.shape_type_def[ShapeType] == 'Null Shape':
				pass
			elif self.shape_type_def[ShapeType] == 'Point':
				self.points.append((self.polys_count, i+1, float(shapes[i].points[0][0]), float(shapes[i].points[0][1]), name))
			elif self.shape_type_def[ShapeType] == 'PolyLine' or self.shape_type_def[ShapeType] == 'Polygon':
				try:
					Xmin, Ymin, Xmax, Ymax = shapes[i].bbox
					NumParts = len(shapes[i].parts)
					NumPoints = len(shapes[i].points)
					self.polys.append((self.shapes_count, self.polys_count, ShapeType, Xmin, Ymin, Xmax, Ymax, NumParts, NumPoints, name))
					self.get_points(shapes[i], ShapeType)
					if i < len(shapes) - 1:
						self.polys_count += 1
				except:
					print('>>> Error: ShapeType[' + str(i) + '] = ' + str(shapes[i].shapeType) + ' <<<')
			else:
				print('--- ' + self.shape_type_def[ShapeType] + ' ---')
				
		if len(self.shapes) > 0:
			self.sqlcur.executemany("INSERT INTO Shapes VALUES (?, ?)", self.shapes)
			print('added ' + str(len(self.shapes)) + ' shape ' + file)
			self.sqlcon.commit()
		if len(self.polys) > 0:
			self.sqlcur.executemany("INSERT INTO Polys VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.polys)
			print('added ' + str(len(self.polys)) + ' polys')
			self.sqlcon.commit()
		if len(self.points) > 0:
			self.sqlcur.executemany("INSERT INTO Points VALUES (?, ?, ?, ?, ?)", self.points)
			print('added ' + str(len(self.points)) + ' points')
			self.sqlcon.commit()
		print()
		self.shapes_count += 1
		self.polys_count += 1
		
if __name__ == '__main__':
	path = 'data/'
	
	files = ('ne_50m_admin_0_countries', 'ne_50m_admin_0_countries_lakes', 'ne_50m_admin_0_boundary_lines_land', 'ne_50m_admin_0_boundary_lines_maritime_indicator', 'ne_50m_admin_0_boundary_map_units', 'ne_50m_admin_0_pacific_groupings', 'ne_50m_airports', 'ne_50m_coastline', 'ne_50m_geographic_lines', 'ne_50m_lakes', 'ne_50m_lakes_historic', 'ne_50m_land', 'ne_50m_ocean', 'ne_50m_populated_places_simple', 'ne_50m_ports', 'ne_50m_rivers_lake_centerlines', 'ne_50m_urban_areas', 'ne_50m_wgs84_bounding_box')
	
	Shape2Sqlite(path, files)

