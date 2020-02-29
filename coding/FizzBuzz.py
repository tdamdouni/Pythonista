from __future__ import print_function
# https://gist.github.com/jefflovejapan/5076080

for i in range(100):
	if i % 15 == 0:
		print('FizzBuzz')
	elif i % 5 == 0:
		print('Buzz')
	elif i % 3 == 0:
		print('Fizz')
	else:
		print(i)

