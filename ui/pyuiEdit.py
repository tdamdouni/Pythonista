# coding: utf-8

'''

Author:  Steven K. Pollack
Date Released: May 16, 2015

allow for text editing to encapsulate specific views from a pyui as subviews of a "container" view

The strucure of a "node" is a dictionary with the four keys:
	
{ "attributes": {dictionary of artibutes of the current node},
  "frame" : "{(top,left},{width,height}}", # notes this is not a dictionary
  "nodes": [list of subviews], # a subview is a node
  "class": "class type"
}

The topmost node (the rootView) is a list with a single node

'''
from __future__ import print_function
import ui, console,os,os.path,sys,json,re,uuid,math,copy,dialogs
from copy import deepcopy

import uidir; reload(uidir); from uidir import FileGetter
import NodeListWalker; reload(NodeListWalker); from NodeListWalker import NodeListWalker

depthColors =  [(1.00, 0.80, 0.40),
                (1.00, 1.00, 0.00),
                (0.40, 0.80, 1.00),
                (0.90, 0.90, 0.90),
                (1.00, 0.40, 1.00),
                (0.80, 1.00, 0.40),
                (0.60, 1.00, 0.30),
               ]

validQuadTuple = re.compile(r"""\(
                                 \D?([+-]?\d+\.?\d*)
                                 \D*([+-]?\d+\.?\d*)
                                 \D*([+-]?\d+\.?\d*)
                                 \D*([+-]?\d+\.?\d*)
                                 \D
                                 |
                                 \D?([+-]?\d+\.?\d*)
                                 \D*([+-]?\d+\.?\d*)
                                 \D*([+-]?\d+\.?\d*)
                                 \D*([+-]?\d+\.?\d*)
                                 """,
                              re.X)
                              


genericView =   '{{"attributes": {{"tint_color": "RGBA(0.000000,0.000000,1.000000,1.000000)","border_color": "RGBA(0.000000,0.000000,0.000000,1.000000)","background_color": "RGBA(1.000000,1.000000,1.000000,1.000000)","enabled": True,"flex": "","uuid": "{}","name": "{}",}},"frame": {},"nodes": {},"class": "View","level":{},"uuid":"{}","parent":"{}",}}'

def flatten(S):
	if S == []:
		return S
	if isinstance(S[0], list):
		return flatten(S[0]) + flatten(S[1:])
	return S[:1] + flatten(S[1:])

def uniqify(sequence, idfun=None):
	''' return a unique, order preserved version in input list'''
	if not idfun:
		def idfun(x): return x
	seen = {}
	result = []
	for item in sequence:
		marker = idfun(item)
		if marker in seen.keys(): 
			continue
		seen[marker] = 1
		result.append(item)
	return result
			
class ItemsWalker(): # walk down an items list and find children
	def __init__(self,items):
		self.items = items

	def walkItems(self,itemList):
		indexList = []
		for index in itemList:
			rowList = []
			rowList.append(index)
			thisItem = self.items[index]
			nodes = thisItem['node']['nodes']
			if nodes:
				nodeList = []
				for node in nodes:
					for row,item in enumerate(self.items):
						if node == item['node']['uuid']:
							nodeList.append(row)
				rowList.append(self.walkItems(nodeList))
			else:
				rowList.append([])
			indexList.append(rowList)
		return indexList

def listShuffle(list,row_from, row_to):
	''' a method to re-order a list '''
	from_item = list[row_from]
	del list[row_from]
	list.insert(row_to,from_item)
	return list

		
class nodeMapView(ui.View):
	def did_load(self):
		self.nodes = []

	def inRectangle(self,point,rect):
		if (rect[0] <= point[0] <= rect[0]+rect[2]) and (rect[1] <= point[1] <= rect[1]+rect[3]):
			return True
		else:
			return False
		
	def centroid(self,frame):
		cX = frame[2]/2.0 + frame[0]
		cY = frame[3]/2.0 + frame[1]
		return (cX,cY)
		
				
	def init(self,data_source):
		self.data_source = data_source
		self.pyuiFrame = self.data_source.items[0]['node']['frame']
		self.pyuiWidth = self.pyuiFrame[2] - self.pyuiFrame[0]
		self.pyuiHeight = self.pyuiFrame[3] - self.pyuiFrame[1]
		if self.pyuiWidth > self.pyuiHeight:
			self.ratio = self.width/self.pyuiWidth
		else:
			self.ratio = self.height/self.pyuiHeight
			
	def draw(self):
		if not self.data_source.items: return
		topNodesFrame = self.data_source.items[0]['node']['frame']
		topNodeCentroid = self.centroid(topNodesFrame)
		
