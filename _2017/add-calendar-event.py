# https://forum.omz-software.com/topic/4142/xcode-calendar-access-error

from  objc_util import *
from ctypes import POINTER
import threading
import calendar, time

store = ObjCClass('EKEventStore').alloc().init()

access_granted = threading.Event()
def completion(_self, granted, _error):
    access_granted.set()
completion_block = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
store.requestAccessToEntityType_completion_(0, completion_block)
access_granted.wait()

event = ObjCClass('EKEvent').eventWithEventStore_(store)

event.title = 'test'
event.startDate = ObjCClass('NSDate').dateWithTimeIntervalSince1970_(time.mktime(time.strptime('2017-06-18 12:00:00', '%Y-%m-%d %H:%M:%S')))
event.endDate = ObjCClass('NSDate').dateWithTimeIntervalSince1970_(time.mktime(time.strptime('2017-06-18 13:00:00', '%Y-%m-%d %H:%M:%S')))
event.setCalendar_(store.defaultCalendarForNewEvents())
LP_c_void_p = POINTER(c_void_p)
err = LP_c_void_p()
store.saveEvent_span_error_(event, 0, err)
