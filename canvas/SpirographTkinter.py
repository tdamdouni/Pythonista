from __future__ import print_function
#Spirograph.py

# https://github.com/The-Penultimate-Defenestrator/Python/blob/master/Spirograph.py

# https://forum.omz-software.com/topic/2532/python-spirographs-anyone

from math import *
from Tkinter import *
import tkColorChooser
import time

thecolor = "#000000"
tk = Tk()

tk.configure(background='white')
run = 0

#Main Widgets
Tlabel = Label(text="Spirograph", background="white")
Tlabel.grid(row=0, column=0, columnspan=3)

Lframe = Frame(tk, bg="white")
Lframe.grid(row=1, column=0)

canvas = Canvas(tk, width=500, height=500, highlightthickness=0)
canvas.grid(row=1, column=1)
canvas.configure(scrollregion=(-250, -250, 250, 250), bg="white")

Rframe = Frame(tk, bg="white")
Rframe.grid(row=1, column=2)

Bframe = Frame(tk, bg="white")
Bframe.grid(row=2, column=0, columnspan=3)

label1 = Label(Rframe, text="Angular Velocities", bg="white")
label1.grid(row=0, column=0, columnspan=2)

scale1 = Scale(Rframe, from_=10, to=-10, resolution=0.1, label="1", bg="white", length=150, highlightthickness=0)
scale1.grid(row=1, column=0)

scale2 = Scale(Rframe, from_=10, to=-10, resolution=0.1, label="2", bg="white", length=150, highlightthickness=0)
scale2.grid(row=1, column=1)

label2 = Label(Lframe, text="Arm Lengths", bg="white")
label2.grid(row=0, column=0, columnspan=2)

scale3 = Scale(Lframe, from_=100, to=0, resolution=1, label="1", bg="white", length=150, highlightthickness=0)
scale3.grid(row=1, column=0)

scale4 = Scale(Lframe, from_=100, to=0, resolution=1, label="2", bg="white", length=150, highlightthickness=0)
scale4.grid(row=1, column=1)


def create_point(coords, canv=canvas):
    assert len(coords) == 2
    canv.create_line(coords[0], coords[1], coords[0]+1, coords[1]+1)

def create_line(coords1, coords2, canv=canvas):
    line = canvas.create_line(coords1[0], coords1[1], coords2[1], coords2[1])
    return line
def border():
    canvas.create_line(-250, -250, -250, 250)
    canvas.create_line(-250, -250, 250, -250)
    canvas.create_line(249, 249, 249, -249)
    canvas.create_line(249, 249, -249, 249)

def rotate(point, angle, center=(0, 0)):
    counterangle = 360 - angle
    while counterangle > 0: counterangle -= 360
    while counterangle < 0: counterangle += 360
    theta = radians(counterangle)
    #Translate point to rotate around center
    translated = point[0]-center[0] , point[1]-center[1]
    #Rotate point
    rotated = (translated[0]*cos(theta)-translated[1]*sin(theta),translated[0]*sin(theta)+translated[1]*cos(theta))
    #Translate point back
    newcoords = (round(rotated[0]+center[0], 1),round(rotated[1]+center[1], 1))
    return newcoords

def createSpiral(armOne, armTwo, color):

    clearbutton.config(text="Stop Drawing")

    x, y = 0, 0
    len1, step1 = armOne
    len2, step2 = armTwo
    global lines
    lines = []
    previousPositions = []

    while step1 > 10 or step2 > 10:
        step1 /= 2
        step2 /= 2

    global run
    run = 1
    iteration = 1
    inarow = 0
    while run:
        scale1.set(step1)
        scale2.set(step2)
        iteration += 1

        point1 = rotate((0,len1), x)
        point2 = map(sum,zip(rotate((0, len2), y), point1))

        #Detection of whether pattern is repeating itself
        if point2 not in previousPositions:
            previousPositions.append(point2)
            inarow = 0
        else:
            inarow += 1

        if inarow > 5:
            print("Pattern is detected to be repeating itself")
            run = 0


        if x == 0:
            oldpoint2 = point2
        else:
            canvas.create_line(oldpoint2[0], oldpoint2[1], point2[0], point2[1], fill=color)
        lines.append( canvas.create_line(0, 0, point1[0], point1[1], fill="#5CE6E6", width=3.0) )
        lines.append( canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill="#5CE6E6", width=3.0) )
        oldpoint2 = point2

        tk.update()

        x += step1
        if x > 360: x -= 360
        y += step2
        if y > 360: y -= 360

        for line in lines:
            canvas.delete(line)
        lines = []
        time.sleep(0.005)
    print("Done!")
    clearbutton.config(text="Clear Canvas")

def getColor():
    global thecolor
    thecolor = tkColorChooser.askcolor("black")[1]
    print(thecolor)

def graph():
    len1 = scale3.get()
    len2 = scale4.get()
    vel1 = scale1.get()
    vel2 = scale2.get()
    createSpiral((len1, vel1), (len2, vel2), thecolor)

def clear():
    canvas.delete("all")
    border()

def STOPPIT():
    global run, lines
    run = 0
    for line in lines:
        canvas.delete(line)
    lines = []

def universalCommand():
    if run:
        STOPPIT()
    else:
        clear()

colorchooserbutton = Button(Bframe, text='Select Color', command=getColor, bg="white")
colorchooserbutton.pack(side=LEFT, padx=5)

button = Button(Bframe, text="Create Spiral", command=graph, bg="white")
button.pack(side=LEFT, padx=5)

clearbutton = Button(Bframe, text="Clear Drawing", command=universalCommand, bg="white")
clearbutton.pack(side=LEFT, padx=5)

border()
while 1:
    tk.update()