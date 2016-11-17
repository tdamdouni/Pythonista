# coding: utf-8

# https://forum.omz-software.com/topic/1338/reminders-list-index-out-of-range/14

import dialogs
import reminders
import ui

v = ui.load_view('reminders')
reminders_table = v['reminders']

def picked(sender):
    item = sender.items[sender.selected_row]
    r = item['reminder']
    r.completed = True
    r.save()
    del sender.items[sender.selected_row]

def grabbed():
    global todo_items, completed_items
    todo = reminders.get_reminders(completed=False)
    todo_items = [{'title': r.title, 'reminder': r} for r in todo]
    done = reminders.get_reminders(completed=True)
    completed_items = [{'title': r.title, 'reminder': r} for r in done]
    reminders_table.data_source = ui.ListDataSource(items=todo_items)
    reminders_table.data_source.action = picked
    reminders_table.reload()

def button_action(sender):
    if segment.selected_index == 0:
        reminders_table.data_source = ui.ListDataSource(items=todo_items)
        reminders_table.data_source.action = picked
        reminders_table.reload()
    elif segment.selected_index == 1:
        reminders_table.data_source = ui.ListDataSource(items=completed_items)
        reminders_table.data_source.action = picked
        reminders_table.reload()

@ui.in_background
def but_action(sender):
    fields = [{'key' : 'name', 'type' : 'text', 'value' : 'Name your reminder'},]
    result=dialogs.form_dialog(title='Create a Reminder', fields=fields)
    r = reminders.Reminder()
    r.title = result['name']
    r.save()
    segment.selected_index = 0
    grabbed()

segment = v['segmentedcontrol1']
segment.action = button_action
reminders_table.data_source.action = picked
create_button = ui.ButtonItem()
create_button.image = ui.Image.named('ionicons-ios7-plus-empty-32')
create_button.action = but_action
grabbed()
v.right_button_items = [create_button]
v.present('sheet')

# --------------------
# Another note: I've never used the built-in list_data_source so my knowledge is shaky.
# I generate TableViewCells directly in my own data_source. However if I did I would try to create a single ui.ListDataSource object at startup and update its contents when needed instead of creating a new one every time the contents change.

# --------------------
reminders_table.data_source = ui.ListDataSource(items=SomethingOrOther)

# --------------------
reminders_table.delegate = reminders_table.data_source

# --------------------

button_action()

# --------------------

def button_action(sender):
    if segment.selected_index:
        reminders_table.data_source.items = completed_items
    else:
        reminders_table.data_source.items = todo_items

# --------------------

def get_reminder_items(completed=False):
    return [{'title': r.title, 'reminder': r}
                for r in reminders.get_reminders(completed=completed)]

# --------------------

reminders_table.data_source.items = get_reminder_items(completed=TrueOrFalse

# --------------------
picked()# --------------------
grabbed()# --------------------
button_action()# --------------------
grabbed()

# --------------------

# coding: utf-8
import dialogs
import reminders
import ui

v = ui.load_view('reminders')
reminders_table = v['reminders']

def get_reminder_items(completed=False):
    return [{'title': r.title, 'reminder': r}
            for r in reminders.get_reminders(completed=completed)]

def picked(sender):
    item = sender.items[sender.selected_row]
    r = item['reminder']
    r.completed = True
    r.save()
    del sender.items[sender.selected_row]

def button_action(sender):
    if segment.selected_index:
        reminders_table.data_source.items = get_reminder_items(completed=True)
    else:
        reminders_table.data_source.items = get_reminder_items(completed=False)

@ui.in_background
def but_action(sender):
    fields = [{'key' : 'name', 'type' : 'text', 'value' : 'Name your reminder'},]
    result=dialogs.form_dialog(title='Create a Reminder', fields=fields)
    r = reminders.Reminder()
    r.title = result['name']
    r.save()
    segment.selected_index = 0
    reminders_table.data_source.items = get_reminder_items(completed=False)

segment = v['segmentedcontrol1']
segment.action = button_action
reminders_table.data_source.action = picked
create_button = ui.ButtonItem()
create_button.image = ui.Image.named('ionicons-ios7-plus-empty-32')
create_button.action = but_action
reminders_table.data_source.items = get_reminder_items(completed=False)
v.right_button_items = [create_button]
v.present('sheet')# --------------------
def button_action(sender):
    completed = segment.selected_index == 1
    reminders_table.data_source.items = get_reminder_items(completed=completed)

# --------------------

# coding: utf-8
import console
import dialogs
import reminders
import ui

v = ui.load_view('reminders')
reminders_table = v['reminders']

def get_reminder_items(completed=False):
    return [{'title': r.title, 'reminder': r}
            for r in reminders.get_reminders(completed=completed)]

def picked(sender):
    item = sender.items[sender.selected_row]
    r = item['reminder']
    if r.completed == True:
        r.completed = False
    else:
        r.completed = True
    r.save()
    del sender.items[sender.selected_row]

def button_action(sender):
    completed = segment.selected_index == 1
    reminders_table.data_source.items = get_reminder_items(completed=completed)

@ui.in_background
def but_action(sender):
    fields = [{'key' : 'name', 'type' : 'text', 'value' : 'Name your reminder'},
              {'key' : 'calendar', 'type' : 'text', 'value' : 'Name a calendar for this reminder'}]
    result=dialogs.form_dialog(title='Create a Reminder', fields=fields)
    all_calendars = reminders.get_all_calendars()
    for calendar in all_calendars:
        if calendar.title == result['calendar']:
            r = reminders.Reminder(calendar)
            r.title = result['name']
            r.save()
            break
    else:
        q = console.alert('Could not find calendar', 'Could not find calendar named ' + result['calendar'] + ' Would you like to create one?', 'Yes', hide_cancel_button=False)
        if q == 1:
            new_calendar = reminders.Calendar()
            new_calendar.title = result['calendar']
            new_calendar.save()
            calendar.title == result['calendar']
            r = reminders.Reminder(calendar)
            r.title = result['name']
            r.save()

    segment.selected_index = 0
    reminders_table.data_source.items = get_reminder_items(completed=False)
    #console.hud_alert('Reminder Created', 'success', 1)

segment = v['segmentedcontrol1']
segment.action = button_action
reminders_table.data_source.action = picked
create_button = ui.ButtonItem()
create_button.image = ui.Image.named('ionicons-ios7-plus-empty-32')
create_button.action = but_action
reminders_table.data_source.items = get_reminder_items(completed=False)
v.right_button_items = [create_button]
v.present('sheet')

# --------------------

    if r.completed == True:
        r.completed = False
    else:
        r.completed = True

# can be replaced by

    r.completed = not r.completed
    
# --------------------
