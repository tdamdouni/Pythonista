# http://stackoverflow.com/questions/33771195/putting-a-linear-regression-solution-together

from numpy import loadtxt, zeros, ones, array, genfromtxt, linspace, logspace, mean, std, arange
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from pylab import plot, show, xlabel, ylabel

#Evaluate the linear regression

def __init__(self, name):
	self.name = name
	
def feature_normalize(self.X):
	mean_r = []
	std_r = []
	X_norm = X
	n_c = X.shape[1]
	for i in range(n_c):
		m = mean(X[:, i])
		s = std(X[:, i])
		mean_r.append(m)
		std_r.append(s)
		X_norm[:, i] = (X_norm[:, i] - m) / s
	return X_norm, mean_r, std_r
	
	
def compute_cost(self, X, y, theta):
	'''
	Comput cost for linear regression
	'''
	#Number of training samples
	m = y.size
	
	predictions = X.dot(theta)
	
	sqErrors = (predictions - y)
	
	J = (1.0 / (2 * m)) * sqErrors.T.dot(sqErrors)
	
	return J
	
	
def gradient_descent(self, X, y, theta, alpha, num_iters):
	'''
	Performs gradient descent to learn theta
	by taking num_items gradient steps with learning
	rate alpha
	'''
	m = y.size
	J_history = zeros(shape=(num_iters, 1))
	
	for i in range(num_iters):
	
		predictions = X.dot(theta)
		
		theta_size = theta.size
		
		for it in range(theta_size):
		
			temp = X[:, it]
			temp.shape = (m, 1)
			
			errors_x1 = (predictions - y) * temp
			
			theta[it][0] = theta[it][0] - alpha * (1.0 / m) * errors_x1.sum()
			
		J_history[i, 0] = compute_cost(X, y, theta)
		
	return theta, J_history
	
#Load the dataset



#Plot the data
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
for c, m, zl, zh in [('r', 'o', -50, -25)]:
    xs = data[:, 0]
    ys = data[:, 1]
    zs = data[:, 2]
    ax.scatter(xs, ys, zs, c=c, marker=m)
ax.set_xlabel('Size of the House')
ax.set_ylabel('Number of Bedrooms')
ax.set_zlabel('Price of the House')
plt.show()
'''

def calctheta(self, name):
	data = genfromtxt (name, delimiter=",")
	y = data[:,0]
	X = data[:,1:11]
	
	
	#number of training samples
	m = y.size
	
	y.shape = (m, 1)
	
	#Scale features and set them to zero mean
	x, mean_r, std_r = feature_normalize(X)
	
	#Add a column of ones to X (interception data)
	it = ones(shape=(m, 12))
	it[:, 1:12] = x
	
	#Some gradient descent settings
	iterations = 100
	alpha = 0.01
	
	#Init Theta and Run Gradient Descent
	theta = zeros(shape=(11, 1))
	
	theta, J_history = gradient_descent(it, y, theta, alpha, iterations)
	print theta
	plot(arange(iterations), J_history)
	xlabel('Iterations')
	ylabel('Cost Function')
	show()

