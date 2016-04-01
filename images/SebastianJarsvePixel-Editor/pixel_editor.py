
import console, scene, photos, clipboard, ui, io, os.path, Image, numpy

def pil_to_ui(img):
	with io.BytesIO() as bIO:
		img.save(bIO, 'png')
		return ui.Image.from_data(bIO.getvalue())
	
def ui_to_pil(img):
	return Image.open(io.BytesIO(img.to_png()))
	
def crop_image(image):
	image = ui_to_pil(image)
	image_data = numpy.asarray(image)
	image_data_bw = image_data.max(axis=2)
	non_empty_columns = numpy.where(image_data_bw.max(axis=0)>0)[0]
	non_empty_rows = numpy.where(image_data_bw.max(axis=1)>0)[0]
	cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
	image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
	new_image = pil_to_ui(Image.fromarray(image_data_new))
	return new_image

class Pixel (scene.Rect):
	def __init__(self, x, y, w, h):
		scene.Rect.__init__(self, x, y, w, h)
		self.colors = [(0, 0, 0, 0)]
		
	def used(self):
		return len(self.colors) > 1 and self.colors[-1] != (0, 0, 0, 0)
		
	def undo(self):
		if len(self.colors) > 1:
			self.colors.pop()

class PixelEditor(ui.View):
	def did_load(self):
		self.row = self.column = 16
		self.pixels = []
		self.pixel_path = []
		self.image_view = self.create_image_view()
		self.grid_layout = self.create_grid_layout()
		self.current_color = (0, 0, 0, 1)
		self.mode = 'pencil'
		self.auto_crop_image = False 
		
	def has_image(self):
		if self.pixel_path:
			if [p for p in self.pixel_path if p.used()]:
				return True 
		return False 

	def set_image(self, image=None):
		image = image or self.create_new_image()
		self.image_view.image = self.superview['preview'].image = image
		
	def get_image(self):
		image = self.image_view.image
		if self.auto_crop_image:
			return crop_image(image)
		return image
		
	def add_history(self, pixel):
		self.pixel_path.append(pixel)

	def create_grid_image(self):
		s = self.width/self.row if self.row > self.column else self.height/self.column
		path = ui.Path.rect(0, 0, *self.frame[2:])
		with ui.ImageContext(*self.frame[2:]) as ctx:
			ui.set_color((0, 0, 0, 0))
			path.fill()
			path.line_width = 2
			for y in xrange(self.column):
				for x in xrange(self.row):
					pixel = Pixel(x*s, y*s, s, s)
					path.append_path(ui.Path.rect(*pixel))
					self.pixels.append(pixel)
			ui.set_color('gray')
			path.stroke()
			return ctx.get_image()

	def create_grid_layout(self):
		image_view = ui.ImageView(frame=self.bounds)
		image_view.image = self.create_grid_image()
		self.add_subview(image_view)
		return image_view

	def create_image_view(self):
		image_view = ui.ImageView(frame=self.bounds)
		image_view.image = self.create_new_image()
		self.add_subview(image_view)
		return image_view

	def create_new_image(self):
		path = ui.Path.rect(*self.frame)
		with ui.ImageContext(self.width, self.width) as ctx:
			ui.set_color((0, 0, 0, 0))
			path.fill()
			return ctx.get_image()

	def create_image_from_history(self):
		path = ui.Path.rect(*self.frame)
		with ui.ImageContext(self.width, self.height) as ctx:
			for pixel in self.pixel_path:
				if not pixel.used():
					continue 
				ui.set_color(pixel.colors[-1])
				pixel_path = ui.Path.rect(*pixel)
				pixel_path.line_width = 0.5
				pixel_path.fill()
				pixel_path.stroke()
			img = ctx.get_image()
			return img
			
	def reset(self, row=None, column=None):
		self.row = row or self.row
		self.column = column or self.column
		self.pixels = []
		self.pixel_path = []
		self.grid_layout.image = self.create_grid_image()
		self.set_image()

	def undo(self):
		if self.pixel_path:
			pixel = self.pixel_path.pop()
			pixel.undo()
			self.set_image(self.create_image_from_history())

	def pencil(self, pixel):
		if pixel.colors[-1] != self.current_color:
			if self.current_color != (0, 0, 0, 0):
				pixel.colors.append(self.current_color)
				self.pixel_path.append(pixel)
				old_img = self.image_view.image
				path = ui.Path.rect(*pixel)
				with ui.ImageContext(self.width, self.height) as ctx:
					if old_img:
						old_img.draw()
					ui.set_color(self.current_color)
					pixel_path = ui.Path.rect(*pixel)
					pixel_path.line_width = 0.5
					pixel_path.fill()
					pixel_path.stroke()
					self.set_image(ctx.get_image())

	def eraser(self, pixel):
		if pixel.used():
			pixel.colors.append((0, 0, 0, 0))
			self.pixel_path.append(pixel)
			img = self.create_image_from_history()
			self.set_image(self.create_image_from_history())

	def color_picker(self, pixel):
		self.current_color = pixel.colors[-1]
		self.superview['colors'].set_color(pixel.colors[-1])

	def action(self, touch):
		p = scene.Point(*touch.location)
		for pixel in self.pixels:
			if p in pixel:
				eval('self.{}(pixel)'.format(self.mode))

	def touch_began(self, touch):
		self.action(touch)

	def touch_moved(self, touch):
		self.action(touch)

