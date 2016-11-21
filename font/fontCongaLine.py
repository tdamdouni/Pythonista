import scene, os

colorLightBlue = scene.Color(.3, .3, 1)
colorWhite     = scene.Color( 1,  1, 1)

fontBlackList = ('AcademyEngraved', 'AppleColorEmoji@2x',
                 'ArialHB', 'Bodoni72', 'ChalkboardSE',
                 'CourierNew', 'DB_LCD_Temp-Black',
                 'EuphemiaCAS', 'Fallback', 'HoeflerText',
                 'LastResort', 'KGPW3UI', 'LockClock',
                 'PartyLET', 'PhoneKeyCaps', 'ZapfDingbats')

def getFontFunction():  # Don't call this directly...
	fileNames = []
	for fileName in os.listdir('/System/Library/Fonts/Cache'): #'../Pythonista.app'):
		if (fileName.endswith('.ttc')
		or fileName.endswith('.ttf')):
			fileName = fileName.rpartition('.tt')[0]
			if fileName.startswith('_H_'):
				fileName = fileName.partition('_H_')[2]
			if (fileName not in fontBlackList
			and 'Bold' not in fileName
			and 'Neue' not in fileName
			and 'Next' not in fileName
			and 'Light' not in fileName
			and 'Bodoni' not in fileName
			and 'Italic' not in fileName
			and 'Medium' not in fileName
			and 'OldStyle' not in fileName
			and 'Condensed' not in fileName
			and 'Old-Style' not in fileName
			and 'MarkerFelt' not in fileName):
				fileNames.append(fileName.partition('New')[0])
	for fileName in sorted(fileNames):
		yield fileName
getFontName = getFontFunction()  # Call getFontName.next()

class FontSampleLayer(scene.Layer):
	def __init__(self, inFontName = 'Helvetica'):
		(imageName, imageSize) = scene.render_text(inFontName,
		font_name=inFontName, font_size=64)
		theRect = scene.Rect(0, 0, imageSize.w, imageSize.h)
		super(self.__class__, self).__init__(theRect)
		self.tint = colorLightBlue
		# self.background = colorWhite  # useful for debugging
		self.image = imageName
		self.dx = 1
		self.dy = 1
		
	def move(self):
		self.frame.x += self.dx
		self.frame.y += self.dy
		sup = self.superlayer.frame
		if self.frame.x <= sup.x or (
		self.frame.x + self.frame.w >= sup.x + sup.w):
			self.dx = -self.dx           # change x direction
			self.frame.x += self.dx * 2  #  with a little hop
		if self.frame.y <= sup.y or (
		self.frame.y + self.frame.h >= sup.y + sup.h):
			self.dy = -self.dy           # change y direction
			self.frame.y += self.dy * 2  #  with a little hop
			
class FontSampleView(scene.Scene):
	def setup(self):
		self.frameCount = -1
		
	def draw(self):
		self.frameCount += 1
		if self.frameCount % 80 == 0:
			try:
				fontName = getFontName.next()
				print(fontName)
				self.add_layer(FontSampleLayer(fontName))
			except StopIteration:
				pass
		scene.background(0, 0, 0)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		for theLayer in self.root_layer.sublayers:
			if isinstance(theLayer, FontSampleLayer):
				theLayer.move()
				
if __name__ == "__main__":
	print('=' * 20)
	scene.run(FontSampleView())

