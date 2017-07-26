# https://github.com/willtownes/python/blob/master/calcpi.py

'''calculates pi to arbitary level of precision'''
import math

def yieldpi():
    '''generates a sequence of increasingly accurate approximations to pi'''
    apx = 4
    i = 1
    neg = False
    while True:
        i+=2
        neg = not neg
        apx += (4.0/i)*(-1)**neg
        yield apx


def calcpi(digits=5):
    '''returns an approximation to pi with specified accuracy'''
    precision = 10**(-digits)
    a = yieldpi()
    b0 = next(a)
    while True:
        b1 = next(a)
        #print(b1)
        if abs(b1-b0) < precision:
            return b1
        else:
            b0 = b1

if __name__ == "__main__":
    print("Approximation of pi to 5 decimal places:")
    ans = calcpi(5)
    print("True pi is: %f"%math.pi)
    print("Our approximation is %f, with an error of %e"%(ans,ans-math.pi))   
            
