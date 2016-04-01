# coding: utf-8

# https://github.com/tjferry14/My-Pythonista-Projects/blob/master/reminders.py

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
    r.completed = not r.completed
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