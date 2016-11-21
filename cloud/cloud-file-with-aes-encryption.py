# coding: utf-8

# https://forum.omz-software.com/topic/2799/cloud-file-with-aes-encryption/12

'''
cloud.py

Vision:

- cloud.Import: to make the entry curve to using code hosted on GitHub much easier
- cloud.File: generic file-type object that implements cloud storage

Credits:

- cloud.Import: idea and first version by @guerito, future versions on @webmaster4o's GitHub
- cloud.File: idea and first version by @guerito, future versions on @webmaster4o's GitHub

'''

import io, os, urllib, json, base64
from Crypto.Cipher import AES

class File(io.BytesIO):
	""" cloud.File: generic file-type object that implements cloud storage """
	def __init__(self, name, mode = '', buffering = 0, encryptionKey = ''):
		self.name = name
		self.mode = mode
		self.encoding = None
		self.errors = None
		self.newlines = None
		self.softspace = 0
		self.__encryptionKey = encryptionKey
		self.mf = self.__mFile()
		self.__iPos = 0
		self.__sBuffer = None
		
	def commit(self):
		mf = self.__mFile()
		if self.mode == 'w':
			mf.write(self.__EncryptionProvider().encodeFile(self.mf, self.__encryptionKey))
		elif self.mode == 'wb':
			b64 = self.__mFile()
			base64.encode(self.mf, b64)
			mf.write(self.__EncryptionProvider().encodeFile(b64, self.__encryptionKey))
		url = self.__CloudProvider().putFileToURL(mf)
		return url
		
	def close(self):
		self.mf.close()
		super(File, self).close()
		
	def flush(self):
		pass
		
	#def fileno(self): should not be implemented for file-like objects
	
	def getvalue(self):
		if self.__sBuffer == None:
			self.__sBuffer = ''
			self.__sBuffer = self.getvalue()
			return self.__sBuffer
		elif len(self.__sBuffer) > 0:
			return self.__sBuffer
		mf = self.__mFile()
		mf.write(self.__EncryptionProvider().decodeFile(self.__CloudProvider().getFileFromURL(self.name), self.__encryptionKey))
		if self.mode == 'r':
			return mf.read()
		if self.mode == 'rb':
			b64 = self.__mFile()
			base64.decode(mf, b64)
			return b64.read()
			
	#def isatty(self): should not be implemented for file-like objects
	
	def next(self):
		self.getvalue()
		if self.__iPos < len(self.__sBuffer):
			return self.readline()
		else:
			raise StopIteration
			
	def read(self, size = -1):
		if size < 0:
			return self.getvalue()[self.__iPos:]
			self.__iPos = len(self.__sBuffer)
		else:
			s = self.getvalue()[self.__iPos:self.__iPos + size]
			self.__iPos += size
			return s
			
	def read1(self):
		return self.read()
		
	def readline(self, size = 0):
		if size < 0:
			return self.read(77)
		else:
			return self.read((self.getvalue()[self.__iPos:] + '\n').find('\n') + 1 if size < 1 else size)
			
	def readlines(self, sizehint = 0):
		l = list()
		while self.__sBuffer == None or self.__iPos < len(self.__sBuffer):
			l.append(self.readline())
		return l
		
	def xreadlines(self):
		return self
		
	def seek(self, offset, whence = os.SEEK_SET):
		self.getvalue()
		if whence == os.SEEK_SET:
			self.__iPos = offset
		elif whence == os.SEEK_CUR:
			self.__iPos += offset
		elif whence == os.SEEK_END:
			self.__iPos = len(self.__sBuffer) + offset
			
	def tell(self):
		return self.__iPos
		
	def truncate(self, size = None):
		self.getvalue()
		if size == None: size = self.__iPos
		self.__sBuffer = self.__sBuffer[:size]
		
	def write(self, str):
		self.mf.write(str)
		self.__iPos += len(str)
		
	def writelines(self, sequence = None):
		for s in sequence:
			self.write(s)
			
			
	class __mFile(io.BytesIO):
		""" memory based file: BytesIO with read() and readline() methods """
		def __init__(self):
			io.BytesIO.__init__(self)
			self.__iPos = 0
			
		def read(self, size = -1):
			if size < 0:
				return self.getvalue()[self.__iPos:]
			else:
				s = self.getvalue()[self.__iPos:self.__iPos + size]
				self.__iPos += size
				return s
				
		def readline(self, size = -1):
			if size < 0:
				return self.read(77)
			else:
				return self.read((self.getvalue()[self.__iPos:] + '\n').find('\n') + 1 if size < 1 else size)
				
				
	class __CloudProvider(object):
		"""default implementation using Gist can be subclassed for: GitHub, @webmaster4o server, Googledrive, Dropbox, Box, OneDrive, WebDav, etc """
		def putFileToURL(self, f):
			return json.loads(urllib.urlopen('https://api.github.com/gists', json.dumps({ "description": "-", "public": False, "files": { '-': { "content": f.read()} } })).read())['files']['-']['raw_url']
			
		def getFileFromURL(self, sURL):
			return urllib.urlopen(sURL)
			
	class __EncryptionProvider(object):
		"""default implementation using Crypto.Cipher AES (stateful), can be subclassed for any other"""
		def __init__(self):
			self.s16 = 'vB03eMZQ0lnsNVX6'
			
		def encodeFile(self, f, key):
			s = f.read()
			if key == '' : return s
			s = str(len(s)) + '-' + s
			s += self.s16[:(16 - (len(s) % 16))]
			aes = AES.new(key[:16] + self.s16[:16 - len(key[:16])], AES.MODE_CBC, self.s16)
			return base64.urlsafe_b64encode(aes.encrypt(s))
			
		def decodeFile(self, f, key):
			s = f.read()
			if key == '' : return s
			aes = AES.new(key[:16] + self.s16[:16 - len(key[:16])], AES.MODE_CBC, self.s16)
			s = aes.decrypt(base64.urlsafe_b64decode(s))
			i = s.find('-')
			return s[i+1:long(s[:i]) + i + 1]
# --------------------

