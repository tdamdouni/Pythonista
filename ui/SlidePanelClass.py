# coding: utf-8

# https://gist.github.com/Phuket2/9db968e16f6f8d8cace1

# https://forum.omz-software.com/topic/2154/using-a-custom-pu-pyui-view-in-another-one-using-ui-editor/18

'''
    code copied from dialogs.py Pythonista 1.6 beta, @omz (Ole Zorn)
    specially the parts of the code that present a datepicker
    in a dialog with animation and a shield of the dialogs contents
    a few mods made
'''
from __future__ import print_function
_country_list = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Democratic Republic of the Congo (Kinshasa)', 'Congo, Republic of (Brazzaville)', 'Cook Islands', 'Costa Rica', 'Ivory Coast', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor (Timor-Leste)', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Great Britain', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Rep. (North Korea)", 'Korea, Republic of (South Korea)', ' ', 'Kuwait', 'Kyrgyzstan', "Lao, People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia, Rep. of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federal States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar, Burma', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian territories', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Island', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion Island', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia (Slovak Republic)', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria, Syrian Arab Republic', 'Taiwan (Republic of China)', 'Tajikistan', 'Tanzania; officially the United Republic of Tanzania', 'Thailand', 'Tibet', 'Timor-Leste (East Timor)', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Ugandax', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City State (Holy See)', 'Venezuela', 'Vietnam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Zambia']

countries_json =[
  {
    "selected" : False,
    "frame" : "{{0, 0}, {500, 200}}",
    "class" : "View",
    "nodes" : [
      {
        "selected" : False,
        "frame" : "{{6, 6}, {488, 29}}",
        "class" : "SegmentedControl",
        "nodes" : [

        ],
        "attributes" : {
          "name" : "seg",
          "frame" : "{{60, 106}, {120, 29}}",
          "uuid" : "E26BCE96-C52F-4F45-AC7A-738809C6AF1D",
          "class" : "SegmentedControl",
          "segments" : "All|Americas|World",
          "flex" : "LRTB"
        }
      },
      {
        "selected" : False,
        "frame" : "{{17, 39}, {327, 147}}",
        "class" : "TableView",
        "nodes" : [

        ],
        "attributes" : {
          "flex" : "WH",
          "data_source_items" : "Australia\nDenmark",
          "name" : "tb_countries",
          "frame" : "{{20, 20}, {200, 200}}",
          "uuid" : "41E098BC-B628-41C7-B2FD-5DAC55F63F88",
          "background_color" : "RGBA(1.0, 1.0, 1.0, 1.0)",
          "data_source_number_of_lines" : 1,
          "class" : "TableView",
          "data_source_delete_enabled" : True,
          "row_height" : 30,
          "data_source_font_size" : 12
        }
      },
      {
        "selected" : False,
        "frame" : "{{404, 162}, {80, 32}}",
        "class" : "Button",
        "nodes" : [

        ],
        "attributes" : {
          "uuid" : "B69CDA6E-07BC-4D3F-A9EF-AECF78C63E7E",
          "frame" : "{{210, 84}, {80, 32}}",
          "title" : "Button",
          "class" : "Button",
          "name" : "button1",
          "font_size" : 15
        }
      },
      {
        "selected" : False,
        "frame" : "{{404, 125}, {80, 29}}",
        "class" : "Button",
        "nodes" : [

        ],
        "attributes" : {
          "uuid" : "B9F40711-CF4C-4644-8C54-2593588D1E3E",
          "frame" : "{{210, 84}, {80, 32}}",
          "title" : "Button",
          "class" : "Button",
          "name" : "button2",
          "font_size" : 15
        }
      }
    ],
    "attributes" : {
      "flex" : "",
      "enabled" : True,
      "tint_color" : "RGBA(0.000000,0.478000,1.000000,1.000000)",
      "custom_class" : "selfwrapper",
      "border_color" : "RGBA(0.000000,0.000000,0.000000,1.000000)",
      "background_color" : "RGBA(1.000000,1.000000,1.000000,1.000000)"
    }
  }
]

pyui_descriptor = \
    {
        # valid types, pyui_file and pyui_str
        # if pyui_file, data = a valid pyui filename
        # if pyui_str, data =  a json str using json.dumps(obj)
        'type'  : 'pyui_file',
        'data'  : None,
        'raw'       : True,
    }

import string
import ui
import json

class PYUILoader(ui.View):
	'''
	loads a pyui file into the class, acts as another ui.View
	class.
	** Please note that the pyui class must have its
	Custom Class attr set to self

	Thanks @JonB
	'''
	def __init__(self, pyui_rec):

		if not pyui_rec:
			# silent fail is ok
			return

		if not isinstance(pyui_rec, dict) or \
		'type' not in pyui_rec or \
		'data' not in pyui_rec or \
		'raw'  not in pyui_rec :

			raise TypeError('''Expected a dict with keys,
			key and data defined''')


		if not pyui_rec.get('type') or \
		not pyui_rec.get('data'):
			raise TypeError('Both type and data values need to be present')

		class selfwrapper(ui.View):
			def __new__(cls):
				return self

		if pyui_rec.get('type') == 'pyui_file':
			ui.load_view( pyui_rec.get('data') ,
			bindings={'selfwrapper':selfwrapper, 'self':self})

		elif pyui_rec.get('type') == 'pyui_str' :
			if pyui_rec.get('raw', False):
				pyui_rec['data'] = json.dumps(pyui_rec.get('data',''))

			ui.load_view_str(pyui_rec.get('data',''),
			bindings={'selfwrapper':selfwrapper, 'self':self})

		self.loaded_type = pyui_rec.get('type')
		return