# need to account for orgins of parents.  need to walk down the tree
		for item in self.data_source.items:
			title = item['title']
			node = item['node']
			level = node['level']
			frame = node['frame']
			uuid = node['uuid']
			try:
				parent = node['parent']
			except KeyError:
				print("Keyerror on node['parent']\n")
				print(item)
				sys.exit(1)
			isSelected = item['selected']
			isHidden = item['hidden']
			offset = [0,0]
			ctr = 0
			while parent != 'ROOT_UUID': 
 # work back through lineage until no more offsets.
				ctr +=1
				if ctr > 30:
					sys.exit(1)
				parentFrame,grandParent = walker.frameByUUID[parent]
				offset = [offset[0] + parentFrame[0], offset[1] +parentFrame[1]]
				parent = grandParent
					
			try:
				xframe = [frame[0] + offset[0], frame[1] + offset[1], frame[2], frame[3]]	
			except TypeError:
				print("Type error in collect")
				print("frame", xframe, "offset", offset)
			if not isHidden and level:
				scaledFrame = [x*self.ratio for x in xframe]
				path = ui.Path.rect(*scaledFrame)
				ui.set_color((depthColors[level]) + (0.5,))
				path.fill()
				ui.set_color(0.5)
				path.line_width = 5 if isSelected else 2
				path.stroke()
			
			
	def touch_began(self,touch):
		global lastSelectedRow
		location = touch.location
		for row,item in enumerate(nodeDelegate.items[1:]):
			if self.inRectangle(location,[x*self.ratio for x in item['node']['frame']]) and not item['hidden']:
				nodeDelegate.items[row+1]['selected'] = not nodeDelegate.items[row+1]['selected']
				if nodeDelegate.items[row+1]['selected']:
					lastSelectedRow = row+1
				else:
					lastSelectedRow = -1
				tvNodeList.reload_data()
				self.set_needs_display()
				break
				
class NodeTableViewDelegate(object):
	def __init__(self,items):
		self.items = items
		self.listLength = len(self.items)
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
	
	def delayed_reload(self):
		global tvNodeList
		tvNodeList.selected_rows = []
		tvNodeList.reload_data()
		

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return self.listLength

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		level = self.items[row]['node']['level']
		cell.text_label.text = (level)*">>" + (level != 0)*" " + self.items[row]['title']
		if self.items[row]['hidden']:
			cell.text_label.text_color = (0.90, 0.90, 0.90)
		else:
			cell.text_label.text_color = 'red' if self.items[row]['selected'] else 'black'	
		cell.accessory_type = 'detail_button'
		try:
			level = self.items[row]['node']['level']
		except KeyError:
			print("Keyerror in cell for row")
			print(row)
			print(self.items[row]['node'])
			sys.exit(1)
		cell.background_color = depthColors[level]
		return cell
	
	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		global lastSelectedRow
		if not self.items[row]['hidden']:
			self.items[row]['selected'] =  not self.items[row]['selected']
			viewNodeMap.set_needs_display()
			lastSelectedRow = row
		ui.delay(self.delayed_reload,0.05)

			
		
	def tableview_did_deselect(self,tableview,section,row):
		pass

	def tableview_accessory_button_tapped(self, tableview, section, row):	
		console.hud_alert('Frame: {}'.format(self.items[row]['node']['frame']))

def collectiveSize(selected,margin=(0,0,0,0)):
	' calculate size of a container with margins specified '
	topLeftX = 10000
	bottomRightX = -10000
	topLeftY = 10000
	bottomRightY = -10000
	for _,item in selected:
		frame = item['node']['frame']
		topLeftX = min(topLeftX,frame[0])
		topLeftY = min(topLeftY,frame[1])
		bottomRightX = max(bottomRightX, (frame[0]+frame[2]))
		bottomRightY = max(bottomRightY, (frame[1]+frame[3]))
	width = bottomRightX - topLeftX
	height = bottomRightY - topLeftY
	topLeftX -= margin[0]
	topLeftY -= margin[1]
	width += margin[0]+margin[1]
	height += margin[2]+margin[3]
	
	return (topLeftX,topLeftY, width, height)

