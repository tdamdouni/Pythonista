### NAME

**SmallTime date entry** – Python script for translating simple informal and relative date-time expressions into standard TaskPaper format YYYY-MM-DD [HH:MM]
and for applying deferrals and forward time shifts  (+4d  -1w  etc)

### DESCRIPTION 

A simple script, small enough to drop into iPad Editorial workflows (c. 150 lines of code) which may serve as a stopgap while iOS installation of the more ambitious ParseDateTime remains a little more tricky than many users will find time for.

The translation function, which takes an informal or relative time expression (examples below), and returns a standard format TaskPaper expression, is:

    phrase_to_datetime(str_expression)

#### Also contains functions for:
1. Batch updating or translating all the relative @key(relative date) tags in a piece of text, and: 
	1. Reporting how many tags of each kind were updated
	2. Listing the keys of any unchanged @key(absolute date) which were found
2. Batch deferring (or bringing ahead) all @key(date) tags  (relative or absolute) of specified kinds e.g. ['start', 'due'] by specified amounts of time, e.g. '+4d', '-1w' etc


### EXAMPLES AND SCREEN SHOTS

Running the examples() function will show the following samples of input phrases and output date/time expressions:

    ('today +7d', '2014-02-18')
    ('11:20 +4d', '2014-02-15 11:20')
    ('2014-02-15 +1w', '2014-02-22')
    ('jan 10', '2015-01-10')
    ('jan 10 2pm', '2015-01-10 14:00')
    ('10 jan at 10am', '2015-01-10 10:00')
    ('now-3d', '2014-02-08 17:11')
    ('+7d', '2014-02-18')
    ('7', '2014-02-18')
    ('11:15', '2014-02-11 11:15')
    ('11:15p', '2014-02-11 23:15')
    ('11p', '2014-02-11 23:00')
    ('aug', '2014-08-01')
    ('jan 5', '2015-01-05')
    ('aug 2019', '2019-08-01')
    ('now', '2014-02-11 17:11')
    ('tomorrow 2pm', '2014-02-12 14:00')
    ('now +4h', '2014-02-11 21:11')
    ('today + 1w', '2014-02-18')
    ('1w', '2014-02-18')
    ('+3y', '2017-02-11')
    ('w', '2014-02-18')
    ('-w', '2014-02-04')


### SOURCE

The [Python source](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/small_time_006.py) is on Github at at [https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/small_time.py](https://github.com/RobTrew/tree-tools/blob/master/TaskPaper%20scripts/small_time_006.py)

