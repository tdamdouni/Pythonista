from __future__ import print_function
# Editorial Reminders

# https://forum.omz-software.com/topic/2429/editorial-reminders/2

def extract_alarm_info(alarm_text):
	for name, s_time in re.findall(r'(.*)@alarm\((.*)\)', alarm_text):
		date, time = s_time.split(', ')
		d_yyyy, d_mm, d_dd = [int(x) for x in date.split('-')]
		t_hh, t_mm = [int(x) for x in time.split(':')]
		
	return {
	'year'      : d_yyyy,
	'month'     : d_mm,
	'day'           : d_dd,
	'hour'      : t_hh,
	'min'           : t_mm,
	'date_str'  : date,
	'time_str'  : s_time,
	}
	
the_alarm = '@alarm(2015-12-10, 22:05)'
print(extract_alarm_info(the_alarm))

