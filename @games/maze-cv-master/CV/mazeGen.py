'''Main module, puts together all CV modules'''
from PIL import Image
import bradley, perspective, redFinder

def finalScan(image):
	'''Generate a clean maze image from a photo of the maze template'''
	sm=min(image.size)
	
	#Find red corners
	corners = redFinder.cornerCoords(image)
	p=image.convert('L')
	
	#Apply perspective transform
	transformed=perspective.transform(corners,perspective.squarecorners(p),p).crop((0,0,sm,sm))
	
	#Apply thresholding
	thresh=bradley.bradley_threshold(transformed)
	
	#Apply second, more precise perspective transform to make image clearer/smoother
	l=thresh.load()
	#list of all black pixels
	blacks = sum([[(x, y) for x in range(thresh.size[0]) if not l[x,y]] for y in range(thresh.size[1])], [])
	thresh=perspective.transform((
		min(blacks, key=lambda x:redFinder.manhattan(x,(0,0))),
		min(blacks, key=lambda x:redFinder.manhattan(x,(sm,0))),
		min(blacks, key=lambda x:redFinder.manhattan(x,(sm,sm))),
		min(blacks, key=lambda x:redFinder.manhattan(x,(0,sm)))),
		perspective.absolutecorners(thresh), thresh)
	
	#crop image into 256 pieces (16x16)
	pixsize = thresh.size[0]/16
	segments = []
	for i in range(16):
		for j in range(16):
			box = (j*pixsize,i*pixsize,(j+1)*pixsize,(i+1)*pixsize)
			segments.append(thresh.crop(box))
	
	def blackWhite(image):
		'''Return `True` if the image is mostly white, else `False` Weigh center pixels more heavily.'''
		l=image.convert('L').load()
		w,h=image.size
		coords = sum([[(x, y) for x in range(w)] for y in range(h)],[])
		lums=[l[x,y] for x,y in coords]
		#Weights based on function y = -0.5|x-8|+4
		weights=[(-0.5*abs(x-8)+4)*(-0.5*abs(y-8)+4) for x,y in coords]
		weighted=[lum*weights[num] for num,lum in enumerate(lums)]
		return sum(weighted)/sum(weights)>127
	
	#Create maze image
	maze = Image.new('L',(16,16))
	l=maze.load()	
	for y in range(16):
		for x in range(16):
			seg = segments[16*y+x]
			l[x,y]=blackWhite(seg)*255
	
	return maze

if __name__ == '__main__':
	img = Image.open('../Test Images/photo1.jpg').resize((320,240))
	finalScan(img).show()