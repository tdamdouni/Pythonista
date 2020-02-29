
# coding: utf-8
'''
ical - Access iOS system calendar from Pythonista
author: Lukas Kollmer <lukas@kollmer.me>
note: Work in progress. not finished
'''
from __future__ import print_function

__all__ = ['Event', 'has_access', 'save_event', 'delete_event', 'get_events', 'get_calendars', 'get_calendar']

from objc_util import *
import sys
import datetime
import time
import calendar as pysyscal
import ctypes


EKEventStore = ObjCClass('EKEventStore')
EKEvent = ObjCClass('EKEvent')
NSDate = ObjCClass('NSDate')
NSDateComponents = ObjCClass('NSDateComponents')
NSCalendar = ObjCClass('NSCalendar')

AUTHORIZATION_STATUS_NOT_DETERMINED = 0
AUTHORIZATION_STATUS_RESTRICTED = 1
AUTHORIZATION_STATUS_DENIED = 2
AUTHORIZATION_STATUS_AUTHORIZED = 3

DEFAULT_CALENDAR_SPECIFIER = 'me.kollmer.ioscalendar.useDefaultCalendar'

_event_store = None

debug = True


class Calendar (object):
	title = None
	identifier = None
	objc_object = None
	

class Event (object):
	loaded_from_system_calendar = False
	start_date = None
	end_date = None
	title = None
	calendar = None
	is_all_day = None
	organizer = None
	identifier = None
	objc_event_object = None
	
	def __init__(self):
		pass
	
	def __str__(self):
		return '<Event title: {}, calendar: {}, start_date: {}, end_date: {}'.format(self.title, self.calendar, self.start_date, self.end_date)
	
	def __repr__(self):
		return self.__str__()


def _event_from_objc_event(objc_event):
	event = Event()
	event.objc_event_object = objc_event
	event.title = str(objc_event.title())
	event.identifier = str(objc_event.eventIdentifier())
	event.calendar = str(objc_event.calendar().title())
	event.start_date = python_date_from_nsdate(objc_event.startDate())
	event.end_date = python_date_from_nsdate(objc_event.endDate())
	return event
		

def _get_event_store():
	global _event_store
	if has_access():
		if _event_store is None:
			_event_store = EKEventStore.alloc().init()
		return _event_store
	elif authorization_not_yet_determined():
		request_access()
		return _get_event_store()
	elif access_denied():
		console.hud_alert('Access to calendar denied. open settings to allow')
	else:
		return None


def _current_authorization_status():
	status = EKEventStore.authorizationStatusForEntityType_(0)
	return status
	
	
def has_access():
	return _current_authorization_status() == AUTHORIZATION_STATUS_AUTHORIZED
	
	
def authorization_not_yet_determined():
	return _current_authorization_status() == AUTHORIZATION_STATUS_NOT_DETERMINED


def access_denied():
	return _current_authorization_status() == AUTHORIZATION_STATUS_DENIED


def request_access_completion_handler(_cmd, success, error_ptr):
		error = ObjCInstance(error_ptr)
		if debug:
			print(success)
			print(error)
	
	
def request_access():
	completion_handler_block = ObjCBlock(request_access_completion_handler, restype=None, argtypes=[c_void_p, c_bool, c_void_p])
	
	EKEventStore.new().requestAccessToEntityType_completion_(0, completion_handler_block)


def save_event(event):
	event_store = _get_event_store()
	objc_event = EKEvent.eventWithEventStore_(event_store)
	objc_event.setTitle_(event.title)
	objc_event.setCalendar_(event.calendar.objc_object)
	objc_event.setStartDate_(nsdate_from_python_date(event.start_date))
	objc_event.setEndDate_(nsdate_from_python_date(event.end_date))
	error_ref = c_void_p(None)
	success = event_store.saveEvent_span_error_(objc_event, 0, ctypes.byref(error_ref))
	if error_ref and debug:
		print(('error', ObjCInstance(error_ref)))
	return success


