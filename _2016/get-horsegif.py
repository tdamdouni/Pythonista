import console, requests

url = 'http://bestanimations.com/Animals/Mammals/Horses/horse-walking-animated-gif1.gif'
url = 'http://fc00.deviantart.net/fs71/f/2012/189/a/a/dressage_horse_animation_by_lauwiie1993-d56it04.gif'
filename = url.split('/')[-1]

with open(filename, 'wb') as out_file:
	out_file.write(requests.get(url).content)
console.quicklook(filename)

