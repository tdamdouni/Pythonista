#!/usr/bin/env python
# Written by: DGC
# An example of how the client interacts with a complex series of objects 
# (car engine, battery and starter motor) through a facade (the car)

#==============================================================================
class Engine(object):
    
    def __init__(self):
        # how much the motor is spinning in revs per minute
        self.spin = 0

    def start(self, spin):
        if (spin > 2000):
            self.spin = spin // 15

#==============================================================================
class StarterMotor(object):
    
    def __init__(self):
        # how much the starter motor is spinning in revs per minute
        self.spin = 0

    def start(self, charge):
        # if there is enough power then spin fast
        if (charge > 50):
            self.spin = 2500

#==============================================================================
class Battery(object):

    def __init__(self):
        # % charged, starts flat
        self.charge = 0

#==============================================================================
class Car(object):
    # the facade object that deals with the battery, engine and starter motor.
    
    def __init__(self):
        self.battery = Battery()
        self.starter = StarterMotor()
        self.engine = Engine()
        
    def turn_key(self):
        # use the battery to turn the starter motor
        self.starter.start(self.battery.charge)

        # use the starter motor to spin the engine
        self.engine.start(self.starter.spin)
        
        # if the engine is spinning the car is started
        if (self.engine.spin > 0):
            print("Engine Started.")
        else:
            print("Engine Not Started.")

    def jump(self):
        self.battery.charge = 100
        print("Jumped")

#==============================================================================
if (__name__ == "__main__"):
    corsa = Car()
    corsa.turn_key()
    corsa.jump()
    corsa.turn_key()

