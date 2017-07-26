# http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating

alist = ['good', 'bad', 'good', 'bad', 'good']
i = 0
for x in alist[:]:
	if x == 'bad':
		alist.pop(i)
		i -= 1
	else:
		# do something cool with x or just print x
		print(x)
	i += 1

