# https://forum.omz-software.com/topic/2447/hackathon-challenge-set-by-ccc-started-new-thread

# Constants:


ACTIVITY_INDICATOR_STYLE_GRAY = 2
ACTIVITY_INDICATOR_STYLE_WHITE = 1
ACTIVITY_INDICATOR_STYLE_WHITE_LARGE = 0
ALIGN_CENTER = 1
ALIGN_JUSTIFIED = 3
ALIGN_LEFT = 0
ALIGN_NATURAL = 4
ALIGN_RIGHT = 2
AUTOCAPITALIZE_ALL = 3
AUTOCAPITALIZE_NONE = 0
AUTOCAPITALIZE_SENTENCES = 2
AUTOCAPITALIZE_WORDS = 1
BLEND_CLEAR = 16
BLEND_COLOR = 14
BLEND_COLOR_BURN = 7
BLEND_COLOR_DODGE = 6
BLEND_COPY = 17
BLEND_DARKEN = 4
BLEND_DESTINATION_ATOP = 24
BLEND_DESTINATION_IN = 22
BLEND_DESTINATION_OUT = 23
BLEND_DESTINATION_OVER = 21
BLEND_DIFFERENCE = 10
BLEND_EXCLUSION = 11
BLEND_HARD_LIGHT = 9
BLEND_HUE = 12
BLEND_LIGHTEN = 5
BLEND_LUMINOSITY = 15
BLEND_MULTIPLY = 1
BLEND_NORMAL = 0
BLEND_OVERLAY = 3
BLEND_PLUS_DARKER = 26
BLEND_PLUS_LIGHTER = 27
BLEND_SATURATION = 13
BLEND_SCREEN = 2
BLEND_SOFT_LIGHT = 8
BLEND_SOURCE_ATOP = 20
BLEND_SOURCE_IN = 18
BLEND_SOURCE_OUT = 19
BLEND_XOR = 25
CONTENT_BOTTOM = 6
CONTENT_BOTTOM_LEFT = 11
CONTENT_BOTTOM_RIGHT = 12
CONTENT_CENTER = 4
CONTENT_LEFT = 7
CONTENT_REDRAW = 3
CONTENT_RIGHT = 8
CONTENT_SCALE_ASPECT_FILL = 2
CONTENT_SCALE_ASPECT_FIT = 1
CONTENT_SCALE_TO_FILL = 0
CONTENT_TOP = 5
CONTENT_TOP_LEFT = 9
CONTENT_TOP_RIGHT = 10
DATE_PICKER_MODE_COUNTDOWN = 3
DATE_PICKER_MODE_DATE = 1
DATE_PICKER_MODE_DATE_AND_TIME = 2
DATE_PICKER_MODE_TIME = 0
KEYBOARD_ASCII = 1
KEYBOARD_DECIMAL_PAD = 8
KEYBOARD_DEFAULT = 0
KEYBOARD_EMAIL = 7
KEYBOARD_NAME_PHONE_PAD = 6
KEYBOARD_NUMBERS = 2
KEYBOARD_NUMBER_PAD = 4
KEYBOARD_PHONE_PAD = 5
KEYBOARD_TWITTER = 9
KEYBOARD_URL = 3
KEYBOARD_WEB_SEARCH = 10
LB_CHAR_WRAP = 1
LB_CLIP = 2
LB_TRUNCATE_HEAD = 3
LB_TRUNCATE_MIDDLE = 5
LB_TRUNCATE_TAIL = 4
LB_WORD_WRAP = 0
LINE_CAP_BUTT = 0
LINE_CAP_ROUND = 1
LINE_CAP_SQUARE = 2
LINE_JOIN_BEVEL = 2
LINE_JOIN_MITER = 0
LINE_JOIN_ROUND = 1
RENDERING_MODE_AUTOMATIC = 0
RENDERING_MODE_ORIGINAL = 1
RENDERING_MODE_TEMPLATE = 2


# Functions:


def _bind_action(*args):
	pass
def _str2color(*args):
	pass
def _str2rect(*args):
	pass
def _view_from_dict(*args):
	pass
def in_background(*args):
	pass
def load_view(*args):
	pass
def load_view_str(*args):
	pass


# Classes:


