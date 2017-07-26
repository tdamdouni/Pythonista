# https://forum.omz-software.com/topic/3971/regex-help-request

def validate(s='00 - 00 - 00'):
	parts = s.split(' - ')
	return len(parts) == 3 and all(len(p) == 2 and p.isdigit() for p in parts)
	
# -----------------------

def validate_with_re(s='00 - 00 - 00'):
	return bool(re.search(r'^\d\d - \d\d - \d\d$', s))

