# coding: utf-8
import re

class NodeListWalker(object):
	def __init__(self):
		self._level = -1
		self.nodes = []
		self.parent = ["ROOT_UUID"]
		self.uuid = "ROOT_UUID"
		self.frameByUUID = {}
		self.nodeByUUID = {}
		
	def reset(self):
		self._level = -1
		self.nodes = []   
		
	@property
	def level(self):
		return self._level		
	
	@level.setter	
	def level(self,value):
		self._level = value
		
	def setFrameByUUID(self,uuid,frame,parent):
		self.frameByUUID[uuid] = (frame,parent)
	
	def parseFrame(self,frame):
		parser = re.compile(r'\{\{(.*),(.*)\}.*\{(.*),(.*\d)\}')
		res  = parser.match(frame).groups()
		list = [float(x) for x in res]
		return tuple(list)
				
	def traverseNodeList(self,nodeList):
		self._level += 1
		if nodeList:
			for node in nodeList:
				attributes = node['attributes']
				classType = node['class']
				frame = self.parseFrame(node['frame'])
				if self._level:
					nodeName = attributes['name'] if 'name' in attributes.keys() else "NULL"
					self.uuid = attributes['uuid'] if 'uuid' in attributes.keys() else "NULL"
				else:
					nodeName = "BASE"
					self.uuid = 'ROOT_UUID'
				nodes = node['nodes'] # need to have these point to UUID-based dictionary
				nodeList = [x['attributes']['uuid'] for x in nodes]
				thisParent = self.parent[-1] if len(self.parent) else "ROOT_UUID"
				self.frameByUUID[self.uuid] = (frame,thisParent)
				self.nodes.append({'level':self._level,
				                   'attributes': attributes,
				                   'frame':frame,
				                   'nodes':nodeList,
				                   'class':classType,
				                   'parent':thisParent,
				                   'uuid':self.uuid,
				                   'name':nodeName,
				                   })
				self.parent.append(self.uuid)
				self.nodeByUUID[self.uuid] = self.nodes[-1]
				self.traverseNodeList(nodes)
		self.parent = self.parent[:-1]
		self._level -= 1