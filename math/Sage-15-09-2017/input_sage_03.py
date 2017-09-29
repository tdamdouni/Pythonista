### SageMath - ODE System Solver:

import numpy as np
np.set_printoptions(threshold=np.inf)

# Parameters:
t_begin = 0
t_end = 10
step = 0.1
h , g = var(' h , g ')
t = var(' t ')

# ODEs and ICs:
  # 'dhdt=g-t-2' et
  # 'dgdt=h+g+t' with
  # 'h(t=0)=1' et
  # 'g(t=0)=3'
functions = [ h , g ]
indep_var = t
system = [ g , -h ]
init_conds = [ 1 , 1 ]

# Solver:
time_interval = srange(t_begin, t_end+step, step)
solution = desolve_odeint(system, init_conds, time_interval, functions, indep_var)

# Output matrix:
number_of_steps = Integer((t_end-t_begin)/step)+1
time_interval_Matrix = np.reshape(time_interval, (1, number_of_steps))
solution_t_functions = np.concatenate((time_interval_Matrix.T, solution), axis=1)
print(solution_t_functions)