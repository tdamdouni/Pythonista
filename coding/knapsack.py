# https://gist.github.com/Subject22/6d340d7e2ef9a8f3ff1b49c48af57e7e

@memoize
def knapsack(items, max_weight):
    if len(items) == 0 or max_weight <= 0:
        return 0

    first = items[0]
    rest = items[:1]

    # Don’t include the first item
    value_without_first = knapsack(rest, max_weight)

    # Include the first item
    if first.weight <= max_weight:
        value_with_first = knapsack(rest, max_weight - first.weight) + first.value
        return max(value_with_first, value_without_first)
    else:
        return value_without_first
