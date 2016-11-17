# https://forum.omz-software.com/topic/3600/indexerror-happens-in-pythonista-3/3

import matplotlib.pyplot as plt;

x = [ ];
y = [ ];

readFile = open('xy.txt','r');

for line in readFile:

	print(line);

splitUP = line.split();

print('x =',splitUP[0],'and y =',splitUP[1]);

x.append(splitUP[0]);
y.append(splitUP[1]);
readFile.close();

plt.plot(x,y);

plt.show();

print(splitUP)

print(splitUP, len(splitUP))
