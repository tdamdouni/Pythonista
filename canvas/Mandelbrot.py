from __future__ import print_function
from math import log
import canvas

H = 1000 #number of different colors in list to use
iterations = 1000 #high for greater detail
colorDensity = 30 #controls how close together the colors are, the higher the closer
ColorList = []

#Majority of processing work completed here.
#Calculates how close a point is to the mandelbrot set
def mandelbrot(real, imag):
        z = 0j
        c = complex(real, imag)
        for i in range(iterations):
                if abs(z) < 2:
                        z = z**2 + c
                else:
                        break
        for a in range(4): #Removes most imperfections in the image
            z = z**2 + c
        return i,z

#Interpolates (Smooths) between 2 different colours
def interpolateC(color,endColor,left):
        if left == 0:
                return color
        rStart = color[0]
        gStart = color[1]
        bStart = color[2]
        rEnd = endColor[0]
        gEnd = endColor[1]
        bEnd = endColor[2]
        rDiff = rEnd-rStart
        gDiff = gEnd-gStart
        bDiff = bEnd-bStart
        rInc = float(rDiff)/left
        gInc = float(gDiff)/left
        bInc = float(bDiff)/left
        #print (str(left))
        return [rStart+rInc,gStart+gInc,bStart+bInc]

#Reads colour stops from a file chosen by the user using the tkinter library
def getPoints():
        #pointsList = [[0.0,0.0,0.0],[float(217)/255,float(203)/255,float(132)/255]] #change me
        pointsList = [[0.0,0.0,0.0],[float(255)/255,float(255)/255,float(255)/255]] #change me
        backwards = pointsList[0:-1]
        backwards.reverse()
        return pointsList+backwards

#Sets up a list of colours for the rendering to use from the points file
def colorList():
        cols = []
        points = getPoints()
        print(points)
        eachLength = H/(len(points)-1)
        howmanytogo = eachLength
        
        for a in range(1,len(points)):
                cols.append(points[a-1])
                for i in range (0,eachLength):
                        cols.append(interpolateC(cols[-1],points[a],howmanytogo))
                        howmanytogo += -1


                howmanytogo = eachLength
        global ColorList
        ColorList = cols

#Turns a number into a colour for the renderer to display
def toColor(a):
        a=a*colorDensity
        a = int(a)%H
        try:
                a = ColorList[int(a)]
                return [int(a[0]*255),int(a[1]*255), int(a[2]*255)]
        except IndexError:
                print(a)
                print(len(ColorList))
                return [0,0,0]

def v(z,n):
        try:
                x = n + 1 - (log(log(abs(z),2),2)/log(2,2))
                return x
        except ValueError:
                return 0

def heightVals(pixSize, t, b, pixH):
        hList = []
        locCount = t-pixSize/2
        while locCount>b:
                hList.append(locCount)
                locCount -= pixSize
        if pixH == len(hList):
                return hList
        else:
                print("oh dear... something's gone wrong", hList, t, b, locCount)


def widthVals(pixSize, l, r, pixW):
        wList = []
        locCount = l+pixSize/2
        while locCount<r:
                wList.append(locCount)
                locCount += pixSize
        if pixW == len(wList):
                return wList
        else:
                print("oh dear... something's gone wrong", wList, r, l, locCount)

colorList()

w = int(raw_input("Width in pixels:"))
h = int(raw_input("Height in pixels:"))
x = float(raw_input("X position:"))
y = float(raw_input("Y position:"))
zoom = float(raw_input("Zoom level:"))

canvas.set_size(w,h)


ratio = 100
pixelSize = (float(3)/float(w))/float(zoom)
left = x-((w/2)*pixelSize)
right = x+((w/2)*pixelSize)
top = y+((h/2)*pixelSize)
bottom = y-((h/2)*pixelSize)

wVals = widthVals(pixelSize, left, right,w)
hVals = heightVals(pixelSize, top, bottom,h)

lastPercentage = 0
print("0%")
a_count = 0
for a in hVals:
        canvas.begin_updates()
        b_count = 0
        for b in wVals:
                n, z = mandelbrot(b,a)
                if (n == iterations):
                        col = [0,0,0]
                else:
                        #print(v(z,n))
                        col = toColor(v(z,n))
                        #col = [1,1,1]
                canvas.set_fill_color(float(col[0])/255,float(col[1])/255,float(col[2])/255)
                canvas.fill_pixel(b_count,a_count)
                b_count += 1
        
        curPerc = 100-(int((a-bottom)/(top-bottom)*100))
        if curPerc>=lastPercentage+1:
            lastPercentage=curPerc
            print(str(lastPercentage)+"%")
        a_count+=1
        canvas.end_updates()
