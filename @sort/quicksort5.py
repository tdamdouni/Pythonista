def quicksort2(test, left, right):
    i = left
    j = right
    if i >= j:
    return
    while i < j:
    while test[i] < test[j]:
        j -= 1
    if i < j:
        temp = test[i]
        test[i] = test[j]
        test[j] = temp

    while test[i] < test[j]:
        i += 1
    if i < j:
        temp = test[i]
        test[i] = test[j]
        test[j] = temp
    if i == left:
    quicksort2(test, i+1, right)
    elif j == right:
    quicksort2(test, left, j-1)
    else:
    quicksort2(test, left, i-1)
    quicksort2(test, i+1, right)

if __name__ == '__main__':
    test = [9, 2, 4, 7, 8, 0, 1, 3]
    quicksort2(test, 0, 7)
    print(test)
