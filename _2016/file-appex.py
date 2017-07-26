# https://forum.omz-software.com/topic/3765/use-existing-scripts-from-outside-pythonista/4

import appex

def main():
	if appex.is_running_extension():
		for file_path in appex.get_file_paths():
			print(file_path)

