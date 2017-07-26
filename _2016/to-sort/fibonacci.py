cpdef int fib(int n):
    if n == 2:
        return 2
    elif n < 0:
        raise NotImplementedError
    elif n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    print(fib(40))
