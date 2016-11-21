import bs4, collections, console, requests, scene

tkColorDict = collections.OrderedDict()  # key = tkinter color name

def loadTkColorDict():  # will automaticly be called by getColor() if needed
	tkColorURL = 'http://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm'
	print('Loading tkinter colors from: ' + tkColorURL)
	tkColorSoup = bs4.BeautifulSoup(requests.get(tkColorURL).text).tbody
	print('Soup is ready.  Creating color table...')
	for tableRow in tkColorSoup.find_all('tr'):
		colorInfo = [x.text for x in tableRow.find_all('p')]
		if colorInfo[0] != 'Name':  # skip the table header
			tkColorDict[colorInfo[0]] = (int(colorInfo[1]) / 255.0,  # red
			int(colorInfo[2]) / 255.0,  # green
			int(colorInfo[3]) / 255.0)  # blue
	# optionaly show the results...
	for colorName in tkColorDict:  # 752 colors
		#console.set_color(*tkColorDict[colorName])  # some colors are not visible
		print('{:<22} = {}'.format(colorName, tkColorDict[colorName]))
	print('tkColorDict now contains {} colors.\n'.format(len(tkColorDict)))
	
def getColor(inColorName = 'grey'):
	if not tkColorDict:    # if   tkColorDict has not been initialized
		loadTkColorDict()  # then put tkinter colors into tkColorDict
	try:
		return scene.Color(*tkColorDict[inColorName])
	except KeyError:
		print("'{}' is not a valid color.  Substituting grey...".format(inColorName))
		return getColor()
		
if __name__ == '__main__':
	lgy = getColor('light goldenrod yellow')
	#console.set_color(lgy.r, lgy.g, lgy.b)  # some colors are not visble
	print("getColor('{}') = ({}, {}, {})".format('light goldenrod yellow', lgy.r, lgy.g, lgy.b))
	
	testColorNames = ('black white red green blue Bob').split()
	for testColorName in testColorNames:
		testColor = getColor(testColorName)
		console.set_color(testColor.r, testColor.g, testColor.b)
		print("getColor('{}') = ({}, {}, {})".format(testColorName, testColor.r, testColor.g, testColor.b))
	console.set_color(0, 0, 0)  # back to black

