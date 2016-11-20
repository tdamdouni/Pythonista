#!python2
# coding: utf-8

# https://gist.github.com/anonymous/d25e981c9a344dd2df288c651d44465b

import ui
import dialogs
import photos
import Image

buttonWidth = ui.get_screen_size()[0]/4
ss = ui.get_screen_size()
#ss = (300,400)

imageContainer = ui.View()
imageContainer.frame = (0,0,ss[0],ss[1]-114)

CURRENTCOLOR = "black"

items = [
        {"title":"Name","type":"text","icon":ui.Image('iob:document_24'),"placeholder":"untitled.png"},
        {"title":"Width","type":"number","icon":ui.Image('iob:arrow_resize_24')},
        {"title":"Height","type":"number","icon":ui.Image('iob:arrow_resize_24')},
        {"title":"Background","type":"text","placeholder":"white, black, red, etc.","icon":ui.Image('iob:image_24'),"value":"white"}
]
popup = dialogs.form_dialog("Image Setup",items)

if popup == None:
	from sys import exit
	exit()
	
imageSize = (popup["Width"],popup["Height"])

class PaletteColor (ui.View):
	def __init__(self, frame, colorName, using, colorHex=None):
		if colorName == "yellow" or colorName == "lightgrey":
			self.dark = True
		else:
			self.dark = False
		self.name = colorName
		self.colorName = colorName
		self.frame = frame
		self.background_color = self.colorName
		self.using = using
		if self.using == True:
			self.checkmark = ui.ImageView()
			if self.dark == True:
				self.checkmark.image = ui.Image('iob:checkmark_32')
			else:
				self.checkmark.image = ui.Image('iow:checkmark_32')
			self.checkmark.frame = (105,60,40,40)
			self.add_subview(self.checkmark)
		self.nameLabel = ui.Label()
		self.nameLabel.text = "   "+self.colorName
		self.nameLabel.frame = (0,self.frame[3]-40,self.frame[2],40)
		if self.colorName == "lightgrey" or self.colorName == "yellow":
			self.nameLabel.text_color = "black"
		else:
			self.nameLabel.text_color = "white"
		self.add_subview(self.nameLabel)
		
	def touch_began(self, touch):
		if self.using != True:
			self.checkmark = ui.ImageView()
			if self.dark == True:
				self.checkmark.image = ui.Image('iob:checkmark_32')
			else:
				self.checkmark.image = ui.Image('iow:checkmark_32')
			self.checkmark.frame = (105,60,40,40)
			self.add_subview(self.checkmark)
			self.superview[CURRENTCOLOR].set_using(False)
		self.using = True
		
	def touch_ended(self, touch):
		def closePalette():
			self.superview.superview["palette"].frame = (0,ss[1],ss[0],200)
		ui.animate(closePalette,0.6)
		global CURRENTCOLOR
		CURRENTCOLOR = self.colorName
		colorbtn.tint_color = self.colorName
		drawCanvas.color = self.colorName
		
	def set_using(self, using):
		self.using = using
		self.remove_subview(self.checkmark)
		
class Paper (ui.View):
	def __init__(self, frame):
		if frame[2] > ss[0] or frame[3] > ss[1]:
			raise Exception("Paper is too big")
		else:
			self.frame = frame
			# create the imageview that actually shows the image you're drawing.
			self.canvas = ui.ImageView()
			self.bg_color = popup["Background"]
			self.canvas.frame = (0,0,frame[2],frame[3])
			with ui.ImageContext(self.width,self.height) as setup:
				self.background = ui.Path()
				ui.set_color(self.bg_color)
				ui.fill_rect(0,0,self.width,self.height)
				bg = self.background.rect(0,0,self.width,self.height)
				self.background = setup
				self.canvas.image = setup.get_image()
				
			self.add_subview(self.canvas)
			
			self.color = CURRENTCOLOR
			self.brush_size = 8
			self.tool = "brush"
			
			self.path = None
			
	def touch_began(self, touch):
		ui.set_color(self.color)
		self.path = ui.Path()
		self.path.line_cap_style = ui.LINE_CAP_ROUND
		self.path.line_join_style = ui.LINE_JOIN_ROUND
		self.path.line_width = self.brush_size
		if self.tool == "brush":
			self.path.move_to(touch.location[0],touch.location[1])
			self.path.line_to(touch.location[0],touch.location[1])
		elif self.tool == "rectangle":
			self.path.fill()
			self.rectPrevPoint = touch.location
	def touch_moved(self, touch):
		if self.tool == "brush":
			self.path.line_to(touch.location[0],touch.location[1])
		elif self.tool == "rectangle":
			ui.set_color(self.color)
			self.path.fill()
			self.path.rect(self.rectPrevPoint[0],self.rectPrevPoint[1],touch.location[0],touch.location[1])
		self.update_paper()
	def touch_ended(self, touch):
		pass
		
	def update_paper(self):
		previousImage = self.canvas.image
		with ui.ImageContext(self.width,self.height) as newImageCtx:
			if previousImage:
				previousImage.draw()
			ui.set_color(self.color)
			self.path.stroke()
			self.canvas.image = newImageCtx.get_image()
			
	def get_image(self):
		return self.canvas.image
		
	def share_image(self, sender):
		dialogs.share_image(self.canvas.image)
		
	def clear_image(self, sender):
		with ui.ImageContext(self.width,self.height) as setup:
			self.background = ui.Path()
			ui.set_color(self.bg_color)
			ui.fill_rect(0,0,self.width,self.height)
			bg = self.background.rect(0,0,self.width,self.height)
			self.background = setup
			self.canvas.image = setup.get_image()
			
