# coding: utf-8

# https://forum.omz-software.com/topic/2929/objc_utils-and-eventkit/5

from __future__ import print_function
from objc_util import *

store = ObjCClass('EKEventStore').alloc().init()

#store._requestAccessForEntityType_() #there needs to be permission granted to access the calendar, not sure exactly how to implement that.

cal = ObjCClass('NSCalendar').currentCalendar()
oneDayAgoComponents = ObjCClass('NSDateComponents').alloc().init()
oneDayAgoComponents.day = -1
# date = ObjCClass('NSDate')
date = ObjCClass('NSDate').date()
oneDayAgo = cal.dateByAddingComponents_toDate_options_(oneDayAgoComponents, date, 0)
#oneDayAge is None??
        
oneYearFromNowComponents = ObjCClass('NSDateComponents').alloc().init()
oneYearFromNowComponents.year = 1
oneYearFromNow = cal.dateByAddingComponents_toDate_options_(oneDayAgoComponents, date, 0)
#oneYearFromNow is None??

#predicate = store.predicateForEventsWithStartDate_endDate_calendars_(oneDayAgo, oneYearFromNow, None)
#this predicate line ^^ crashes pythonista

# --------------------

store = ObjCClass('EKEventStore').alloc().init()
access_granted = threading.Event()
def completion(_self, granted, _error):
    access_granted.set()
completion_block = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
store.requestAccessToEntityType_completion_(0, completion_block)
access_granted.wait()

# ...
predicate = store.predicateForEventsWithStartDate_endDate_calendars_(oneDayAgo, oneYearFromNow, None)
events = store.eventsMatchingPredicate_(predicate)
print(events)
# --------------------
