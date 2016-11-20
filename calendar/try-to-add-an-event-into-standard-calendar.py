# coding: utf-8

# https://forum.omz-software.com/topic/3053/try-to-add-an-event-into-standard-calendar

from objc_util import *

#import threading

# EKEventStore = calendar database
store = ObjCClass('EKEventStore').alloc().init()

# Pythonista has authorization to access calendar, thus code is commented
#access_granted = threading.Event()
#def completion(_self, granted, _error):
#    access_granted.set()
#completion_block = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
#store.requestAccessToEntityType_completion_(0, completion_block)
#access_granted.wait()

event = ObjCClass('EKEvent').eventWithEventStore_(store)

event.title = 'test'
event.startDate = ObjCClass('NSDate').date()
event.endDate = ObjCClass('NSDate').date()
event.setCalendar_(store.defaultCalendarForNewEvents())
#event.alarms = ...

# store.saveEvent_(event,0) # only this instance

# The method should be saveEvent_span_error_(). The span parameter is only relevant for recurring events, I think. You can probably pass 0 for that.

store.saveEvent_span_error_(event,0,)