def delete_event(event, delete_future_occurencies=False):
	event_store = _get_event_store()
	if isinstance(event, Event):
		_event = event.objc_event_object
	elif event._get_objc_classname() == 'EKEvent':
		_event = event
	else:
		raise NameError('Error getting event to save')
	error_ref = c_void_p(None)
	success = event_store.removeEvent_span_error_(_event, int(delete_future_occurencies), ctypes.byref(error_ref))
	if error_ref and debug:
		# Do something with the error
		print(ObjCInstance(error_ref))
	return success


def get_calendars():
	store = _get_event_store()
	objc_calendars = store.calendarsForEntityType_(0)
	calendars = []
	for cal in objc_calendars:
		calendar = Calendar()
		calendar.title = str(cal.title())
		calendar.identifier = str(cal.calendarIdentifier())
		calendar.objc_object = cal
		calendars.append(calendar)
	return calendars


def get_calendar(name):
	all_calendars = get_calendars()
	try:
		return [cal for cal in all_calendars if cal.title == name][0]
	except IndexError:
		raise NameError("Could not find calendar with name '{}'".format(name))


def get_events(count=10, calendar=DEFAULT_CALENDAR_SPECIFIER, include_past=False):
	'''
	Note: For some reason, the predicate created by the event store can span at most 4 years from the start date. therefore, setting the start date to NSDate.distantPast (01/01/70) and the end date to NSDate.distantFuture will be absolutely useless, since ios will automatically set the end date to 01/01/74. solution: when include_past is true, fetch events beteeen 2 years in the past and 2 years in the future (todo: file a radar)
	'''
	store = _get_event_store()
	cal = store.defaultCalendarForNewEvents()
	
	if isinstance(calendar, Calendar):
		if debug:
			print('passed instance')
		calendar = calendar.title
	
	if not calendar == DEFAULT_CALENDAR_SPECIFIER:
		if debug:
			print('not default')
		cal_id = ''
		for c in get_calendars():
			if c.title == calendar:
				cal_id = c.identifier
				cal = store.calendarWithIdentifier_(cal_id)
	
	if debug:
		print('will load {} events for calendar {}'.format(count, cal.title()))
	if include_past:
		time_inverval_for_two_years = 60*60*24*365*2 # seconds(60) * minutes(60) * hours(24) * days(365)
		start_date = NSDate.dateWithTimeIntervalSinceNow_((time_inverval_for_two_years)*(-1))
		end_date = NSDate.dateWithTimeIntervalSinceNow_(time_inverval_for_two_years)
	else:
		start_date = NSDate.date()
		end_date = NSDate.distantFuture()
	predicate = store.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [cal])
	events_matching_predicate = store.eventsMatchingPredicate_(predicate)
	if events_matching_predicate is None:
		return []
	else:
		if count == 0:
			objc_events = list(events_matching_predicate)
		else:
			objc_events = list(events_matching_predicate)[:count]
		
		events = map(_event_from_objc_event, objc_events)
		return events


def python_date_from_nsdate(nsdate):
	return datetime.datetime.fromtimestamp(nsdate.timeIntervalSince1970())


def nsdate_from_python_date(date):
	# TODO: Find a way to get a timestamp from python date without the calendar module
	date_as_tuple = date.timetuple()
	timestamp = pysyscal.timegm(date_as_tuple)
	
	return NSDate.alloc().initWithTimeIntervalSince1970_(timestamp)
	
if __name__ == '__main__':
	import console
	console.clear()
	
	
	
	print(('has access:', has_access()))
	print(('event store:', _get_event_store()))
	#get_calendars()
	#get_events(1, 'Personal')
	test_calendar = get_calendar('Pythonista Test')
	print(test_calendar)
	print(get_events(10, test_calendar))
	#print(get_calendars()[0].objc_object)
	all_events = get_events(0, test_calendar)
	
	for event in all_events:
		print(event)
		print(delete_event(event))
	
	print('will save test event')
	test_event = Event()
	test_event.title = 'testevent tbd'
	test_event.calendar = get_calendar('Pythonista Test')
	test_event.start_date = datetime.datetime(2016, 06, 02, 20, 00, 00)
	test_event.end_date = datetime.datetime(2016, 06, 02, 20, 15, 00)
	
	save_event_success = save_event(test_event)
	print(('saved event', save_event_success))
	
	
