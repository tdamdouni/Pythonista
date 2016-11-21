# https://gist.github.com/Phuket2/bbb460f97b6ba5cc8b54c10ab0b56d1a

'''
        Pythonista Forum - @Phuket2

        CSS Color Lookup - wrench item
        A very basic utility to look up a css name in a list with a filter
        function and a copy to clipbord the color, quoted.
        Only works for Python 3.xx, i think only because of the use of
        super().__init__ in the classes

        Very basic, but can be handy.  Personally, i like using css colors
        even though there is only 148 of them.

        I did not make a repo , because i want to do more. I made
        a gist because its still useful in its current state, to me anyway.

        I think and hope this will be short lived, as i think @omz will add
        css colors to the built in color picker when time permits.

        I am sure i have done some no, no's in the code. Just sick of making
        nothing.  Rather than go down all the rabbit holes trying to be
        correct, just did things in a way that were fairly straight fwd
        for me...

        I feel i have kept it pretty simple and easy to understand.  The code
        looks a little long for what it does. but its only because of
        seperating views into their own classes. while i am sure the design
        is not great, its still pretty flexible to modify, hence what looks
        like duplication and an increase in the code lines. well, thats my
        thinking anyway.

        Anyway, i have some ideas to add functionality, another panel after
        clicking the color. show the rgb values, modify the color with alpha
        settings , view text of the selected css color on a selectable
        background as a sort of preview, select colors using a slider of
        the percentage of r, g or b color components, save sets of colors that can be recalled and placed on the clipboard as a list etc...
        Just for fun
'''

# saved to..
# https://gist.github.com/b53613abe70dabca02573344f01903a9

import ui, clipboard, console

_css_colors=['rosybrown', 'antiquewhite', 'lightsteelblue', 'white', 'darkblue', 'darkviolet', 'plum', 'darkcyan', 'blanchedalmond', 'chocolate', 'sienna', 'tomato', 'peachpuff', 'lightyellow', 'bisque', 'aqua', 'oldlace', 'maroon', 'palegreen', 'chartreuse', 'darkturquoise', 'linen', 'magenta', 'lemonchiffon', 'powderblue', 'papayawhip', 'gold', 'khaki', 'lightseagreen', 'darkred', 'floralwhite', 'turquoise', 'mediumspringgreen', 'indianred', 'lightgreen', 'crimson', 'mintcream', 'lavender', 'purple', 'orchid', 'darkslateblue', 'whitesmoke', 'moccasin', 'beige', 'mistyrose', 'dodgerblue', 'hotpink', 'lightcoral', 'goldenrod', 'coral', 'cadetblue', 'black', 'mediumseagreen', 'gainsboro', 'paleturquoise', 'darkgreen', 'darkkhaki', 'mediumblue', 'dimgray', 'darkorchid', 'deeppink', 'mediumvioletred', 'lightgray', 'darkgrey', 'lightsalmon', 'lightblue', 'lightslategrey', 'slategray', 'slateblue', 'greenyellow', 'darkgray', 'lawngreen', 'cornflowerblue', 'midnightblue', 'lightpink', 'deepskyblue', 'navy', 'lightskyblue', 'darkorange', 'blueviolet', 'lightgrey', 'lightgoldenrodyellow', 'violet', 'ivory', 'mediumslateblue', 'cyan', 'rebeccapurple', 'firebrick', 'green', 'burlywood', 'wheat', 'mediumpurple', 'mediumturquoise', 'skyblue', 'peru', 'forestgreen', 'royalblue', 'aquamarine', 'silver', 'olive', 'palevioletred', 'mediumorchid', 'darkslategray', 'darkslategrey', 'steelblue', 'olivedrab', 'lime', 'orangered', 'grey', 'sandybrown', 'slategrey', 'pink', 'blue', 'palegoldenrod', 'ghostwhite', 'brown', 'darkseagreen', 'saddlebrown', 'salmon', 'cornsilk', 'red', 'snow', 'tan', 'aliceblue', 'yellow', 'yellowgreen', 'springgreen', 'thistle', 'navajowhite', 'teal', 'lightcyan', 'orange', 'darksalmon', 'mediumaquamarine', 'darkolivegreen', 'lavenderblush', 'indigo', 'fuchsia', 'honeydew', 'azure', 'lightslategray', 'seagreen', 'gray', 'dimgrey', 'limegreen', 'darkmagenta', 'darkgoldenrod', 'seashell']

def create_swatch_image(color, w=32):
	# create a ui.Image of a named color
	# this is a little over the top, i did it this way both as a test
	# and to fit into the item spec of ui.ListSource.
	# only 148 css color entries, so its ok.
	s = ui.Path.oval(0, 0, w, w)
	with ui.ImageContext(w, w) as ctx:
		ui.set_color(color)
		s.fill()
		return ctx.get_image()
		
		
class MyDataClass(object):
	# supplies our list with records that are formatted for
	# ui.ListDataSource. Because we create swatch images, this is a good
	# idea. All the swatchs' are created once and kept.
	def __init__(self, *args, **kwargs):
		self.data = self._my_data(_css_colors)
		
	def _my_data(self, lst):
		# ListDataSource format
		return [{'title': clr,
		'image': create_swatch_image(clr, w=24),
		'accessory_type': 'detail_button'
		}for i, clr in enumerate(sorted(lst))]
		
	def filter(self, filter=''):
		# return the data, if filter is not passed, all records returned
		# else a subset of records are returned based on the filter.
		return [d for d in self.data if filter in d['title']]
		
		
