import Image
from Cleanbar import cleanbar
import photos, speech, console

speech.say('left image?', '', .18)
s1 = cleanbar(photos.pick_image())
speech.say('right image?', '', .18)
s2 = cleanbar(photos.pick_image())

w = s1.size[0] + s2.size[0] + 60
h = max(s1.size[1], s2.size[1]) + 40
ss = Image.new('RGB', (w,h), '#888')
ss.paste(s1, (20, (h - s1.size[1])/2))
ss.paste(s2, (s1.size[0] + 40, (h - s2.size[1])/2))
console.clear()
ss.show()
