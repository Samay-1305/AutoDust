from time import sleep
import RPi.GPIO as GPIO
import os
import time

class Control:
    def __init__(self):
        self.pins = [3, 5] #Motor Interface Pins
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
            self.GPIO.setup(pin, GPIO.OUT)
        self.GPIO_TRIGGER = 8
        self.GPIO_ECHO = 10
        
        self.GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        self.GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        self.dist_threshhold = self.distance() - 2

    def rotate(self, val):
        try:
            pin = self.pins[int(val)]
            self.GPIO.output(pin, GPIO.HIGH)
            sleep(5)
            self.GPIO.output(pin, GPIO.LOW)
            sleep(0.5)
            self.dist_threshhold = self.distance() - 2
            return True
        except Exception as MotorError:
            print(MotorError)
            return False

    def listen_for_change(self):
        run = True
        while run:
            dist = self.distance()
            if dist < self.dist_threshhold:
                run = False
        return True

    def distance(self):
        self.GPIO.output(self.GPIO_TRIGGER, True)
    
        sleep(0.00001)
        self.GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        while self.GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
    
        while self.GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def release(self):
        self.GPIO.cleanup()
