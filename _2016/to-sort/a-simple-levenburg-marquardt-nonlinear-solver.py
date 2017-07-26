# https://gist.github.com/jsbain/a8885911babb1967bc949dfce072010e

# simple numpy optimization example
import numpy as np


def jacobian(f,x0):
	# given a function f(*x)
	# derive df/dx
	f0=f(x0)
	dx=0.00001
	dfdx=np.matrix(np.zeros([len(f0),len(x0)]))
	for i in range(len(x0)):
		x=x0
		x[i]+=dx
		dfdx[:,[i]]=(f(x)-f0)/dx
	return f0,dfdx
	
def solve(f, y,x0, maxiter):
	L=.01 #lambda damping factor
	v=1.5 #damping adjustment factor
	x=x0
	f0,J=jacobian(f,x)
	F=f0-y
	S0=F.conj().T*F
	i=0
	while i<maxiter:
		print(i,S0.tolist()[0],x.T.tolist()[0],L)
		# compute step
		JtJ=J.conj().transpose()*J	
		#U=JtJ + L*np.diagflat(JtJ.diagonal())
		U=JtJ + L*np.eye(JtJ.shape[0])
		dx=np.linalg.lstsq(U, -J.transpose()*(f0-y))[0]
		F=f(x+dx)-y
		S=F.conj().T*F
		if S<S0:
			L=L/v
			x=x+dx
			f0,J=jacobian(f,x)
			S0=S
			print(S)
			i+=1
		else:
			L=L*v
		if S<1e-8:
			print ('TolFun')
			return x
		if np.linalg.norm(dx)<1e-6:
			print ('TolX')
			return x
	print('maxiter')
	return x
	
			
## example. ##
# fit y=a*exp(-t*b)+noise		
def myfun(t,a):
	return a[0,0]*np.exp(-t*a[1,0])
	
t=np.matrix(np.linspace(0,1,25)).transpose()
x_truth=np.matrix([[7.6],
						 [5.1]])

x_guess=np.matrix([[1.],
						 [1.]])

y_meas=myfun(t,x_truth)+0.1*np.random.randn(*t.shape)
x=solve(lambda x:myfun(t,x), y_meas, x_guess, 100)
print('done:')
print(x)
