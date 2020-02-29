from __future__ import print_function
# https://gist.github.com/jefflovejapan/7796921

class BinaryHeap(list):
	def __init__(self):
		list.__init__(self)
		list.append(self, 0)
		
	def append(self, item):
		list.append(self, item)
		self.perc_up(len(self) - 1, item)
		
	def perc_up(self, index, item):
		if self[index // 2] > item:
			current_val = self[index // 2]
			self.perc_up(index // 2, item)
			self[index] = current_val
		else:
			self[index] = item
			
	def perc_down(self, index):
		comparisons = (2 * index, 2 * index + 1)
		if 2 * index + 1 < len(self):
			small_index = min(comparisons, key=lambda i: self[i])
			if self[small_index] < self[index]:
				self[small_index], self[index] = self[index], self[small_index]
				self.perc_down(small_index)
				
	def find_min(self):
		return self[1]
		
	def del_min(self):
		minval = self[1]
		self[1] = self[-1]
		self.pop()
		self.perc_down(1)
		return minval
		
		
def tests():
	heap = BinaryHeap()
	
	heap.append(13)
	heap.append(5)
	heap.append(17)
	heap.append(11)
	heap.append(8)
	
	def heaptest(aheap):
		for i in xrange(len(aheap)):
			if i > 1:
				assert aheap[i] >= aheap[i // 2]
				
	heap.del_min()
	heaptest(heap)
	print(heap)
	
if __name__ == '__main__':
	tests()

