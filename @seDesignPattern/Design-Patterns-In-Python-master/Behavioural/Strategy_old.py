#!/usr/bin/env python
# Written by: DGC

import abc

#==============================================================================
class PrimeFinder(object):
    
    def __init__(self, algorithm):
        """ 
        Constructor, takes a lass called algorithm. 
        algorithm should have a function called calculate which will take a 
        limit argument and return an iterable of prime numbers below that 
        limit.
        """ 
        self.algorithm = algorithm
        self.primes = []

    def calculate(self, limit):
        """ Will calculate all the primes below limit. """
        self.primes = self.algorithm.calculate(limit)

    def out(self):
        """ Prints the list of primes prefixed with which algorithm made it """
        print(self.algorithm.name)
        for prime in self.primes:
            print(prime)
        print("")

#==============================================================================
class Algorithm(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate(self, limit):
        raise

#==============================================================================
class HardCoded(Algorithm):
    """ 
    Has hardcoded values for all the primes under 50, returns a list of those
    which are less than the given limit.
    """
    
    def __init__(self):
        self.name = "hard_coded_algorithm"

    def calculate(self, limit):
        hardcoded_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
        primes = []
        for prime in hardcoded_primes:
            if (prime < limit):
                primes.append(prime)
        return primes

#==============================================================================
class Standard(Algorithm):
    """ 
    Not a great algorithm either, but it's the normal one to use.
    It puts 2 in a list, then for all the odd numbers less than the limit if 
    none of the primes are a factor then add it to the list.
    """

    def __init__(self):
        self.name = "standard_algorithm"

    def calculate(self, limit):
        primes = [2]
        # check only odd numbers.
        for number in range(3, limit, 2):
            is_prime = True
            # divide it by all our known primes, could limit by sqrt(number)
            for prime in primes:
                if (number % prime == 0):
                    is_prime = False
                    break
            if (is_prime):
                primes.append(number)
        return primes

#==============================================================================
if (__name__ == "__main__"):
    hard_coded_algorithm = HardCoded()
    hardcoded_primes = PrimeFinder(hard_coded_algorithm)
    hardcoded_primes.calculate(50)
    hardcoded_primes.out()

    standard_algorithm = Standard()
    standard_primes = PrimeFinder(standard_algorithm)
    standard_primes.calculate(50)
    standard_primes.out()

    print(
        "Do the two algorithms get the same result on 50 primes? %s" 
        %(str(hardcoded_primes.primes == standard_primes.primes))
        )

    # the hardcoded algorithm only works on numbers under 50
    hardcoded_primes.calculate(100)
    standard_primes.calculate(100)

    print(
        "Do the two algorithms get the same result on 100 primes? %s" 
        %(str(hardcoded_primes.primes == standard_primes.primes))
        )
