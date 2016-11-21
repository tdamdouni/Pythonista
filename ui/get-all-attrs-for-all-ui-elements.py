# https://forum.omz-software.com/topic/3559/share-get-all-attrs-for-all-ui-elements

# Phuket2 , Pythonista Forums (Python profiency, not much)
# date - 7 oct 2016
# works for python 2 or 3
'''
    get_all_attrs_set - the main function of interest

    iterates over a list of all the ui Elements, and retuns a set of
    all the unique attrs for all the ui Elements combined.

    i am sure this could be tighten up more. But i think the readabilty
    is ok now. if not for ui.NavigationView, i would have tried to use
    a list comp rather than the for. I could have tried to special case
    it, but i think personally this is more clear given what it is.
'''

import ui, pprint, inspect

'''
    # 7 oct 2016
    This was hard coded before. Have commented it out now. i have left
    it in just to show the lesson i learnt.  only recently also :(
    @ccc provided the list comp in the func get_ui_classes() that
    totally negates having to create a static list.

_ui_controls = \
    [
        ui.View, ui.Button, ui.ButtonItem, ui.ImageView, ui.Label,
        ui.NavigationView, ui.ScrollView, ui.SegmentedControl,
        ui.Slider, ui.Switch, ui.TableView, ui.TextField, ui.TextView,
        ui.WebView, ui.DatePicker, ui.ActivityIndicator, ui.TableViewCell
    ]
'''

def get_ui_classes():
	# thanks @ccc
	return [c for _, c in inspect.getmembers(ui) if hasattr(c, 'superview')]
	
_ui_controls = get_ui_classes()

def get_full_dict(obj):
	# get all the dict attrs for obj, no filter
	return {k: getattr(obj, k) for k in dir(obj)}
	
def get_all_attrs_set():
	# return a set of unique attrs across all ui_elements
	# sets doing all the hard work with the union operator '|'
	s = set()
	for ctl in _ui_controls:
		try:
			s = s | set(get_full_dict(ctl()))
		except:
			# handle differently for ui.NavigationView, it needs a
			# ui.View as a param
			if ctl is ui.NavigationView:
				s = s | set(get_full_dict(ctl(ui.View())))
			else:
				# print out a control type if an error produced we
				# do not handle
				print(ctl)
	return s
	
if __name__ == '__main__':
	# pprint prints out a nice easy to view, sorted list of the attrs
	pp = pprint.PrettyPrinter(indent=4, width=80)
	attr_set = get_all_attrs_set()
	pp.pprint(attr_set)
	print('Number of unique attrs across all ui elements (not filtered) - {}'.format(len(attr_set)))
	print()
	print('python 3.5x reports 155 items, python 2.7x reports 149 items. the difference lays in the attrs starting with _')
# --------------------
import ui, pprint, inspect

def get_all_attrs_set():
	s = set()
	for ctl in [c for _, c in inspect.getmembers(ui) if hasattr(c, 'superview')]:
		try:
			s = s | set({k: getattr(ctl, k) for k in dir(ctl)})
		except:
			if ctl is ui.NavigationView:
				s = s | set({k: getattr(ctl, k) for k in dir(ctl(ui.View()))})
			else:
				print(ctl)
	return s
	
if __name__ == '__main__':
	# pprint prints out a nice easy to view, sorted list of the attrs
	pp = pprint.PrettyPrinter(indent=4, width=80)
	attr_set = get_all_attrs_set()
	pp.pprint(attr_set)
	print('Number of unique attrs across all ui elements (not filtered) - {}'.format(len(attr_set)))
	print()
	print('python 3.5x reports 155 items, python 2.7x reports 149 items. the difference lays in the attrs starting with _')

