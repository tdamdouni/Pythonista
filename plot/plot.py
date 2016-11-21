import matplotlib.pyplot as plt

x = range(15)
plt.plot(x, [xi**2 for xi in x])
plt.ylabel('Number of stocks')
plt.xlabel('Number of months')
plt.show()
