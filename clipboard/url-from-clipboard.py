# Source https://gist.github.com/Blether/7665238

import clipboard

clipcontents = clipboard.get()
new_clip = clipcontents[clipcontents.find('htt'):].split()[0]

clipboard.set(new_clip)
print('Clipboard now contains:\n' + new_clip)
