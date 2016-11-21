# coding: utf-8

# https://forum.omz-software.com/topic/2697/workaround-for-multiple-file-sharing/10

files = {"averages.py"}
# This program will calculate the average value of a list of floats.

stored = []
average = 0
keep_adding = True

while keep_adding == True:
    entered_value = raw_input("Enter a number, or end: ")
    if entered_value == "end":
        break
    elif entered_value == "alpha":
        print 7.6
    else: 
        stored.append(float(int(entered_value)))
        
for num in stored:
    average += num

print "Average: "+str(float(average/len(stored)))'''}

for file in files.keys():
    open(file,"w").write(files[file])

#==============================

# coding: utf-8

files = {"averages.py":'''# coding: utf-8
# This program will calculate the average value of a list of user entered floats.

from __future__ import division

stored = []

while True:
    entered_value = raw_input("Enter a number, or end: ").lower()
    if entered_value == "end":
        break
    elif entered_value == "alpha":
        print(7.6)
    else:
        stored.append(float(entered_value))

print("Average: " + str(sum(stored) / len(stored)))'''}

for filename in files:
    with open(filename, "w") as out_file:
        out_file.write(files[filename])
