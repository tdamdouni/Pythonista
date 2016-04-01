from contextlib import contextmanager
from time import time
from sys import stdout

@contextmanager
def duration(outfile=stdout):
    start = time()
    yield
    end = time()
    outfile.write(str(end - start) + '\n')
