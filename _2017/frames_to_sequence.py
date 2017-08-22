# https://gist.github.com/harvitronix/696dce24778c60dfa526c22b4c985541

temp_list = deque()
with open(filename, 'rb') as fin:
    frames = pickle.load(fin)

for frame in frames:
    features = frame[0]
    actual = frame[1]

    # Add to the queue.
    if len(temp_list) == num_frames - 1:
        temp_list.append(features)
        X.append(np.array(list(temp_list)))
        y.append(actual)
        temp_list.popleft()
    else:
        temp_list.append(features)
        continue
