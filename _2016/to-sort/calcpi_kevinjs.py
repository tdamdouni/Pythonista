#!/usr/bin/env python

# https://github.com/kevinjs/algoprep/blob/master/python/calc/calcpi.py

from __future__ import print_function
from math import hypot
from random import random
from functools import wraps
import eventlet
import gevent
import time
from multiprocessing.dummy import Pool as t_Pool
from multiprocessing import Pool as p_Pool

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        result = func(*args, **kwargs)
        ed = time.time()
        print('%s cost: %s sec' %(func.__name__ ,ed-st))
        return result
    return wrapper

def test(tries):
    return sum(hypot(random(), random()) < 1 for _ in range(tries))

@timeit
def run_single(tries, nbF):
    rslt = map(test, [tries] * nbF)
    ret = 4. * sum(rslt) / float(nbF * tries)
    return ret

@timeit
def run_multi_thread(tries, nbF, pool_size):
    p = t_Pool(pool_size)
    rslt = p.map(test, [tries] * nbF)
    ret = 4. * sum(rslt) / float(nbF * tries)
    return ret

@timeit
def run_multi_processing(tries, nbF, poll_size):
    p = p_Pool(poll_size)
    rslt = p.map(test, [tries] * nbF)
    ret = 4. * sum(rslt) / float(nbF * tries)
    return ret

@timeit
def run_gevent(tries, nbF):
    pass

@timeit
def run_eventlet(tries, nbF):
    pass

if __name__=='__main__':
    print(run_single(4000, 3000))
    #print 'run multi thread, 1'
    #print run_multi_thread(4000, 3000, 1)
    #print 'run multi thread, 2'
    #print run_multi_thread(4000, 3000, 2)
    print('run multi processing, 1')
    print(run_multi_processing(4000, 3000, 1))
    print('run multi processing, 4')
    print(run_multi_processing(4000, 3000, 4))