class pyuiBuilder():
	def __init__(self,rowByUUID,nodeDelegate):
		self.rowByUUID = rowByUUID
		self.padLevel = 0
		self.items = nodeDelegate.items
		self.outString = ""
		
	def openBrace(self):
		self.outString +=  "{}[\n".format(self.padLevel*"  ")
		self.padLevel +=1

		
	def closeBrace(self,comma=False):
		commaIndex = self.outString.find(',',-4)
		if commaIndex != -1:
			self.outString = self.outString[:commaIndex] + '\n'
		self.padLevel -=1
		if comma:
			self.outString += "{}],\n".format(self.padLevel*"  ")
		else:
			self.outString += "{}]\n".format(self.padLevel*"  ")
		
	def openCurly(self):
		self.outString += "{}{{\n".format(self.padLevel*"  ")
		self.padLevel +=1
		
	def closeCurly(self,comma=False):
		commaIndex = self.outString.find(',',-4)
		if commaIndex != -1:
			self.outString = self.outString[:commaIndex] + '\n'
		self.padLevel -=1
		if comma:
			self.outString += "{}}},\n".format(self.padLevel*"  ")
		else:
			self.outString += "{}}}\n".format(self.padLevel*"  ")
				
	def padded(self,string):
		self.outString += "{}{}".format(self.padLevel*"  ",string)
		
	def unpadded(self,string):
		self.outString += string
	
	def traverse(self,uuid):
		thisNode = self.items[self.rowByUUID[uuid]]['node']
		nodes = thisNode['nodes']
		attributes = thisNode['attributes']
		frame = thisNode['frame']
		thisClass = thisNode['class']
		try:
			name = thisNode['name']
		except:
			name = attributes['name']

		self.openCurly()
		self.padded('"attributes": {\n')
		self.padLevel += 1
		for key,value in attributes.items():
			if key in ["frame","class"]:
				continue
			self.padded('"{}": '.format(key))
			if type(value) == type(True):
				if value:
					self.unpadded('true, \n')
				else:
					self.unpadded('false, \n')
			elif type(value) in (type(1.5),type(1)):
				self.unpadded('{}, \n'.format(value))
			else:
				if key == 'data_source_items':
					value = value.replace('\n','\\n')
				self.unpadded('"{}", \n'.format(value))
					
		self.closeCurly(comma=True)
		self.padded('"frame": "{{{{{}, {}}}, {{{}, {}}}}}", \n'.format(*frame))
		self.padded('"class": "{}", \n'.format(thisClass))
		self.padded('"nodes":')
		if not nodes:
			self.unpadded('[],\n')
		else:			
			self.unpadded('[\n')
			self.padLevel += 1
			firstNode = True
			for node in nodes:
				self.traverse(node)
			self.closeBrace(comma=True)
		self.closeCurly(comma=True)
								
	def makeString(self,root):
		self.padLevel = 0
		self.outString = ''
		self.openBrace()
		self.traverse(root['uuid'])
		self.closeBrace()
		return self.outString

@ui.in_background
def onSave(button):
	global nodeDelegate,walker,undoStack,fileDirectory
	try:
		fileName = console.input_alert('Ouptut File','Enter Output File Name',fileDirectory+'/')
	except KeyboardInterrupt:
		return
	
	base,ext = os.path.splitext(fileName)
	if not ext:
		ext = '.pyui'
		
	if ext not in ['.pyui','.json']:
		console.hud_alert('invalid ui file type')
		return

	root = nodeDelegate.items[0]['node']
	
	fileName = base+ext
	
	rowByUUID = {}
	for row,item in enumerate(nodeDelegate.items):
		rowByUUID[item['node']['uuid']] = row
		
	pyui = pyuiBuilder(rowByUUID,nodeDelegate)
	outString = pyui.makeString(root)
	
	with open(fileName, 'wb') as fh:
		fh.write(outString)
	
def buildTree(workingList,inputList,items):
	for thisIndex,nodes in inputList:
		workingList.append(items[thisIndex])
		if nodes:
			buildTree(workingList,nodes,items)

