# coding: utf-8

# https://gist.github.com/danrcook/369bf95d2a4d857f00fc84a0c1f261a8

# https://forum.omz-software.com/topic/3373/sharing-logging_setup

'''
Something to simplify use of the logging module, for use in Pythonista. This is set up to write to different files if used for different moduels.

Setup: Place this in the site-packages folder as 'logging_setup.py'

Usage:
	import logging
	import logging_setup
	log = logging_setup.logging_setup('my_log') #use a unique name
	log.debug('a message for debug')
	logging.shutdown() #necessary at the end of the script running

Quick Setup:
	import logging
	import logging_setup
	log = logging_setup.logging_setup('my_log') #use a unique name
	log.debug('a message for the log')
	log.error('oh no.')
	log.warning('oh no.')
	log.critical('call 911... or omz')
	log.info('well now it seems you have some mighty fine logging going on.')
	logging.shutdown() #necessary at the end of the script running

Keywords:
	- "mode" default is 'w' for rewrite. 'a' for append
	- "level" default is 'debug' (lowest)
	- "fmt" default example: "DEBUG: Here is something to debug". Please read logging docs if you want to set up a different format. fmt=('%(message)s') will log only messages

Reccommended Usage for levels (from logging docs:
	DEBUG: Detailed information, typically of interest only when diagnosing problems.
	
	INFO: Confirmation that things are working as expected.

	WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

	ERROR: Due to a more serious problem, the software has not been able to perform some function.

	CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
'''


import logging

def logging_setup(name, mode='w', level='DEBUG', fmt='%(levelname)s:\t%(message)s'):
	'''simple setup for logging module'''

	log = logging.getLogger(name) 
	log.setLevel(level)
	
	file_handler = logging.FileHandler(name + '_log.txt', mode=mode)
	file_handler.setLevel(level) 
	
	formatter = logging.Formatter(fmt=fmt) 
	
	file_handler.setFormatter(formatter)
	
	log.addHandler(file_handler)

	return log

#def logging_setup(filename=None, filemode='w', level='DEBUG',
#                  format='%(levelname)s:\t%(message)s'):
#    '''simple setup for logging module'''
#    filename = filename or __file__.rpartition('.')[0] + '.log'
#    logging.basicConfig(filename=filename, filemode=filemode, format=format,
#                        level=level)
#    return logging.getLogger()

#log = logging_setup()

if __name__ == '__main__':
	log = logging_setup('my_log')
	m = 'this is my variable'
	log.debug('this is a')
	log.info('some info about a variable: %s' % m)
	log.warning('a warning')
	log.error('an error')
	log.critical('something critical')
	logging.shutdown() #don't forget it!!

