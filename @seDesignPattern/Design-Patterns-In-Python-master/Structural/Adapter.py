#!/usr/bin/env python
# Written by: DGC

#==============================================================================
class RCCar(object):

    def __init__(self):
        self.speed = 0

    def change_speed(self, speed):
        self.speed = speed
        print("RC car is moving at " + str(self.speed))

#==============================================================================
class RCAdapter(object):

    def __init__(self):
        self.car = RCCar()

    def move_forwards(self):
        self.car.change_speed(10)

    def move_backwards(self):
        self.car.change_speed(-10)

    def stop(self):
        self.car.change_speed(0)

#==============================================================================
class RemoteControl(object):

    def __init__(self):
        self.adapter = RCAdapter()

    def stick_up(self):
        self.adapter.move_forwards()

    def stick_down(self):
        self.adapter.move_backwards()

    def stick_middle(self):
        self.adapter.stop()

#==============================================================================
if (__name__ == "__main__"):
    controller = RemoteControl()
    controller.stick_up()
    controller.stick_middle()
    controller.stick_down()
    controller.stick_middle()
    
