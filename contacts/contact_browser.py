import console, contacts, ui

people = contacts.get_all_people()
names = sorted([p.full_name for p in people])

class TheDelegate(object):
	def textfield_did_change(self, textfield):
		query = textfield.text.lower()
		contacts_view = textfield.superview['contactstable']
		matches = None
		if query:
			matches = sorted([p.full_name for p in people
			if query in p.full_name.lower()])
			v.name = str(len(matches)) + ' Matches' 
		contacts_view.data_source.items = matches or names
		contacts_view.reload()

	def tableview_did_select(self, tableview, section, row):
		console.hud_alert(tableview.data_source.items[row], 'success', 0.5)

v = ui.load_view('contact_browser')
the_delegate = TheDelegate()

v['search string'].clear_button_mode = 'while_editing'
v['search string'].delegate = the_delegate

contacts_view = v['contactstable']
contacts_view.data_source = ui.ListDataSource(names)
contacts_view.delegate = the_delegate

v.present('sheet')
