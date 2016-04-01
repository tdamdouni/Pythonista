def qicksort(test, left, right):
    i = left
    j = right
    key = test[right]

    if i >= j:
    return
    while i < j:
    while test[i] < key and i < j:
        i += 1
    if i < j:
        test[j] = test[i]
        j -= 1
    while test[j] > key and i < j:
        j -= 1
    if i < j:
        test[i] = test[j]
        i += 1
    test[i] = key
    qicksort(test, left, i-1)
    qicksort(test, i+1, right)

if __name__ == '__main__':
    test = [3, 8, 4, 1, 6, 7, 0, 9]
    qicksort(test, 0, 7)
    print(test)