@ui.in_background
def onCollect(button):	
	global nodeDelegate,walker,undoStack,lastSelectedRow
	
	selected = []
	for row,item in enumerate(tvNodeList.delegate.items):
		if item['selected'] and not item['hidden']:
			selected.append((row,item))
		
	if selected:
		item = selected[0][1] # get the first selected 
		oldParent = item['node']['parent']
		oldLevel = item['node']['level']
		
		for _,item in selected:
			if oldParent != item['node']['parent']:
				console.hud_alert("Mixed heritgate items collected.  Must all have same parent")
				return				

		result = dialogs.form_dialog("Container View",
						[{'type':'text', 
							'key':'name', 
							'title':'View Name',
							'value':''},
						 {'type':'text',
							'key':'margins',
							'title':'Frame Margins',
							'value':'0,0,0,0'},
						 {'type':'text',
							'key':'customView',
							'title':'Custom View Class',
							'value':''}
						]
						)
		if not result:
			return
			
		customViewClass = result['customView']
		name = result['name']
	
		match = validQuadTuple.match(result['margins'])
		if match:
			margins = [float(x) for x in match.groups() if x]
			if len(margins) != 4:
				console.hud_alert("{} is invalid margin definition".format(result))
		else:
			console.hud_alert("{} is invalid margin definition".format(result))
			return			
			
		undoStack.append((deepcopy(nodeDelegate.items),
										  deepcopy(walker.frameByUUID))
										)		
		for row,item in enumerate(nodeDelegate.items):
			if item['node']['uuid'] == oldParent:
				oldParentRow = row
																
		collectionFrame = collectiveSize(selected,margins)
		location = "{{{}, {}}}".format(*collectionFrame[:2])
		widthHeight = "{{{}, {}}}".format(*collectionFrame[2:])
		collectionPyuiFrame = "{{{}, {}}}".format(location,widthHeight)
		collectionUUID = str(uuid.uuid4()).upper()
		childUUIDs =[]
		parentFrame,parentUUID = walker.frameByUUID[oldParent]

		children = []
		# adjust the first generation children frames and parehhood
		for row,item in selected:
			thisUUID = item['node']['uuid']
			thisFrame = item['node']['frame']
			newFrame = (thisFrame[0]  - collectionFrame[0],
									thisFrame[1]  - collectionFrame[1],
									thisFrame[2], thisFrame[3])
			thisLoc = "{{{}, {}}}".format(*newFrame[:2])
			thisWH = "{{{}, {}}}".format(*newFrame[2:])
			pyuiFrame = "{{{}, {}}}".format(thisLoc,thisWH)
			nodeDelegate.items[row]['node']['frame'] = newFrame
			nodeDelegate.items[row]['node']['attributes']['frame'] = pyuiFrame
			nodeDelegate.items[row]['node']['parent'] = collectionUUID
			for nodeIndex,node in enumerate(nodeDelegate.items[oldParentRow]['node']['nodes']):
				if node == thisUUID:
					nodeDelegate.items[oldParentRow]['node']['nodes'][nodeIndex] = collectionUUID
					break			
			#the above will lead to redundant references to the same node.  Make unique later.
			
			walker.setFrameByUUID(thisUUID,newFrame,collectionUUID) # update the "byUUID" hash
			childUUIDs.append(nodeDelegate.items[row]['node']['uuid']) #save for writing the collection view
# accululate all childrens rows (as a tree)
			childwalker = ItemsWalker(nodeDelegate.items)
			children.append(childwalker.walkItems([row,]))
			del childwalker
		
		nodeDelegate.items[oldParentRow]['node']['nodes'] = uniqify(nodeDelegate.items[oldParentRow]['node']['nodes'])
		childrenRows = flatten(children) # get the indexes as a simple list
		for row in childrenRows:
			nodeDelegate.items[row]['node']['level'] += 1
			
		thisNode = genericView.format(collectionUUID, name, collectionFrame, childUUIDs,oldLevel,collectionUUID,oldParent)
		thisItem= {
          'title': name,
          'node' : eval(thisNode),
          'selected':False,
          'hidden':False,
          'accessory_type':None,
          } 
		if customViewClass:
			thisItem['custom_class'] = customViewClass
			
		insertPoint = selected[0][0]
		
		childrenItems = [nodeDelegate.items[row] for row in childrenRows]
		
		otherItems = [nodeDelegate.items[row] for 
									row in range(insertPoint+1,len(nodeDelegate.items))
									if row not in childrenRows]
									
		nodeDelegate.items.insert(insertPoint,thisItem)
		nodeDelegate.listLength += 1
		walker.setFrameByUUID(collectionUUID,collectionFrame,oldParent)

		nodeDelegate.items[:] = nodeDelegate.items[:insertPoint+1]
		for item in childrenItems:
			nodeDelegate.items.append(item)
		for item in otherItems:
			nodeDelegate.items.append(item)
			
		for row,_ in enumerate(nodeDelegate.items):
			nodeDelegate.items[row]['selected'] = False
			nodeDelegate.items[row]['hidden'] = False		
		
		tvNodeList.selected_rows = []
		lastSelectedRow = -1
		tvNodeList.reload_data()
		viewNodeMap.set_needs_display()

		
		
		
