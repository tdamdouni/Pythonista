# # https://github.com/lukaskollmer/pythonista

import os
import editor


def custom_themes():
	home = os.getenv('CFFIXED_USER_HOME')
	user_themes_path = os.path.join(home, 'Library')
	
	print(os.listdir(user_themes_path))

def get():
	return editor.get_theme_dict()
	
def background_color():
	return get().get("background")

if __name__ == "__main__":
	import json
	print(json.dumps(get(), indent=4))
	#print(get())
	#print(background_color())
