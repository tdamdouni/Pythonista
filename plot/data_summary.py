# -*- coding: utf-8 -*-
# v1.0  2014-06-17

# https://gist.github.com/beer2011/e0aac99bfe48ad31ae3f

from __future__ import print_function
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math



# 簡易データ分析
def summary(np_arr):
	print('----- summary -----')
	print('標本= ', np_arr)
	print('標本数= ', len(np_arr))
	print('最小値= ', np.min(np_arr))
	print('最大値= ', np.max(np_arr))
	print('中央値= ', np.median(np_arr))
	print('平均= ', np.mean(np_arr))
	print('分散= ', np.var(np_arr))
	print('標準偏差= ', np.std(np_arr))
	print('不偏分散= ', fuhen_var(np_arr))
	print('標本標準誤差= ', hyoujyun_gosa(np_arr))
	
# 不偏分散
def fuhen_var(np_arr):
	mean = np.mean(np_arr)
	sum = 0
	for i in np_arr:
		sum = sum + math.pow(i-mean, 2)
	return sum / (len(np_arr)-1)
	
# 標本標準誤差
def hyoujyun_gosa(np_arr):
	mean = np.mean(np_arr)
	sum = 0
	for i in np_arr:
		sum = sum + math.pow(i-mean, 2)
	fuhen = sum / (len(np_arr)-1)
	return math.sqrt(fuhen / len(np_arr))
	
# 散布図表示
def plot():
	plt.plot(DATA, 'ro')
	plt.margins(0.2)
	plt.show()
	plt.close()
	
# ヒストグラム表示
def hist():
	plt.hist(DATA)
	plt.show()
	plt.close()

# カイ2乗分析
def chi_test(observed, expected):
	
	pass
	
# MAIN
def main():
	np_arr = np.array(DATA)
	summary(np_arr)
	# カイ２乗データ
	observed = np.array(OBSERVED)
	expected = np.array(EXPECTED)
	# 
	while True:
		print('s)ummary, p)lot, h)istgram, c)hi_test, q)uit = ?')
		inp = raw_input()
		if inp == 'q':
			print('***終了しました***')
			break
		elif inp == 's':
			summary(np_arr)
		elif inp == 'p':
			plot()
		elif inp == 'h':
			hist()
		elif inp == 'c':
			chi_test(observed, expected)



if __name__ == '__main__':
	# 対象データ
	DATA=[568,530,581,554,536,518,564,552]
	OBSERVED = [[435, 165], [265, 135]]
	EXPECTED = [[420, 180], [280, 120]]
	# 
	main()