class ColorView (ui.View):
	def did_load(self):
		self.color = {'r':0, 'g':0, 'b':0, 'a':1}
		for subview in self.subviews:
			self.init_action(subview)

	def init_action(self, subview):
		if hasattr(subview, 'action'):
			subview.action = self.choose_color if subview.name != 'clear' else self.clear_user_palette
		if hasattr(subview, 'subviews'):
			for sv in subview.subviews:
				self.init_action(sv)

	def get_color(self):
		return tuple(self.color[i] for i in 'rgba')

	def set_color(self, color=None):
		color = color or self.get_color()
		for i, v in enumerate('rgba'):
			self[v].value = color[i]
			self.color[v] = color[i]
		rgb_to_hex = tuple(int(i*255) for i in color[:3])
		self['color_input'].text = ''.join('#{:02X}{:02X}{:02X}'.format(*rgb_to_hex))
		self['current_color'].background_color = color
		self.superview['editor'].current_color = color

	@ui.in_background
	def choose_color(self, sender):
		if sender.name in self.color:
			self.color[sender.name] = sender.value
			self.set_color()
		elif sender in self['palette'].subviews:
			self.set_color(sender.background_color)
		elif sender.name == 'color_input':
			try: 
				c = sender.text if sender.text.startswith('#') else eval(sender.text)
				v = ui.View(background_color=c)
				self['color_input'].text = str(v.background_color)
				self.set_color(v.background_color)
			except Exception as e:
				console.hud_alert('Invalid Color', 'error')

class ToolbarView (ui.View):
	def did_load(self):
		self.pixel_editor = self.superview['editor']
		for subview in self.subviews:
			self.init_actions(subview)

	def init_actions(self, subview):
		if hasattr(subview, 'action'):
			if hasattr(self, subview.name):
				subview.action = eval('self.{}'.format(subview.name))
			else: 
				subview.action = self.set_mode
		if hasattr(subview, 'subviews'):
			for sv in subview.subviews:
				self.init_actions(sv)
				
	def show_error(self):
		console.hud_alert('Editor has no image', 'error', 0.8)
		
	@ui.in_background		
	def trash(self, sender):
		if self.pixel_editor.has_image():
			msg = 'Are you sure you want to clear the pixel editor? Image will not be saved.'
			if console.alert('Trash', msg, 'Yes'):
				self.pixel_editor.reset()
		else: 
			self.show_error()
			
	@ui.in_background
	def save(self, sender):
		if self.pixel_editor.has_image():
			image = self.pixel_editor.get_image()
			option = console.alert('Save Image', '', 'Camera Roll', 'New File', 'Copy image')
			if option == 1:
				photos.save_image(image)
				console.hud_alert('Saved to cameraroll')
			elif option == 2:
				name = 'image_{}.png'
				get_num = lambda x=1: get_num(x+1) if os.path.isfile(name.format(x)) else x
				file_name = name.format(get_num())
				with open(file_name, 'w') as f:
					ui_to_pil(image).save(f, 'png')
				console.hud_alert('Image saved as "{}"'.format(file_name))
			elif option == 3:
				clipboard.set_image(image, format='png')
				console.hud_alert('Copied')
		else: 
			self.show_error()
			
	def undo(self, sender):
		self.pixel_editor.undo()
				
	@ui.in_background
	def preview(self, sender):
		if self.pixel_editor.has_image():
			v = ui.ImageView(frame=(100,400,512,512))
			v.image = self.pixel_editor.get_image()
			v.width, v.height = v.image.size
			v.present('popover', popover_location=(200, 275), hide_title_bar=True)
		else: 
			self.show_error()
			
	def crop(self, sender):
		if not self.pixel_editor.auto_crop_image:
			sender.background_color = '#4C4C4C'
			sender.tint_color = 'white'
			self.pixel_editor.auto_crop_image = True
		else: 
			sender.background_color = (0, 0, 0, 0)
			sender.tint_color = 'black'
			self.pixel_editor.auto_crop_image = False 

	@ui.in_background
	def pixels(self, sender):
		if self.pixel_editor.has_image():
			console.hud_alert("Can't chage size while editing.", "error")
			return 
		try: 
			size = eval(sender.text)
			row, column = (size if isinstance(size, tuple) else (size, size))
			self.pixel_editor.reset(row, column)
			self['pixels'].text = '{},{}'.format(row, column)
		except Exception as e:
			console.hud_alert('Invalid size', 'error', 0.8)
		
	def set_mode(self, sender):
		self.pixel_editor.mode = sender.name
		for b in self['tools'].subviews:
			b.background_color = tuple((0, 0, 0, 0))
		sender.background_color = '#4C4C4C'


ui.load_view('pixel_editor').present(orientations=['portrait'])
