import timeit
result = timeit.timeit("pyscrypt.hash(password= b'foobar', salt= b'seasalt', N=1024, r=1, p=1, dkLen=32)", setup="import pyscrypt", number=100)
print(result)

