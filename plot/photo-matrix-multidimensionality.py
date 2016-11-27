# https://forum.omz-software.com/topic/3677/add-items-to-the-list-keeping-the-multidimensionality

from PIL import Image
import numpy as np

img = Image.open("photo.jpg")
arr = np.array(img)

x = []
h,w,rgb = arr.shape
size = 5

for i in range(0,h):
	for j in range(0,w):
		part = arr[i:i+size,j:j+size]
		if len(part)==size and len(part[0])==size:
			x.append(part)

print(part.shape)
