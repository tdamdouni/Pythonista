import console
import editor
import keyword
import os
import string
import sys

ALLOWED_CHARS = set(string.ascii_letters + string.digits + string.whitespace + "_.")
DOCS = os.path.expanduser("~/Documents")

def preformat(name):
	name = str(name).strip()
	if name.startswith("from "):
		name = name[len("from "):].strip()
		if " import " in name:
			name = name[:name.rfind(" import ")].strip()
	elif name.startswith("import "):
		name = name[len("import "):].strip()
		
	if " as " in name:
		name = name[:name.rfind(" as ")].strip()
		
	return name
	
def is_valid_name(name):
	name = str(name).strip()
	
	# False strings are always invalid
	if not name:
		return False
		
	# Check for illegal chars by deleting all allowed ones and checking len
	if set(name) in ALLOWED_CHARS:
		return False
		
	# Check individual submodule parts
	parts = name.split(".")
	for part in parts:
		part = part.strip()
		
		# Skip part if empty
		if not part:
			continue
			
		# Check if part is keyword, starts with number or has invalid whitespace
		if keyword.iskeyword(part) or part[0] in string.digits or len(set(part) & set(string.whitespace)) > 0:
			return False
			
	# All tests passed, assumed a valid module name
	return True
	
def find_path(name):
	# Reject invalid module names
	if not is_valid_name(name):
		raise ValueError(name + " is not a valid module name")
		
	name = str(name).strip()
	
	# Check if built-in
	if name in sys.builtin_module_names:
		return "<built-in>"
		
	# Check all sys.path locations
	for p in sys.path:
		loc = os.path.abspath(os.path.join(p, name + ".py"))
		if os.path.exists(loc) and os.path.isfile(loc):
			return loc
			
	# Last resort, import module and check __file__
	try:
		mod = __import__(name)
	except ImportError:
		# Everything failed, assume nonexistant
		return "<string>"
	return mod.__file__ if hasattr(mod, "__file__") else "<built-in>"
	
def main(args):
	if args:
		name = args[0]
	else:
		sel = editor.get_selection() or ""
		seltxt = preformat(editor.get_text()[sel[0]:sel[1]])
		if sel and sel[0] != sel[1] and is_valid_name(seltxt):
			name = seltxt
		else:
			name = console.input_alert("Find Module")
			
	try:
		loc = find_path(name)
	except ValueError:
		console.hud_alert(name + " is not a valid module name", "error")
		return
		
	if loc == "<built-in>":
		console.hud_alert(name + " is a built-in module", "error")
	elif loc == "<string>":
		console.hud_alert("Could not find module " + name, "error")
	else:
		editor.open_file(os.path.relpath(loc, DOCS))
		
if __name__ == "__main__":
	main(sys.argv[1:])

