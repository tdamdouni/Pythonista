# coding: utf-8

# https://gist.github.com/S0n1cDev/475ac5d879e84eea9f55

from objc_util import *
UIScreen = ObjCClass('UIScreen')
	
def main():
	screen = UIScreen.mainScreen()
	if screen.brightness() < 0.3:
		screen.setBrightness_(0.6)
	else:
		screen.setBrightness_(0.1)

if __name__ == '__main__':
	main()
