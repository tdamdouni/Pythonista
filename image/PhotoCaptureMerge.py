# coding: utf-8

# http://mygeekdaddy.net/2016/01/12/capture-and-merge-photos-with-pythonista/

# Prompts user to take 2 pictures and merges the two images together    
from __future__ import print_function
import clipboard
import Image
import console
import photos

console.clear()

console.alert("Take first image", "", "Ok")
img1=photos.capture_image()

console.alert("Take second image", "", "Ok")
img2=photos.capture_image()

console.show_activity()

w1,h1 = img1.size
w2,h2 = img2.size

# Set the width and height of each image
img1_w = img1.size[0]
img1_h = img1.size[1]
img2_w = img2.size[0]
img2_h = img1.size[1]

def image_merge(img):
    if (img1_w*1.0)/img1_h > 1:
        print('Landscape screenshot...')
        background = Image.new('RGB', ((img1_w+20), ((img1_h*2)+30)), (255,255,255))
        print("Generating image...")
        background.paste(img1,(10,10))
        background.paste(img2,(10,(img1_h+20)))
        photos.save_image(background)
        print("Image saved") 
    else:
        print('Portrait screenshot...')
        background = Image.new('RGB', (((img1_w*2)+30),(img1_h+20)), (255, 255, 255))
        print("Generating image...")
        background.paste(img1,(10,10))
        background.paste(img2,((img1_w+20),10))
        photos.save_image(background)   
        print("Image saved")

if img1_w == img2_w:
    image_merge(img1)
else:
    console.alert("Incorrect image ratio", "", "Ok")