class ActivityIndicator (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.hides_when_stopped = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.style = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def start(self, *args):
		pass
	def start_animating(self, *args):
		pass
	def stop(self, *args):
		pass
	def stop_animating(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class Button (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.background_image = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.enabled = None
		self.flex = None
		self.font = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.image = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.title = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class ButtonItem (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.enabled = None
		self.image = None
		self.tint_color = None
		self.title = None



class DatePicker (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.countdown_duration = None
		self.date = None
		self.enabled = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.mode = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class GState (object):
	def __init__(self, *args):
		pass
		self.__weakref__ = None



class Image (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.rendering_mode = None
		self.scale = None
		self.size = None
	def clip_to_mask(self, *args):
		pass
	def draw(self, *args):
		pass
	def draw_as_pattern(self, *args):
		pass
	def from_data(cls, *args):
		pass
	def from_image_context(cls, *args):
		pass
	def named(cls, *args):
		pass
	def resizable_image(self, *args):
		pass
	def show(self, *args):
		pass
	def to_png(self, *args):
		pass
	def with_rendering_mode(self, *args):
		pass



class ImageContext (object):
	def __init__(self, *args):
		pass
		self.__weakref__ = None



class ImageView (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.image = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def load_from_url(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class Label (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alignment = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.flex = None
		self.font = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.line_break_mode = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.number_of_lines = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.text = None
		self.text_color = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class ListDataSource (object):
	def __init__(self, *args):
		pass
		self.__weakref__ = None
		self.items = None



class ListDataSourceList (object):
	def __init__(self, *args):
		pass
		self.__weakref__ = None
	def count(self, *args):
		pass
	def extend(self, *args):
		pass
	def index(self, *args):
		pass
	def insert(self, *args):
		pass
	def pop(self, *args):
		pass
	def remove(self, *args):
		pass
	def reverse(self, *args):
		pass
	def sort(self, *args):
		pass



class NavigationView (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bar_tint_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_bar_hidden = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.title_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def pop_view(self, *args):
		pass
	def present(self, *args):
		pass
	def push_view(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class Path (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.bounds = None
		self.eo_fill_rule = None
		self.line_cap_style = None
		self.line_join_style = None
		self.line_width = None
	def add_arc(self, *args):
		pass
	def add_clip(self, *args):
		pass
	def add_curve(self, *args):
		pass
	def add_quad_curve(self, *args):
		pass
	def append_path(self, *args):
		pass
	def close(self, *args):
		pass
	def fill(self, *args):
		pass
	def hit_test(self, *args):
		pass
	def line_to(self, *args):
		pass
	def move_to(self, *args):
		pass
	def oval(cls, *args):
		pass
	def rect(cls, *args):
		pass
	def rounded_rect(cls, *args):
		pass
	def set_line_dash(self, *args):
		pass
	def stroke(self, *args):
		pass



class Point (object):
	def __init__(self, *args):
		pass
		self.x = None
		self.y = None
	def as_tuple(self, *args):
		pass



class Rect (object):
	def __init__(self, *args):
		pass
		self.h = None
		self.height = None
		self.max_x = None
		self.max_y = None
		self.min_x = None
		self.min_y = None
		self.origin = None
		self.size = None
		self.w = None
		self.width = None
		self.x = None
		self.y = None
	def as_tuple(self, *args):
		pass
	def center(self, *args):
		pass
	def contains_point(self, *args):
		pass
	def contains_rect(self, *args):
		pass
	def inset(self, *args):
		pass
	def intersection(self, *args):
		pass
	def intersects(self, *args):
		pass
	def max(self, *args):
		pass
	def min(self, *args):
		pass
	def translate(self, *args):
		pass
	def union(self, *args):
		pass



class ScrollView (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alpha = None
		self.always_bounce_horizontal = None
		self.always_bounce_vertical = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounces = None
		self.bounds = None
		self.center = None
		self.content_inset = None
		self.content_mode = None
		self.content_offset = None
		self.content_size = None
		self.corner_radius = None
		self.decelerating = None
		self.delegate = None
		self.directional_lock_enabled = None
		self.dragging = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.indicator_style = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.paging_enabled = None
		self.right_button_items = None
		self.scroll_enabled = None
		self.scroll_indicator_insets = None
		self.shows_horizontal_scroll_indicator = None
		self.shows_vertical_scroll_indicator = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.tracking = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class SegmentedControl (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.enabled = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.segments = None
		self.selected_index = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class Size (object):
	def __init__(self, *args):
		pass
		self.h = None
		self.height = None
		self.w = None
		self.width = None
		self.x = None
		self.y = None
	def as_tuple(self, *args):
		pass



class Slider (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.continuous = None
		self.corner_radius = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.value = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class Switch (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.enabled = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.value = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class TableView (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.allows_multiple_selection = None
		self.allows_multiple_selection_during_editing = None
		self.allows_selection = None
		self.allows_selection_during_editing = None
		self.alpha = None
		self.always_bounce_horizontal = None
		self.always_bounce_vertical = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounces = None
		self.bounds = None
		self.center = None
		self.content_inset = None
		self.content_mode = None
		self.content_offset = None
		self.content_size = None
		self.corner_radius = None
		self.data_source = None
		self.decelerating = None
		self.delegate = None
		self.directional_lock_enabled = None
		self.dragging = None
		self.editing = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.indicator_style = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.paging_enabled = None
		self.right_button_items = None
		self.row_height = None
		self.scroll_enabled = None
		self.scroll_indicator_insets = None
		self.selected_row = None
		self.selected_rows = None
		self.separator_color = None
		self.shows_horizontal_scroll_indicator = None
		self.shows_vertical_scroll_indicator = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.tracking = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def delete_rows(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def insert_rows(self, *args):
		pass
	def present(self, *args):
		pass
	def reload(self, *args):
		pass
	def reload_data(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_editing(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class TableViewCell (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.accessory_type = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.content_view = None
		self.corner_radius = None
		self.detail_text_label = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.image_view = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.selectable = None
		self.selected_background_view = None
		self.subviews = None
		self.superview = None
		self.text_label = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class TextField (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.action = None
		self.alignment = None
		self.alpha = None
		self.autocapitalization_type = None
		self.autocorrection_type = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bordered = None
		self.bounds = None
		self.center = None
		self.clear_button_mode = None
		self.content_mode = None
		self.corner_radius = None
		self.delegate = None
		self.enabled = None
		self.flex = None
		self.font = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.keyboard_type = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.placeholder = None
		self.right_button_items = None
		self.secure = None
		self.spellchecking_type = None
		self.subviews = None
		self.superview = None
		self.text = None
		self.text_color = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def begin_editing(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def end_editing(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class TextView (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alignment = None
		self.alpha = None
		self.always_bounce_horizontal = None
		self.always_bounce_vertical = None
		self.auto_content_inset = None
		self.autocapitalization_type = None
		self.autocorrection_type = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounces = None
		self.bounds = None
		self.center = None
		self.content_inset = None
		self.content_mode = None
		self.content_offset = None
		self.content_size = None
		self.corner_radius = None
		self.decelerating = None
		self.delegate = None
		self.directional_lock_enabled = None
		self.dragging = None
		self.editable = None
		self.flex = None
		self.font = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.indicator_style = None
		self.keyboard_type = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.paging_enabled = None
		self.right_button_items = None
		self.scroll_enabled = None
		self.scroll_indicator_insets = None
		self.selectable = None
		self.selected_range = None
		self.shows_horizontal_scroll_indicator = None
		self.shows_vertical_scroll_indicator = None
		self.spellchecking_type = None
		self.subviews = None
		self.superview = None
		self.text = None
		self.text_color = None
		self.tint_color = None
		self.touch_enabled = None
		self.tracking = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def begin_editing(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def end_editing(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def replace_range(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass



class Touch (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.location = None
		self.phase = None
		self.prev_location = None
		self.timestamp = None
		self.touch_id = None


class Transform (object):
	def __init__(self, *args):
		pass
	def concat(self, *args):
		pass
	def invert(self, *args):
		pass
	def rotation(cls, *args):
		pass
	def scale(cls, *args):
		pass
	def translation(cls, *args):
		pass



class Vector2 (object):
	def __init__(self, *args):
		pass
		self.x = None
		self.y = None
	def as_tuple(self, *args):
		pass

class View (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def present(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def wait_modal(self, *args):
		pass
		
class WebView (object):
	def __init__(self, *args):
		pass
		self._objc_ptr = None
		self.alpha = None
		self.autoresizing = None
		self.background_color = None
		self.bg_color = None
		self.border_color = None
		self.border_width = None
		self.bounds = None
		self.center = None
		self.content_mode = None
		self.corner_radius = None
		self.delegate = None
		self.flex = None
		self.frame = None
		self.height = None
		self.hidden = None
		self.left_button_items = None
		self.multitouch_enabled = None
		self.name = None
		self.navigation_view = None
		self.on_screen = None
		self.right_button_items = None
		self.scales_page_to_fit = None
		self.subviews = None
		self.superview = None
		self.tint_color = None
		self.touch_enabled = None
		self.transform = None
		self.width = None
		self.x = None
		self.y = None
	def add_subview(self, *args):
		pass
	def bring_to_front(self, *args):
		pass
	def close(self, *args):
		pass
	def draw_snapshot(self, *args):
		pass
	def eval_js(self, *args):
		pass
	def evaluate_javascript(self, *args):
		pass
	def go_back(self, *args):
		pass
	def go_forward(self, *args):
		pass
	def load_html(self, *args):
		pass
	def load_url(self, *args):
		pass
	def present(self, *args):
		pass
	def reload(self, *args):
		pass
	def remove_subview(self, *args):
		pass
	def send_to_back(self, *args):
		pass
	def set_needs_display(self, *args):
		pass
	def size_to_fit(self, *args):
		pass
	def stop(self, *args):
		pass
	def wait_modal(self, *args):
		pass

