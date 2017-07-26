#!python2
import matplotlib.pylab as plt

data = []
data2 = []
for i in range(30):
	data.append(i)
	data2.append(i**2)

plt.figure('lin')
plt.xlabel('x')
plt.ylabel('y')
plt.title('linear')
plt.plot(data, data)
plt.show()

plt.figure('quad')
plt.xlabel('x')
plt.ylabel('y')
plt.title('quadratic')
plt.plot(data, data2)
plt.show()
