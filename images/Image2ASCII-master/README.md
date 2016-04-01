# Image2ASCII
Python application to convert images to ASCII art.

This is a python module that can convert any arbitrary image to ASCII art. It contains a module, `Image2ASCII.py`, that contains two functions.

##Functions

####image2ASCII
The first function contained in `Image2ASCII.py` is `image2ASCII`. It can be used like `image2ASCII(im)` where im is a PIL image. For any image you provide, it does a few things.
* Crop the image: the first real thing the function does is crop the image to be the largest possible square, which it centers in the top left.
* Convert the image to black and white: for our use, we don't need the image to have multiple values with color. We only need it to have areas of brightness. We convert it to type 'L' for luminosity, that only has one value to work with.
* Compress the image: We need the image to be a size so that one pixel corresponds to one character. We don't want it to be too big! By default, the image is 200 pixels wide
* Strech the image: Fonts are typically taller than they are wide. When we print out ASCII art this way, it appears to be streched vertically. By squishing it down beforehand, it appears normal in text.
* Actually generate the art: We iterate through the image, pixel by pixel, and decide on a character that would have appropriate 'visual weight'
Then, the art is returned to you as a string with line breaks (`\n`)

The function can also be used to show the starting image beforehand or generate art of a different size. In this case, you can use `image2ASCII(im, scale, showimage)`, where scale is an integer and showimage is a boolean value. 

#####Example
The image ![Circle](https://www.easycalculation.com/area/images/circle.gif), at a size of 20x20 looks like this:
```
                    
      ,iv||/-       
   ./i|=~_cvivc,    
  /v/|c||c~v!~vi\   
 c~==~\/cc|/_civ~/  
 vv!vv|c=!v~~i|/_\  
 |!|~icvc|/~==_v_!  
  /_\|/v/iv~~ii!!   
   ,~i\c__|~c~!,    
      -=|\vi.       
```
####RenderASCII
The second function in `Image2ASCII.py` is `RenderASCII`. It can be used like `RenderASCII(text)`, where text is a string. The function is designed to render text from `image2ASCII` onto an image for easy viewing, without copy/pasting from the console. Rendering the text from the ball looks pretty much the same as the ball text pasted above. This same rendering method works quickly with big images.
#####Example
![Imgur](http://i.imgur.com/WWw63u4.jpg)

##Example Script
```
from Image2ASCII import *
image = Image.open("Test_Images/Calvin.jpg") #Open the image
ascii = image2ASCII(image)                   #Convert the image to ASCII
outputimage = RenderASCII(ascii)             #Render the ASCII
outputimage.show()                           #Show the final product
```
This shows a rendered ASCII art image of the provided image of Calvin.
