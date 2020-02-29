from __future__ import print_function
#
#  merge(list1,list2): merges two sorted lists into one sorted list
#
#  Parameters:
#    list1, list2:  lists whose entries are in ascending order
#
#  Returns:
#    a sorted list containing the contents of list1 and list2
#
def merge(list1, list2):
  i = 0
  j = 0
  result = []

  while i < len(list1) and j < len(list2):
    if list1[i] < list2[j]:
      result.append(list1[i])
      i = i + 1
    else:
      result.append(list2[j])
      j = j + 1

  while i < len(list1):
    result.append(list1[i])
    i = i + 1

  while j < len(list2):
    result.append(list2[j])
    j = j + 1

  return result



#
# mergeSort(list): sorts the contents of list
#
# Parameters:
#   list:  list of unordered data
#
# Returns:
#   a sorted list containing the contents of list
#
#
def mergeSort(list):
  if len(list) <= 1:
    return list

  middle = len(list)/2
  left = mergeSort(list[:middle])
  right = mergeSort(list[middle:])
  result = merge(left,right)
  return result



L = [8,1,7,6,2,4,5,3]
print(L)
sorted = mergeSort(L)
print(sorted)