class CountriesPanel(PYUILoader):
	def __init__(self, pyui_rec):
		super(CountriesPanel, self).__init__(pyui_rec)

		self.populate_data()

	def populate_data(self):
		self['tb_countries'].data_source.items = _country_list
		self['seg'].segments = string.ascii_uppercase


	def release(self):
		pass




class UIAnimatedPanel(object):
	def __init__(self, parent, panel_obj, show_panel = True):
		self.parent = parent
		self.left_item_actions = []

		# used as a cache of menu ButtonItems objects
		# with their enabled states

		self.menu_btn_states = []


		self.view = None

		self.dismiss = None
		self.panel = panel_obj

		self.use_shield_btn = True


		self.fade_in_duration  = 0.3
		self.fade_out_duration = 0.3

		if not hasattr(parent, 'panel_displayed'):
			parent.panel_displayed = False

		# not sure about this.. its a start
		# saving the results of the panel in a dict
		# in the parent.
		if not hasattr(parent, 'panel_result_dict'):
			parent.panel_displayed = False

		if hasattr(self.parent, 'container_view'):
			# to work with dialogs.py
			self.view = self.parent.container_view
		else:
			self.view = parent

		self.p_width = self.view.width
		self.p_height = self.view.height


		if show_panel:
			self.show_panel()

	def show_panel(self):
		'''
		stops us showing muliple times.because we make this class
		on the fly, storing states inside the class does not make
		sense so we strore them in the parent :(
		'''
		if hasattr(self.parent, 'panel_displayed'):
			if self.parent.panel_displayed:
				return

		self.parent.panel_displayed = True

		ui.end_editing()

		# save and disable the menu buttons
		self.disable_menu_buttons()

		# removed the shield view. didnt think it was needed
		# as ui.Button is a ui.View. i changed some alpha vals.
		# seems to work the same...i hope so
		self.dismiss = ui.Button()
		self.dismiss.flex = 'WH'
		self.dismiss.frame = (0, 0, self.p_width, self.p_height)
		self.dismiss.background_color = (0, 0, 0, 0.5)
		self.dismiss.action = self.dismiss_action
		self.dismiss.alpha = 0.0

		self.panel.frame = (0, self.dismiss.height - self.panel.height,
		self.dismiss.width, self.panel.height )

		self.panel.flex = 'TW'
		self.panel.transform = ui.Transform.translation(0, self.panel.height)
		self.dismiss.add_subview(self.panel)

		self.view.add_subview(self.dismiss)

		def fade_in():
			self.dismiss.alpha = 1.0
			self.panel.transform = ui.Transform.translation(0, 0)

		ui.animate(fade_in, self.fade_in_duration)

	def dismiss_action(self, sender = None):
		def fade_out():
			self.dismiss.alpha = 0 # modified from .5 to 0 because no shield
			self.panel.transform = ui.Transform.translation(0, self.panel.height)

		def remove():
			# make sure we clean up

			if hasattr(self.panel, 'release'):
				self.panel.release()

			self.dismiss.remove_subview(self.panel)
			self.view.remove_subview(self.dismiss)
			self.dismiss = None

			# try to be nice and not leave our
			# crap (attr) in the parent class
			delattr(self.parent, 'panel_displayed')
			self.reset_menu_buttons()

		ui.animate(fade_out, self.fade_out_duration, completion=remove)

	def disable_menu_buttons(self):

		# backup the enabled states of the menus ButtonItem
		# YUK !!!
		menu_btns = list()
		if self.parent.left_button_items:
			self.menu_btn_states += [(btn, btn.enabled)for btn in self.parent.left_button_items
			if isinstance(btn, ui.ButtonItem)]

		if self.parent.right_button_items:
			self.menu_btn_states += [(btn, btn.enabled)for btn in self.parent.right_button_items
			if isinstance(btn, ui.ButtonItem)]


		# disable all the menu items
		for tp in self.menu_btn_states:
			tp[0].enabled = False

	def reset_menu_buttons(self):
		# restore the enabled states
		for tp in self.menu_btn_states:
			tp[0].enabled = tp[1]




def show_panel(sender):
	UIAnimatedPanel(sender.superview, CountriesPanel(dict(type = 'pyui_str', data = countries_json, raw = True)))

def beep_beep():
	print('RoadRunner here....')

if __name__ == '__main__':

	# create the host ui.View
	frame = (0,0, 500, 500)
	v = ui.View(frame = frame)

	v.background_color = 'white'
	# make some host menu items...
	# we want to test these are disabled when the panel us shown
	# and restored to the previous states once dusmissed.
	btn0 = ui.ButtonItem(title = 'left0')
	btn1= ui.ButtonItem(title = 'right0')
	btn2 = ui.ButtonItem(title = 'right1')
	btn0.action = btn1.action = btn2.action = beep_beep
	v.left_button_items  = (btn0,)
	v.right_button_items = (btn1, btn2)


	# uncomment to see the states are being re-instated correctly
	#btn0.enabled = False

	btn = ui.Button(name = 'btntest', title = 'Show Panel')
	btn.action = show_panel
	btn.border_with = .5
	btn.width = 100
	btn.heigth = 30

	v.add_subview(btn)
	v.present('sheet')
	pyui_d = dict(type = 'pyui_str', data = countries_json, raw = True)
	#pyui_d = dict(type = 'pyui_file', data = 'Countries', raw = False)


	UIAnimatedPanel(v, CountriesPanel(pyui_d))