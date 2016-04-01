import sys

def quick_sort(list):
   if list == []: return []
   return quick_sort([x for x in list[1:] if x <  list[0]]) + \
          list[0:1] + \
          quick_sort([x for x in list[1:] if x >= list[0]])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        list = []
        with open(sys.argv[1], 'r') as f:
            for line in f:
                list.append(int(line))
        sorted_list = quick_sort(list)
        print(sorted_list)
    else:
        print("Usage: %s [list file]" % sys.argv[0])
