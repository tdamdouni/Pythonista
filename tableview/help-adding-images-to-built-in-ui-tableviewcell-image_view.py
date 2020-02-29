# coding: utf-8

# https://forum.omz-software.com/topic/2863/help-adding-images-to-built-in-ui-tableviewcell-image_view

from __future__ import print_function
import ui
#import openSecretsEndpoints
import dialogs
import imageStuff

class MyTableViewDelegate (object):
	@ui.in_background
	def tableview_did_select(self, tableview, section, row):
		# Called when a row IS selected.
		print('printing...did select')
		
		handleKeys = self.data.keys()
		handleKeySection = self.data.keys()[section]
		handleAvatarURL = self.data[self.data.keys()[section]][1]
		handleRelevantTweets = self.data[self.data.keys()[section]][0]
		handleRowTweet = self.data[self.data.keys()[section]][0][row]
		
		dialogs.alert(str(self.data[self.data.keys()[section]][0][row]))
		
class MyTableViewDataSource (object):
	def tableview_number_of_sections(self,tableview):
		return len(self.data)
		
	def tableview_title_for_header(self,tableview,section):
		#return self.data.keys()[section]
		#return "Twitter Handles"
		return self.data.keys()[section]
		
	def tableview_number_of_rows(self,tableview,section):
		key = self.data.keys()[section]
		return len(self.data[key][0])
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		
		key = self.data.keys()[section]
		cell = ui.TableViewCell()
		
		cell.autoresizing ='auto'
		cell.size_to_fit()
		cell.height=50
		
		cell.text_label.text = self.data[self.data.keys()[section]][0][row]
		
		#cell.content_view.add_subview()
		#cell.image_view = imageStuff.circleMaskViewFromURL(self.data[self.data.keys()[section]][1])
		
								#ALSO TRIED THIS:
		cell.imageView = ui.ImageView()
		cell.imageView.image = imageStuff.circleMaskViewFromURL(self.data[self.data.keys()[section]][1])
		cell.imageView.present()
		
		return cell
		
def fill_data(self, tableview, data):

	self.data = data
	
	
#dataSource = openSecretsEndpoints.Candidacy().getCandidateList()
dataSource = {u'RepTimMurphy': ([u"I'm next @FoxBusiness @TeamCavuto discussing @HouseCommerce request 4 #FBI #Apple 2 appear on future of #encryption https://t.co/ZfJyV2iooe"], u'http://pbs.twimg.com/profile_images/378800000252739465/67e48a9fc07ce37c132d93cc9e4c6874_normal.jpeg'), u'RepMeehan': ([u"There's too much at stake for a standoff between Apple and the FBI. https://t.co/tke9NwSxyn &lt;--- my view on in today's @PhillyInquirer", u"In today's @PhillyInquirer: my views on the ongoing debate regarding #Apple, the #FBI and encryption: https://t.co/EIAJsB9LXQ"], u'http://pbs.twimg.com/profile_images/1388714447/MPF11_031_506_normal.jpg'), u'RepTomMarino': ([u'RT @HouseJudiciary: Apple, FBI to face off at House hearing on encryption https://t.co/xNOB3rsH37 via @USATODAY'], u'http://pbs.twimg.com/profile_images/704700495730974720/4K03J5FW_normal.jpg')}

table = dataSource[1]

OTVD = ui.TableView()
data = MyTableViewDataSource()
OTVD.delegate = MyTableViewDelegate()
OTVD.row_height = 50

OTVD.data_source = data
print(data)
print(len(table))


if len(table) >=1:
	data.fill_data(OTVD, table)
	
	OTVD.delegate.data = data.data
	
	OTVD.present()
	
	
#==============================

# coding: utf-8

# imageStuff.py

import ui
import webbrowser
#these are fillers for phhton 3 changes
try:
	import cStringIO
	print("old cString")
except ImportError:
	from io import StringIO as cStringIO
	print("new stringIO")
try:
	import urllib2
	print(urllib2)
except ImportError:
	import urllib3 as urllib2
	print((urllib3,' as urllib2'))
from PIL import Image, ImageOps, ImageDraw
import io
import Image

#url = "https://d1w2poirtb3as9.cloudfront.net/d28b29f37088409b5041.jpeg"


def circleMaskViewFromURL(url):
	url=url
	#load image from url and show it
	file=cStringIO.StringIO(urllib2.urlopen(url).read())
	
	img = Image.open(file)
	
	#begin mask creation
	bigsize = (img.size[0] * 3, img.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(img.size, Image.ANTIALIAS)
	
	img.putalpha(mask)
	
	#show final masked image
	img.show()
	img=pil2ui(img)
	
	return img
	
# pil <=> ui
def pil2ui(imgIn):
	with io.BytesIO() as bIO:
		imgIn.save(bIO, 'PNG')
		imgOut = ui.Image.from_data(bIO.getvalue())
	del bIO
	return imgOut
	
	
	
if __name__=="__main__":

	#tests
	circleMaskViewFromURL("http://vignette2.wikia.nocookie.net/jamesbond/images/3/31/Vesper_Lynd_(Eva_Green)_-_Profile.jpg/revision/latest?cb=20130506215331")
	
#==============================

cell.image_view = imageStuff.circleMaskViewFromURL(self.data[self.data.keys()[section]][1])

#==============================

cell.image_view.image = imageStuff.circleMaskViewFromURL(self.data[self.data.keys()[section]][1])