def onSelectChildren(button):
	global nodeDelegate,lastSelectedRow
	def markChildren(thisRow):
		thisUUID = nodeDelegate.items[thisRow]['node']['uuid']
		for row in range(thisRow,len(nodeDelegate.items)):
			if nodeDelegate.items[row]['node']['parent'] == thisUUID:
				nodeDelegate.items[row]['selected'] = True
				markChildren(row)
						
	if lastSelectedRow < 0:
		return
	markChildren(lastSelectedRow)
	lastSelectedRow = -1
	tvNodeList.reload_data()
	viewNodeMap.set_needs_display()

		
def onQuit(button):
	global v
	v.close()
	
	
def onUndo(button):
	global nodeDelegate,undoStack,walker,lastSelectedRow
	if undoStack:
		previousList,previousDict = undoStack.pop()
		nodeDelegate.items = deepcopy(previousList)
		walker.frameByUUID = deepcopy(previousDict)
		for row,_ in enumerate(nodeDelegate.items):
			nodeDelegate.items[row]['selected'] = False
			nodeDelegate.items[row]['hidden'] = False
		nodeDelegate.listLength = len(nodeDelegate.items)
		lastSelectedRow = -1
		tvNodeList.reload_data()
		viewNodeMap.set_needs_display()
			
def onHideSelected(button):
	global nodeDelegate
	for row,item in enumerate(nodeDelegate.items):
		if item['selected']:
			nodeDelegate.items[row]['hidden'] = True
			item['selected'] = False
	viewNodeMap.set_needs_display()
	tvNodeList.reload_data()
						
def onUnhideAll(button):
	global nodeDelegate
	for item in nodeDelegate.items:
		item['hidden'] = False
	viewNodeMap.set_needs_display()
	tvNodeList.reload_data()
	
def onDeselectAll(button):
	global nodeDelegate,lastSelectedRow
	for item in nodeDelegate.items:
		item['selected'] = False
	lastSelectedRow = -1
	viewNodeMap.set_needs_display()
	tvNodeList.reload_data()
	
if __name__ == '__main__':
	undoStack = []
	fg = FileGetter(types=['pyui','json'])
	fg.getFile()
	thisFile = fg.selection
	fileDirectory = os.path.normpath(os.path.dirname(thisFile))

	_,ext = os.path.splitext(thisFile)
	if not ext in ['.pyui','.json']:
		console.hud_alert('Invalid file type')
		sys.exit(1)
	
	with open(thisFile,'r') as fh:
		pyui = json.load(fh)
	
	walker = NodeListWalker()
	walker.traverseNodeList(pyui)

	items = [{
          'title': x['name'],
          'node' : x, 
          'selected':False,
          'hidden':False,
          'accessory_type':None,
          } 
          for x in walker.nodes]
          
	v = ui.load_view()
	nodeDelegate = NodeTableViewDelegate(items)
	tvNodeList = v['view_nodeList']
	tvNodeList.delegate = nodeDelegate
	tvNodeList.data_source = nodeDelegate
	tvNodeList.allows_multiple_selection = True	
	viewNodeMap = v['nodeMap']
	viewNodeMap.init(nodeDelegate)
	viewNodeMap.touch_enabled = True
	lastSelectedRow = -1
	
	v['button_Collect'].action = onCollect
	v['button_Quit'].action = onQuit 
	v['button_Save'].action = onSave
	v['button_Undo'].action = onUndo
	v['button_Hide_Selected'].action = onHideSelected
	v['button_Unhide_All'].action = onUnhideAll
	v['button_Select_Children'].action = onSelectChildren
	v['button_Deselect_All'].action = onDeselectAll

	v.present()


	