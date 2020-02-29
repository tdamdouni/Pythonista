from __future__ import print_function
# https://gist.github.com/jefflovejapan/5076080

def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
	while True:
		ok = raw_input(prompt)
		if ok in ('y', 'ye', 'yes'):
			return True
		if ok in ('n', 'no', 'nop', 'nope'):
			return False
		retries = retries - 1
		if retries < 0:
			raise IOError('refusenik user')
		print(complaint)
		
p =ask_ok('whaddup sun?')
print(p)
