# https://gist.github.com/jefflovejapan/5076080

def front_x(words):
	# +++your code here+++
	xwords = []
	noxwords = []
	endwords =[]
	for word in words:
		if word[0] == 'x':
			xwords.append(word)
		else:
			noxwords.append(word)
	xwords.sort()
	noxwords.sort()
	endwords = xwords + noxwords
	return endwords
	
derp = ['mix', 'xyz', 'apple', 'xanadu', 'aardvark']
front_x(derp)

