from __future__ import print_function
# https://gist.github.com/omz/6855c10632c286401f9d

# coding: utf-8
# Batch-upload script for how-old.net (Pythonista)

import photos
import requests
import json
import ui
from io import BytesIO

result_size = 320
# Set to True to upload full-size images (takes longer):
upload_originals = False
# Only applies if upload_originals is False:
jpeg_quality = 70

def main():
	images = photos.pick_image(multi=True, original=upload_originals, raw_data= upload_originals)
	if images is None:
		return
	for i, img in enumerate(images):
		print('Uploading image %i/%i...' % (i+1, len(images)))
		if not upload_originals:
			b = BytesIO()
			img.save(b, 'JPEG', quality=jpeg_quality)
			data = b.getvalue()
		else:
			data = img
		r = requests.post('http://how-old.net/Home/Analyze?isTest=False', files={'file': ('someimage.jpg', data)})
		d = json.loads(json.loads(r.text))
		faces = d.get('Faces')
		ui_img = ui.Image.from_data(data)
		scale = result_size / max(ui_img.size)
		w, h = ui_img.size[0] * scale, ui_img.size[1] * scale
		with ui.ImageContext(w, h) as ctx:
			ui_img.draw(0, 0, w, h)
			for face in faces:
				rect = [float(face['faceRectangle'][key]) * scale for key in ['left', 'top', 'width', 'height']]
				caption_rect = (rect[0], rect[1], max(40, rect[2]), 16)
				ui.set_color((0, 0, 0, 0.5))
				ui.Path.rect(*rect).stroke()
				ui.fill_rect(*caption_rect)
				attrs = face['attributes']
				age = attrs['age']
				if age % 1.0 == 0:
					age = int(age)
				caption = '%s (%s)' % (age, attrs['gender'][0])
				ui.draw_string(caption, caption_rect, color='white')
			result_img = ctx.get_image()
			result_img.show()
			if faces:
				faces_str = ', '.join(['%s (%s)' % (face['attributes']['age'], face['attributes']['gender']) for face in faces])
				print('%i face%s: %s' % (len(faces), 's' if len(faces) != 1 else '', faces_str))
			else:
				print('No faces found')
	print('Done')

if __name__ == '__main__':
	main()