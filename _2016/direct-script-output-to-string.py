# https://forum.omz-software.com/topic/3953/direct-script-output-to-string

# Run the main script:
	if (scriptPath) {
	NSString *script = @"from sympy import *\ninit_printing(use_unicode=True)\nx = Symbol('x')\nprint(solve(x**2 - 1, x))";
	if (script) {
	[[PythonInterpreter sharedInterpreter] run:script asFile:scriptPath];
	} else {
	NSLog(@"Could not load main.py (make sure its encoding is UTF-8)");
	}
	} else {
	NSLog(@"Could not find main.py");
	}
# --------------------
def _capture_output_main():
	import _outputcapture
	import sys
	
	class StdoutCatcher (object):
		def __init__(self):
			self.encoding = 'utf8'
		def write(self, s):
			if isinstance(s, str):
				_outputcapture.CaptureStdout(s)
			elif isinstance(s, unicode):
				_outputcapture.CaptureStdout(s.encode('utf8'))
		def writelines(self, lines):
			for line in lines:
				self.write(line + '\n')
		def flush(self):
			pass
			
	class StderrCatcher (object):
		def __init__(self):
			self.encoding = 'utf8'
		def write(self, s):
			if isinstance(s, str):
				_outputcapture.CaptureStderr(s)
			elif isinstance(s, unicode):
				_outputcapture.CaptureStderr(s.encode('utf8'))
		def flush(self):
			pass
			
	class StdinCatcher (object):
		def __init__(self):
			self.encoding = 'utf8'
		def read(self, len=-1):
			return _outputcapture.ReadStdin(len)
			
		def readline(self):
			return _outputcapture.ReadStdin()
			
	sys.stdout = StdoutCatcher()
	sys.stderr = StderrCatcher()
	sys.stdin = StdinCatcher()
	
_capture_output_main()
del _capture_output_main
# --------------------

