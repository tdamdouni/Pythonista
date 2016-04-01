#Run this file

import ui, photos, time, console, dialogs, _dialogs
from io import BytesIO
from PIL import Image

from Image2ASCII import image2ASCII, RenderASCII
from ShadowView import ShadowView

def pil_to_ui(img):
	b = BytesIO()
	img.save(b, "PNG")
	data = b.getvalue()
	b.close()
	return ui.Image.from_data(data)


@ui.in_background
def imagetake(sender):
	im = photos.capture_image()
	if im:
		rootView.remove_subview(view1)
		main(im)

@ui.in_background
def imagepick(sender):
	im = photos.pick_image()
	if im:
		main(im)
		rootView.remove_subview(view1)
	

def segaction(sender):
	if sc.selected_index == 0:
		view2.add_subview(tshare)
		view2.remove_subview(ishare)
	elif sc.selected_index == 1:
		view2.add_subview(ishare)
		view2.remove_subview(tshare)

def pulldown():
	view2.y = 0

@ui.in_background
def exportt(sender):
	dialogs.share_text(out)

@ui.in_background	
def exporti(sender):
	console.show_activity()
	ishare['colorbox'].end_editing()
	
	color = ishare['colorbox'].text
	
	if color != '':
		if not color.startswith('#'):
			color = '#'+color
		if len(color) != 7:
			raise ValueError('Must be hexidecimal')
		im = RenderASCII(out, bgcolor=color)
		i.image = pil_to_ui(im)
		rootView.background_color = color
		view2.draw()
		
		
	else:
		im = outim
	
	
	b = BytesIO()
	im.save(b, 'PNG')
	img_data = b.getvalue()
	
	console.hide_activity()
	
	_dialogs.share_image_data(img_data)

def main(im):
	global out
	out = image2ASCII(im)
	global outim
	outim = RenderASCII(out)
	
	rootView.background_color = 0.92
	
	global i
	i = ui.ImageView()
	
	i.frame = (0, 10, 1024, 768)
	i.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
	
	i.image = pil_to_ui(outim)
	rootView.add_subview(i)
	
	close.bring_to_front()
	
	view2.remove_subview(ishare)
	view2.x = 247
	view2.y = -285
	rootView.add_subview(view2)
	
	time.sleep(1.5)
	ui.animate(pulldown, 1)
	


rootView = ui.View(frame=(0, 0, 1024, 768))




#Build view1
view1 = ui.View(frame=(0, 0, 1024, 768))

pick = ui.Button(frame=(206,293,200,200), name='pickimage')
pick.image = ui.Image.named('ionicons-image-256')
pick.action = imagepick
pick.tint_color = '#b6b6b6'

take = ui.Button(frame=(618,293,200,200), name='takephoto')
take.image = ui.Image.named('ionicons-camera-256')
take.action = imagetake
take.tint_color = '#b6b6b6'

view1.add_subview(take)
view1.add_subview(pick)

rootView.add_subview(view1)


#Build view2
view2 = ui.load_view('Popup.pyui')
view2.background_color = (0.93,0.93,0.93,0.0)

ishare = view2['ShareImage']
ishare['colorbox'].autocapitalization_type = ui.AUTOCAPITALIZE_NONE
tshare = view2['ShareText']
sc = view2['segcon']
sc.action = segaction


close = ui.Button(frame=(992,20,24,24))
close.image = ui.Image.named('ionicons-close-24')
close.action = lambda sender: sender.superview.close()
close.tint_color = '#b6b6b6'

rootView.add_subview(close)
rootView.present('full_screen', hide_title_bar=True)
