from __future__ import print_function
# Put notebooks/files into a zipped backpack/zip archive with this [schoolbag script](https://github.com/TutorialDoctor/Scripts-for-Kids/blob/master/Python/schoolbag.py).

class Notebook:
	notebooks = []
	
	def __init__(self,name='notebook'):
		self.name = name
		self.file_name = name+'.txt'
		Notebook.notebooks.append(self.file_name)
	
	def __str__(self):
		return self.file_name
	
	def Write(self,x):
		with open(self.file_name,'a') as outfile:
			outfile.write(x+'\n')
	
	def Read(self):
		with open(self.file_name,'r') as infile:
			print(infile.read())
	
	def Erase(self):
		with open(self.file_name,'w') as outfile:
			outfile.write('')

from zipfile import ZipFile

class Backpack:
	items = []
	
	def __init__(self):
		self.name = 'my backpack'
		self.file_name = self.name+'.zip'
	
	def __str__(self):
		return self.name
	
	def Add(self,file_name,content=''):
		Backpack.items.append(file_name)
		with ZipFile(self.file_name,'a') as outzip:
			with open(file_name,'a') as outfile:
				outfile.write(content+'\n')
			outzip.write(file_name)
			
	def Dump(self,folder):
		with ZipFile(self.file_name) as inzip:
			inzip.extractall(folder)
	
	def Read(self):
		with ZipFile(self.file_name,'r') as inzip:
			for item in Backpack.items:
				print(inzip.open(item,'r').read())


# IMPLEMENTATION
#book1 = Notebook('notes')
#print book1
#book1.Write('hello')
#book1.Write('again')
#book1.Read()
#book1.Erase()
#print Notebook.notebooks
#print book1.name
#print book1.file_name


#backpack = Backpack()
#print backpack.name
#backpack.Add(book1.file_name)
#backpack.Add('stuff.txt','just some stuff to write')
#backpack.Add('otherstuff.txt','more stuff here')
#print backpack.items
#backpack.Dump('contents')
#backpack.Read()