def make_ui_object(ui_type, *args, **kwargs):
	# utility to create ui object with all kwargs
	obj = ui_type()
	for k, v in kwargs.items():
		if hasattr(obj, k):
			setattr(obj, k, v)
	return obj
	
	
class Panel(ui.View):
	# a base class, not doing much, can do more.
	def __init__(self, p, h, *args, **kwargs):
		'''
		p = the intended parent view
		h = the height of the panel
		'''
		# set the frame before calling super incase kwargs contridicts
		# the normal setup
		f = ui.Rect(0, 0, p.width, h)
		self.frame = f
		super().__init__(*args, **kwargs)
		self.default_action = None
		
		# add ourself to the parent...recalcitrant child
		# probably not good form to do this, not sure
		p.add_subview(self)
		
		
class SearchPanel(Panel):
	def __init__(self, p, h, *args, **kwargs):
		super().__init__(p, h, *args, **kwargs)
		self.name = 'sp'
		self.bg_color = 'coral'
		self.flex = 'wrb'
		
		self.make_view()
		
	def make_view(self):
		txtfld = make_ui_object(ui.TextField)
		txtfld.placeholder = 'Filter'
		txtfld.clear_button_mode = 'always'
		txtfld.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
		txtfld.spellchecking_type = False
		
		txtfld.frame = self.bounds.inset(8, 4)
		txtfld.delegate = self
		txtfld.flex = 'wrb'
		self.add_subview(txtfld)
		
	def textfield_did_change(self, textfield):
		# send the contents of search field to our default_action if
		# it has been set.
		if self.default_action:
			self.default_action(self, textfield.text)
			
			
class ListPanel(Panel):
	def __init__(self, p, h, *args, **kwargs):
		super().__init__(p, h, *args, **kwargs)
		self.name = 'lp'
		self.dc = MyDataClass()
		self.lds = None
		
		self.make_view()
		
	def make_view(self):
		tv = ui.TableView(name='lst', frame=self.bounds)
		lds = ui.ListDataSource(items=self.dc.data)
		lds.delete_enabled = False
		lds.action = self.action
		lds.accessory_action = self.accessory_action
		tv.data_source = lds
		
		tv.flex = 'whlrtb'
		tv.delegate = lds
		self.add_subview(tv)
		self.lds = lds
		
	def filter(self, text):
		'''
		filter the list, very crude...
		'''
		tb = self['lst']
		self.lds.items = self.dc.filter(text)
		tb.content_offset = (0, 0)
		
	@property
	def num_records(self):
		return len(self.lds.items)
		
	def accessory_action(self, sender):
		if self.default_action:
			item = sender.items[sender.tapped_accessory_row]
			self.default_action(self, item['title'])
			
	def action(self, sender):
		# maybe will use later. But dont want to use this to copy the
		# color to the clipboard.
		pass
		
		
class FooterPanel(Panel):
	'''
	for now, just shows a label with the number of items displayed
	in the list.
	'''
	def __init__(self, p, h, *args, **kwargs):
		super().__init__(p, h, *args, **kwargs)
		self.name = 'fp'
		self.make_view()
		self.bg_color = 'coral'
		self.flex = 'wlt'
		
	def make_view(self):
		lb = make_ui_object(ui.Label, name='msg_lb', frame=self.frame)
		lb.text_color = 'white'
		lb.font = ('Avenir Next Condensed', 22)
		lb.alignment = ui.ALIGN_CENTER
		lb.center = self.center
		lb.flex = 'wlt'
		self.add_subview(lb)
		
	@property
	def msg_text(self):
		return self['msg_lb'].text
		
	@msg_text.setter
	def msg_text(self, msg_text):
		self['msg_lb'].text = msg_text
		
		
class MyClass(ui.View):
	# the presentation class so to speak
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		# create the views, only sized. Positioning happens in layout
		sp = SearchPanel(self, 44)
		lp = ListPanel(self, 300)
		fp = FooterPanel(self, 32)
		
		# set callbacks
		sp.default_action = self.cb_search_text
		lp.default_action = self.cb_info_button
		
		self['fp'].msg_text = 'Items - {}'.format(self['lp'].num_records)
		
	def layout(self):
		'''
		position the views.
		manually resize the height of the listpanel
		should do all this with flex, later...
		'''
		v = self['sp']
		v.y = 0
		
		v = self['fp']
		v.y = self.bounds.max_y - v.height
		
		v = self['lp']
		v.y = self['sp'].bounds.max_y
		v.height = self.height - (self['sp'].height + self['fp'].height)
		
	def cb_search_text(self, sender, text):
		# the searchpanel calling us with the text in the textfield
		self['lp'].filter(text.lower())
		self['fp'].msg_text = 'Items - {}'.format(self['lp'].num_records)
		
	def cb_info_button(self, sender, text):
		# the listpanel calling us with the text from the ui.TableView
		quote = "'"
		clipboard.set('{quote}{item}{quote}'.format(item=text,
		quote=quote))
		console.hud_alert(text + '-Copied')
		self.close()
		
		
if __name__ == '__main__':
	w = 320
	h = ui.get_screen_size()[1]*.6
	f = (0, 0, w, h)
	style = 'popover'
	title_color = 'white'
	title_bar_color = 'coral'
	animated = False
	
	# just added this...
	if not style is 'sheet' and not style is 'popover':
		w,h = ui.get_screen_size()
		f = (0, 0, w, h)
		
		
		
	mc = MyClass(name='CSS Color Lookup', frame=f, bg_color='white')
	
	mc.present(style=style, animated=animated,
	title_color=title_color,
	title_bar_color=title_bar_color)

