# https://gist.github.com/Subject22/6d340d7e2ef9a8f3ff1b49c48af57e7e

def dfs(graph, start):
    stack = [(None, start)]
    visited = {start}

    while len(stack) > 0:
        parent, current = stack.pop()
        yield parent, current
        new_children = graph[current] - visited
        stack += ((current, child) for child in new_children)
        visited |= new_children


def bfs(graph, start):
    queue = [(None, start)]
    visited = {start}

    while len(queue) > 0:
        parent, current = queue.pop(0)
        yield parent, current
        new_children = graph[current] - visited
        queue += ((current, child) for child in new_children)
        visited |= new_children


def shortest_path(graph, start, end):
    paths = {None: []}  # {destination: [path]}

    for parent, child in bfs(graph, start):
        paths[child] = paths[parent] + [child]

        if child == end:
            return paths[child]

    return None # or raise appropriate exception


graph = {'A': {'B', 'C','E'},
         'B': {'A','C', 'D'},
         'C': {'D'},
         'D': {'C'},
         'E': {'F', 'D'},
         'F': {'C'}}
