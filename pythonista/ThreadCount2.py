# coding: utf-8

# https://forum.omz-software.com/topic/2744/pythonista-hung-can-t-stop-program-stop-x-button-was-disabled/7

from __future__ import print_function
import threading
import time
import Queue
import random
import collections
import console


class WorkerCounterThread(threading.Thread):

	def __init__(self, stopnum, outputQueue, delay_val):
		threading.Thread.__init__(self)
		print("\nThread delay = %1.2f\n" % delay_val)
		self.count = 1
		self.finished = False
		self.stopnum = stopnum
		self.output = outputQueue
		self.delay_val = delay_val
		
	def run(self):
	
		while not self.finished:
		
			self.output.put(self.count)
			
			if self.count == self.stopnum:
				#print"Stop count is %d" % self.count
				self.stop()
			else:
				self.count += 1
				time.sleep(self.delay_val)
				
	def stop(self):
		self.finished = True
		
#################################################

def main():

	console.clear()
	
	results = Queue.Queue()
	thread_delay = random.choice([.2, .4, .1, .19, .26, .3])
	wc_thread = WorkerCounterThread(20, results, thread_delay)
	wc_thread.start()
	
	loops = 0
	accum =[]
	accum_loops = 0
	count_stats = collections.Counter()
	
	while 1:
	
		while not results.empty():
			accum.append(results.get())
			
		if accum:
			accum_len = len(accum)
			for count in accum:
				print("Count=%2d, len(accum) = %d" % (count, accum_len))
				count_stats[accum_len] += 1
				
			accum_loops += 1
			accum = []
			
		if not wc_thread.isAlive():
			break
			
		time.sleep(random.random())
		loops += 1
		
	print("\nDONE: mainloops= {:,},accum_loops=%d\n".format(loops) % accum_loops)
	
	for val, count in count_stats.iteritems():
		print("Val = %2d, count = %2d" %(val, count))
		
		
if __name__ == '__main__':
	main()

