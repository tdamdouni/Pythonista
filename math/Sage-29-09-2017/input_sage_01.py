## Import numpy and matplotlib.pyplot:
import numpy as np
np.set_printoptions(threshold=np.inf)   ## for full output (avoid truncated arrays like: '[1, 2, 3 ... 100, 101, 102]')

import matplotlib.pyplot as plt

import time


## Some examples:

""" 
scipy interpolate:
See how to import scipy modules in Python: https://docs.scipy.org/doc/scipy/reference/api.html
See all scipy modules here: https://docs.scipy.org/doc/scipy/reference/py-modindex.html
"""
## Import here the scipy modules you need in the following way, as a reminder for me:
#from scipy.fftpack import fft   ## to import only the function 'fft' of the module 'scipy.fftpack'
## or
#from scipy.fftpack import *   ## to import all functions of the module 'scipy.fftpack'

from scipy.interpolate import interp1d
x = np.arange(0, 10)
y = np.exp(-x/3.0)
f = interp1d(x, y)
xnew = np.arange(0, 9, 0.1)
ynew = f(xnew)

time.sleep(1)
print(xnew)

time.sleep(1)
print(ynew)


#plt.plot(x, y, 'o', xnew, ynew, '-')
#plt.show()


""" 
scipy fftpack:
See how to import scipy modules in Python: https://docs.scipy.org/doc/scipy/reference/api.html
See all scipy modules here: https://docs.scipy.org/doc/scipy/reference/py-modindex.html
"""
## Import here the scipy modules you need in the following way, as a reminder for me:
#from scipy.fftpack import fft   ## to import only the function 'fft' of the module 'scipy.fftpack'
## or
#from scipy.fftpack import *   ## to import all functions of the module 'scipy.fftpack'

from scipy.fftpack import fft
x = np.array([1.0, 2.0, 1.0, -1.0, 1.5])
y = fft(x)

time.sleep(1)
print(y)


"""
pandas Series:
"""
import pandas as pd
s = pd.Series([1,3,5,np.nan,6,8])

time.sleep(1)
print(s)


""" 
sympy solve:
"""
import sympy as sy   ## see: http://docs.sympy.org/latest/py-modindex.html
y = sy.Symbol('y')
sol = sy.solve(y**2-3*y+5, y)

time.sleep(1)
print(sol)

time.sleep(1)
sy.pprint(sol, use_unicode=False)



"""
mpmath ODE System solver:
"""
from mpmath import *
mp.pretty = True

mp.dps = 25
tolerance = 0.001
taylor_degree = 4
solver_method = 'taylor'

t_begin = 0
t_end = 5
step = 0.5

system = lambda t, y: [ y[1]-t-2 , y[0]+y[1]+t ]
init_conds = [ 1 , 3 ]
solution = mp.odefun(system, t_begin, init_conds, tol=tolerance, degree=taylor_degree, method=solver_method, verbose=False)
time_interval = np.arange(t_begin, t_end+step, step)
number_of_steps = int((t_end-t_begin)/step+1)
time_interval_Matrix = np.reshape(time_interval, (1, number_of_steps))
solution_Matrix = []

for t in time_interval:
    solution_Matrix.append(solution(t))

solution_t_functions = np.concatenate((time_interval_Matrix.T, solution_Matrix), axis=1)

time.sleep(1)
print(solution_t_functions)





"""
scipy ODE System solver:
"""
# Parameters:
t_begin = 0
t_end = 5
step = 0.5
h , g = var(' h , g ')
t = var(' t ')

# ODEs and ICs:
  # 'dhdt=g-t-2' et
  # 'dgdt=h+g+t' with
  # 'h(t=0)=1' et
  # 'g(t=0)=3'
functions = [ h , g ]
indep_var = t
system = [ g-t-2 , h+g+t ]
init_conds = [ 1 , 3 ]

# Solver:
time_interval = srange(t_begin, t_end+step, step)
solution = desolve_odeint(system, init_conds, time_interval, functions, indep_var)

# Output matrix:
number_of_steps = Integer((t_end-t_begin)/step)+1
time_interval_Matrix = np.reshape(time_interval, (1, number_of_steps))
solution_t_functions = np.concatenate((time_interval_Matrix.T, solution), axis=1)

time.sleep(1)
print(solution_t_functions)






"""
octave and maxima:
"""
var1=octave.eval("1-2")
var2=maxima.eval("x+x")

time.sleep(1)
print(var1)

time.sleep(1)
print(var2)




"""
test to pass Pythonista some variables for SageMathCell:
"""
time.sleep(1)
print(1)

time.sleep(1)
print(2)

time.sleep(1)
print(30)


