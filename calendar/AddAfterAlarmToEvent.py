# coding: utf-8

# https://gist.github.com/cvpe/30bcb17ac86b03eecad85ed2b74f93f3

# https://forum.omz-software.com/topic/3060/add-an-alarm-after-begin-of-a-calendar-event

# Add Alarm After Begin to Calendar Event

#           ===========
from __future__ import print_function
import ui
import console
import dialogs
import time
from objc_util import *
import threading
import webbrowser

class MyView(ui.View):

	def __init__(self,w,h):
		global store
		self.width = w
		self.height = h
		
		# EKEventStore = calendar database
		store = ObjCClass('EKEventStore').alloc().init()
		
		# Once Pythonista has been authorized, this code does not need to be executed
		#------- begin of commented code
		#access_granted = threading.Event()
		#def completion(_self, granted, _error):
		#       access_granted.set()
		#completion_block = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
		#store.requestAccessToEntityType_completion_(0, completion_block)
		#access_granted.wait()
		#------- end of commented
		
		#cal = ObjCClass('NSCalendar').currentCalendar()
		
		# Button: end
		end_button = ui.Button(name='end_button')
		#end_button.border_color = 'black'
		#end_button.border_width = 1
		end_button.width = 32
		end_button.height = 32
		end_button.x = 10
		end_button.y = 20
		end_button.background_image = ui.Image.named('iob:close_circled_256')
		end_button.title = ''
		end_button.action = self.end_action
		self.add_subview(end_button)
		
		# Button: dates
		dat_button = ui.Button(name='dat_button')
		#dat_button.border_color = 'black'
		#dat_button.border_width = 1
		dat_button.width = 32
		dat_button.height = 32
		dat_button.x = self.width-dat_button.width-10
		dat_button.y = end_button.y
		dat_button.background_image = ui.Image.named('iob:calendar_256')
		dat_button.title = ''
		dat_button.action = self.dat_action
		self.add_subview(dat_button)
		
		# Label: titre
		titlbl = ui.Label(name='titlbl')
		titlbl.width = w - end_button.width - dat_button.width - 3*10
		titlbl.height = 32
		titlbl.x = 10
		titlbl.y = end_button.y
		titlbl.text = 'Add Alarm After Begin to Calendar Event'
		titlbl.alignment = ui.ALIGN_CENTER
		titlbl.font= ('Courier-Bold',20)
		titlbl.text_color = 'blue'
		self.add_subview(titlbl)
		
		# TableView: Events
		evttab = ui.TableView()
		evttab.name = 'evttab'
		evttab.x = 10
		evttab.y = titlbl.y + titlbl.height + 10
		evttab.width = self.width - 20
		evttab.height = self.height - evttab.y - 10
		evttab.row_height = 20
		evttab.border_color = 'black'
		evttab.border_width = 1
		evttab.delegate = self
		self.add_subview(evttab)
		
	#@ui.in_background
	def dat_action(self,sender):
		global store
		
		# Ask begin and end date
		title = 'Begin date'
		d1dt = dialogs.date_dialog(title=title,done_button_title=title)
		if d1dt == None:
			return
		d1 = d1dt.strftime('%Y%m%d')
		self.name = 'Select end date'
		d2 = '20000101'
		title = 'End date'
		while d2 < d1:
			d2dt = dialogs.date_dialog(title=title,done_button_title=title)
			if d2dt == None:
				return
			d2 = d2dt.strftime('%Y%m%d')
			if d2 < d1:
				title = 'End date must be >= begin date, retry'
				
		# Convert string yyyymmdd to NSdate
		dateFormat = ObjCClass('NSDateFormatter').alloc().init()
		dateFormat.setDateFormat_('yyyyMMdd HH:mm')
		date1 = dateFormat.dateFromString_(d1+' 00:01')
		print(date1)
		date2 = dateFormat.dateFromString_(d2+' 23:59')
		print(date2)
		
		predicate = store.predicateForEventsWithStartDate_endDate_calendars_(date1, date2, None)
		self.events = store.eventsMatchingPredicate_(predicate)
		
		evttabs = []
		self.events_array = []
		for event in self.events:
			# store events in normal array instead of NSarray because this one is not updatable
			self.events_array.append(event)
			strdt = event.startDate()
			enddt = event.endDate()
			dur = enddt.timeIntervalSinceDate_(strdt)
			dur = dur/60 # minutes
			days,remain = divmod(dur, 24*60)
			hours,mins = divmod(remain,60)
			if days == 0:
				durf = '    '
			else:
				durf = '{:02d}j '.format(int(days))
			if hours == 0:
				durf = durf + '    '
			else:
				durf = durf + '{:02d}h '.format(int(hours))
			if mins == 0:
				durf = durf + '    '
			else:
				durf = durf + '{:02d}m '.format(int(mins))
			txt = str(dateFormat.stringFromDate_(strdt) ) + ' ' + durf + ': ' + str(event.title())
			evttabs.append(txt)
			
		evtlst = ui.ListDataSource(items=evttabs)
		evtlst.font= ('Courier',15)
		evtlst.text_color = 'black'
		self['evttab'].data_source = evtlst
		self['evttab'].reload()
		
	# see https://forum.omz-software.com/topic/2601/dialogs-issue
	#
	# if Done is pressed in form_dialog, this error occurs:
	# File "/var/mobile/Containers/Bundle/Application/CEBD1281-94B0-4EEC-BA60-D9599A5873CD/Pythonista.app/Frameworks/PythonistaKit.framework/pylib/site-packages/dialogs.py", line 365, in done_action
	# self.container_view.close()
	# AttributeError: 'NoneType' object has no attribute 'close
	# Here is the fix. The problem is that dialogs produces a model view, and Python needs to know that, or bad things happen. This is done by using the decorator @ui.inbackground.
	
	@ui.in_background
	def tableview_did_select(self, tableview, section, row):
		global store
		# Called when a row was selected
		event = self.events_array[row]
		alarms = event.alarms()
		fields = []
		if alarms <> None:
			i = 1
			for alarm in alarms:
				al = int(alarm.relativeOffset()/60)
				fields.append({'title':'n° '+str(i),'key':'alarm'+str(i),'type':'number','value':str(al)})
				i = i + 1
		else:
			i = 1
			
		# add a blank alarm for a new one
		n = i
		al = 0
		fields.append({'title':'n°'+str(n),'key':'alarm'+str(n),'type':'number','value':str(al)})
		als = dialogs.form_dialog(title='Alarmes (en minutes)',done_button_title='ok',fields=fields, sections=None)
		modif = False
		if als <> None:
			# Done pressed
			i = 1
			while i <= n:
				al = int(als['alarm'+str(i)])*60
				if i < n:
					alold = int(alarm.relativeOffset()/60)
				else:
					alold = 0
				if al <> alold:
					modif = True
					if i < n:
						# remove alarm
						event.removeAlarm_(alarms[i-1])
						
					if al <> 0:
						# add non zero alarm
						alarm = ObjCClass('EKAlarm').alarmWithRelativeOffset_(al)
						event.addAlarm_(alarm)
						
				i = i + 1
				
			if modif:
				if event.hasRecurrenceRules():
					but = console.alert('Event is recurrent','modify this instance only?','Yes','No',hide_cancel_button=True)
					if but == 1:
						span = 0 # only this instance
					else:
						span = 1 # all instances
				else:
					span = 0 # only this instance
				# store modified event in calendar
				store.saveEvent_span_error_(event,span,None)
				
				# store modified in memory, reason why we use a normal array instead of a NSarray
				self.events_array[row] = event
				
	def end_action(self,sender):
		self.close()
		
	def will_close(self):
		pass
		
#----- Main code ------------------------
console.clear()

# Hide script
w, h = ui.get_screen_size()
back = MyView(w,h)
back.background_color='white'
back.present('full_screen',hide_title_bar=True)

# Back to home screen
#webbrowser.open('launcher://crash')

