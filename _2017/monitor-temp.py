# https://gist.github.com/kevalpatel2106/ac79e08e6362e246e757895d0e9aa1f6

# pi@raspberrypi:~ $ /opt/vc/bin/vcgencmd measure_temp
# temp=56.9'C

import os
import time

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

while True:
        print(measure_temp())
        time.sleep(1)
