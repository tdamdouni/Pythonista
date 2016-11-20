#!python2
# coding: utf-8

# https://gist.github.com/anonymous/1447d2196a3e11088f4d4fcc9f5174bf

# https://forum.omz-software.com/topic/3323/paper-for-uis/3

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
			
			self.color = "black"
			self.brush_size = 8
			
			self.path = None
			
	def touch_began(self, touch):
		self.path = ui.Path()
		self.path.line_cap_style = ui.LINE_CAP_ROUND
		self.path.line_join_style = ui.LINE_JOIN_ROUND
		self.path.line_width = self.brush_size
		self.path.move_to(touch.location[0],touch.location[1])
		self.path.line_to(touch.location[0],touch.location[1])
		self.path.fill()
	def touch_moved(self, touch):
		self.path.line_to(touch.location[0],touch.location[1])
		self.path.fill()
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
		sender.title = "DRAW"
		global CURRENTCOLOR
		CURRENTCOLOR = drawCanvas.color
		drawCanvas.color = "white"
	elif sender.title == "DRAW":
		sender.title = "ERASE"
		drawCanvas.color = CURRENTCOLOR
def change_color(sender):
	colorSwitcher = dialogs.list_dialog("Colors",["Black","Red","Green","Blue","Yellow"])
	if colorSwitcher is not None:
		sender.tint_color = colorSwitcher.lower()
		drawCanvas.color = colorSwitcher.lower()
def more(sender):
	paperSection = ("Brush",[{"title":"Color","icon":ui.Image('iob:record_24'),"placeholder":"Enter a CSS value","type":"text","tint_color":drawCanvas.color,"value":drawCanvas.color},{"title":"Size","placeholder":str(drawCanvas.brush_size),"type":"number"}])
	morePopup = dialogs.form_dialog("More",sections=[paperSection])
	if morePopup != None:
		if morePopup["Size"] != "":
			drawCanvas.brush_size = int(morePopup["Size"])
		colorbtn.tint_color = morePopup["Color"]
		drawCanvas.color = morePopup["Color"]
		
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
colorbtn.action = change_color
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

root.add_subview(toolbar)
root.add_subview(drawCanvas)

#imageContainer.add_subview(drawCanvas)

root.right_button_items = [sharebtn]
root.present(title_bar_color='#ff5e5e',title_color="white")