imageContainer = (0,0,ui.get_screen_size()[0],ui.get_screen_size()[1]-114)

foundx = (imageContainer[2]-int(popup["Width"]))/2
foundy = (imageContainer[3]-int(popup["Height"]))/2

drawCanvas = Paper((foundx,foundy,int(popup["Width"]),int(popup["Height"])))

def change_utensil(sender):
	if sender.title == "ERASE":
		sender.title = "BRUSH"
		global CURRENTCOLOR
		CURRENTCOLOR = drawCanvas.color
		drawCanvas.color = "white"
		drawCanvas.tool = "brush"
	elif sender.title == "BRUSH":
		sender.title = "RECT"
		drawCanvas.color = CURRENTCOLOR
	elif sender.title == "RECT":
		sender.title = "ERASE"
		drawCanvas.tool = "rectangle"
def change_color(sender):
	colors = ["black","grey","blue","pink","red","green","teal","turquoise","brown","dodgerblue","purple"]
	endList = []
	for color in colors:
		endList.append({"title":color,"image":ui.Image('iob:record_24')})
	colorSwitcher = dialogs.list_dialog("Colors",endList)
	if colorSwitcher is not None:
		sender.tint_color = colorSwitcher["title"].lower()
		drawCanvas.color = colorSwitcher["title"].lower()
def more(sender):
	paperSection = ("Brush",[{"title":"Color","icon":ui.Image('iob:record_24'),"placeholder":"Enter a CSS value","type":"text","tint_color":drawCanvas.color,"value":drawCanvas.color},{"title":"Size","placeholder":str(drawCanvas.brush_size),"type":"number"}])
	morePopup = dialogs.form_dialog("More",sections=[paperSection])
	if morePopup != None:
		if morePopup["Size"] != "":
			drawCanvas.brush_size = int(morePopup["Size"])
		colorbtn.tint_color = morePopup["Color"]
		drawCanvas.color = morePopup["Color"]
def color_palette(sender):
	def openPalette():
		palette.frame = (0,ss[1]-263,ss[0],200)
	ui.animate(openPalette,0.6)
	
toolbar = ui.View()
toolbar.frame = (0,ss[1]-114,ss[0],50)
toolbar.background_color = '#ff5e5e'
toolbar.name = "toolbar"
clearbtn = ui.Button()
clearbtn.action = drawCanvas.clear_image
clearbtn.frame = (buttonWidth*3,0,buttonWidth,50)
clearbtn.image = ui.Image('iow:close_24')
clearbtn.tint_color = "white"
utensilbtn = ui.Button()
utensilbtn.action = change_utensil
utensilbtn.frame = (buttonWidth*2,0,buttonWidth,50)
utensilbtn.title = "ERASE"
utensilbtn.tint_color = "white"
utensilbtn.font = ('<System-Bold>',14)
colorbtn = ui.Button()
colorbtn.action = color_palette
colorbtn.frame = (buttonWidth,0,buttonWidth,50)
colorbtn.image = ui.Image('iob:record_24')
colorbtn.tint_color = "black"
settingsbtn = ui.Button()
settingsbtn.action = more
settingsbtn.frame = (0,0,buttonWidth,50)
settingsbtn.image = ui.Image('iow:more_32')
settingsbtn.tint_color = "white"
toolbar.add_subview(clearbtn)
toolbar.add_subview(utensilbtn)
toolbar.add_subview(colorbtn)
toolbar.add_subview(settingsbtn)

sharebtn = ui.ButtonItem()
sharebtn.image = ui.Image('iow:ios7_upload_outline_24')
sharebtn.tint_color = "white"
sharebtn.action = drawCanvas.share_image

if ".png" not in popup["Name"]:
	popup["Name"] += ".png"
	
root = ui.View()
root.frame = (0,0,ss[0],ss[1])
root.name = popup["Name"]
root.background_color = '#f5f5f5'

palette = ui.ScrollView()
palette.background_color = "white"

allColors = ["black","red","blue","green","yellow","purple","dodgerblue","lime","pink","hotpink","turquoise","teal","brown","grey","lightgrey","orange"]

palette.frame = (0,ss[1],ss[0],200)
palette.shows_horizontal_scroll_indicator = True
palette.shows_vertical_scroll_indicator = False
palette.directional_lock_enabled = True
palette.name = "palette"
palette.content_size = (20+(270*len(allColors)),200)

currentPosition = [20,20]

for color in allColors:
	if color == CURRENTCOLOR:
		using = True
	else:
		using = False
	newCard = PaletteColor((currentPosition[0],currentPosition[1],250,160),color,using)
	palette.add_subview(newCard)
	currentPosition[0] += 270
	
root.add_subview(toolbar)
root.add_subview(drawCanvas)
root.add_subview(palette)

#imageContainer.add_subview(drawCanvas)

root.right_button_items = [sharebtn]
root.present(title_bar_color='#ff5e5e',title_color="white")

