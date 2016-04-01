ui.ACTIVITY_INDICATOR_STYLE_GRAY ,ui.ACTIVITY_INDICATOR_STYLE_WHITE ,
ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE,ui.ALIGNMENTS ,ui.ALIGN_CENTER ,
ui.ALIGN_JUSTIFIED,ui.ALIGN_LEFT ,ui.ALIGN_NATURAL ,ui.ALIGN_RIGHT ,
ui.AUTOCAPITALIZE_ALL,ui.AUTOCAPITALIZE_NONE ,ui.AUTOCAPITALIZE_SENTENCES ,
ui.AUTOCAPITALIZE_WORDS,ui.BLEND_CLEAR ,ui.BLEND_COLOR ,ui.BLEND_COLOR_BURN ,
ui.BLEND_COLOR_DODGE,ui.BLEND_COPY ,ui.BLEND_DARKEN ,ui.BLEND_DESTINATION_ATOP ,
ui.BLEND_DESTINATION_IN,ui.BLEND_DESTINATION_OUT ,ui.BLEND_DESTINATION_OVER ,
ui.BLEND_DIFFERENCE,ui.BLEND_EXCLUSION ,ui.BLEND_HARD_LIGHT ,ui.BLEND_HUE ,
ui.BLEND_LIGHTEN,ui.BLEND_LUMINOSITY ,ui.BLEND_MULTIPLY ,ui.BLEND_NORMAL ,
ui.BLEND_OVERLAY,ui.BLEND_PLUS_DARKER ,ui.BLEND_PLUS_LIGHTER ,
ui.BLEND_SATURATION,ui.BLEND_SCREEN ,ui.BLEND_SOFT_LIGHT ,ui.BLEND_SOURCE_ATOP ,
ui.BLEND_SOURCE_IN,ui.BLEND_SOURCE_OUT ,ui.BLEND_XOR ,ui.COLOR_REGEX ,
ui.CONTENT_BOTTOM,ui.CONTENT_BOTTOM_LEFT ,ui.CONTENT_BOTTOM_RIGHT ,
ui.CONTENT_CENTER,ui.CONTENT_LEFT ,ui.CONTENT_REDRAW ,ui.CONTENT_RIGHT ,
ui.CONTENT_SCALE_ASPECT_FILL,ui.CONTENT_SCALE_ASPECT_FIT ,
ui.CONTENT_SCALE_TO_FILL,ui.CONTENT_TOP ,ui.CONTENT_TOP_LEFT ,
ui.CONTENT_TOP_RIGHT,ui.CORRECTION_TYPES ,ui.DATE_PICKER_MODE_COUNTDOWN ,
ui.DATE_PICKER_MODE_DATE,ui.DATE_PICKER_MODE_DATE_AND_TIME ,
ui.DATE_PICKER_MODE_TIME,ui.KEYBOARD_ASCII ,ui.KEYBOARD_DECIMAL_PAD ,
ui.KEYBOARD_DEFAULT,ui.KEYBOARD_EMAIL ,ui.KEYBOARD_NAME_PHONE_PAD ,
ui.KEYBOARD_NUMBERS,ui.KEYBOARD_NUMBER_PAD ,ui.KEYBOARD_PHONE_PAD ,
ui.KEYBOARD_TWITTER,ui.KEYBOARD_URL ,ui.KEYBOARD_WEB_SEARCH ,ui.LB_CHAR_WRAP ,
ui.LB_CLIP,ui.LB_TRUNCATE_HEAD ,ui.LB_TRUNCATE_MIDDLE ,ui.LB_TRUNCATE_TAIL ,
ui.LB_WORD_WRAP,ui.LINE_CAP_BUTT ,ui.LINE_CAP_ROUND ,ui.LINE_CAP_SQUARE ,
ui.LINE_JOIN_BEVEL,ui.LINE_JOIN_MITER ,ui.LINE_JOIN_ROUND ,ui.RECT_REGEX ,
ui.RENDERING_MODE_AUTOMATIC,ui.RENDERING_MODE_ORIGINAL ,
ui.RENDERING_MODE_TEMPLATE,

class GState (object):
	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		pass

class ImageContext (object):
	def __init__(self, width, height, scale=0.0):
		pass

	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		pass

	def get_image(self):
		pass

class ListDataSource (object):
	def __init__(self, items=None):
		pass

	def reload(self):
		pass

	def items(self):
		pass

	def items(self, value):
		pass

	def tableview_number_of_sections(self, tv):
		pass

	def tableview_number_of_rows(self, tv, section):
		pass

	def tableview_can_delete(self, tv, section, row):
		pass

	def tableview_can_move(self, tv, section, row):
		pass

	def tableview_accessory_button_tapped(self, tv, section, row):
		pass

	def tableview_did_select(self, tv, section, row):
		pass

	def tableview_move_row(self,	
 tv,	
 from_section,	
 from_row,	
 to_section,	
 to_row):
		pass

	def tableview_delete(self, tv, section, row):
		pass

	def tableview_cell_for_row(self, tv, section, row):
		pass

class ListDataSourceList (list):
	def __init__(self, seq, datasource):
		pass

	def append(self, item):
		pass

	def __setitem__(self, key, value):
		pass

	def __delitem__(self, key):
		pass

	def __setslice__(self, i, j, seq):
		pass

	def __delslice__(self, i, j):
		pass

def _bind_action(v, action_str, f_globals, f_locals, attr_name='action'):
	pass

def _str2color(color_str, default=None):
	pass

def _str2rect(rect_str):
	pass

def _view_from_dict(view_dict, f_globals, f_locals):
	pass

def in_background(fn):
	pass

	def new_fn(*args, **kwargs):
		pass

def load_view(pyui_path=None, bindings=None, stackframe=None):
	pass

def load_view_str(json_str, bindings=None, stackframe=None):
	pass

