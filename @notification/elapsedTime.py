import math, time

def elapsedTime(start_time):
    dt = time.time() - start_time
    minutes = dt / 60
    seconds = dt % 60
    centiseconds = math.modf(dt)[0] * 100
    return '%02d:%02d.%02d' % (minutes, seconds, centiseconds)
    #return '{:0>2}:{:0>2}.{:0>2}'.format(minutes, seconds, centiseconds)

start_time = time.time()
time.sleep(1)
print(elapsedTime(start_time))
