# https://forum.omz-software.com/topic/3499/simple-file-download/9

# https://gist.github.com/jsbain/fcb3f42932dde9b0ff6c122893d1b230

with open(destpath,'wb') as file:
	file.write(requests.get(url).content)

