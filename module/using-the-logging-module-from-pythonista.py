# coding: utf-8

# https://forum.omz-software.com/topic/1529/using-the-logging-module-from-pythonista

import sys
import traceback,logging

logging.basicConfig(filename = 'log')

exception_logger = logging.getLogger('log.exception')

def log_traceback(ex, ex_traceback):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    print tb_text
    exception_logger.log(0,tb_text)
                            .
                            .
                            .

        try:
            self.items[self.currentRow]['accessory_type'] = 'none' # un-flags current selected row
        except Exception as ex: #needed for very first selection    
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback)


#==============================

import logging

LOG_FILENAME = 'logging_example.out'
logging.basicConfig(filename=LOG_FILENAME,
                level=logging.DEBUG,
                )

logging.debug('This message should go to the log file')

f = open(LOG_FILENAME, 'rt')
try:
    body = f.read()
finally:
    f.close()

print 'FILE:'
print body

#==============================

import logging,sys,traceback

LOG_FILENAME = 'logging_example.txt'
logging.basicConfig(filename=LOG_FILENAME,
                level=logging.DEBUG,
                )
                

def log_traceback(ex, ex_traceback):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    logging.debug(tb_text)

logging.debug('This message should go to the log file')

list = "this is a test".split()
try:
    print list[7]
except Exception as ex:
    _, _, ex_traceback = sys.exc_info()
    log_traceback(ex, ex_traceback)

logging.debug("got past the exception")


#==============================

DEBUG:root:This message should go to the log file
DEBUG:root:Traceback (most recent call last):
  File "/var/mobile/Containers/Data/Application/3469D264-D1AC-451E-9E4A-B3E38AD33B7F/Documents/chordcalc/test/Untitled.py", line 18, in <module>
    print list[7]
IndexError: list index out of range

DEBUG:root:got past the exception
