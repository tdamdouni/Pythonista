# https://gist.github.com/SamyBencherif/b08f63366f54294a179c
"""
Curve Fit

Gives a point function that intersects any given set of points.

Eg.
(1,1),(2,2) ->	(0t^2+1t^1+0t^0,0t^2+1t^1+0t^0)

Written by Samy Bencherif
Using Pythonista for iOS
"""

def powiter(length, i):
    k = [1]
    for j in range(1,length):
        k.append(i**j)
    return k[::-1]

def oper(r, a, b):
    if type(a)!=list:
    	a = [a]*len(b)
    if type(b)!=list:
    	b = [b]*len(a)
    k = []
    for i in range(len(a)):
        k.append(eval('float(%f)%sfloat(%f)' % (a[i], r, b[i])))
    return k

points = raw_input("Points: ")
points = list(eval(points.replace(' ', '')))
Imatrix = []
Omatrix = []
for i in range(len(points)):
    Imatrix.append(powiter(len(points), i+1)+[points[i][0]])
    Omatrix.append(powiter(len(points), i+1)+[points[i][1]])
    
coef = []

for matrix in (Imatrix, Omatrix):
    for row in range(len(matrix)):
        for subrow in range(row+1, len(matrix)):
            matrix[subrow] = oper('-', matrix[subrow], oper('*', float(matrix[subrow][row])/float(matrix[row][row]), matrix[row]))
    for row in range(len(matrix)-1,-1,-1):
        for subrow in range(row-1,-1,-1):
            i = row-len(matrix)-1
            matrix[subrow][-1]-=(matrix[row][-1]/matrix[row][i])*matrix[subrow][i]
            matrix[subrow][i]=0
    coef.append([matrix[row][-1]/matrix[row][row] for row in range(len(matrix))])

#lazy synthesizer
k = ''
for i in range(len(coef[0])):
	k = str(coef[0][::-1][i])+'t^'+str(i)+'+'+k

g = ''
for i in range(len(coef[1])):
	g = str(coef[1][::-1][i])+'t^'+str(i)+'+'+g

print('(%s,%s)'%(k[:-1],g[:-1]))

#find a b c d values of matix
# at^3+bt^2+ct+d