from ..raspberry_pi_program_testowy.config import *
import RPi.GPIO as GPIO
import time


class MyDiode:
    CHANGE_VAL = 10

    def __init__(self, duty_cycle=0, frequency=50):
        self.current_duty_cycle = duty_cycle
        self.diode = GPIO.PWM(led1, frequency) # Hz

    def start(self):
        self.diode.start(self.current_duty_cycle) # dc

    def increase_led(self):
        self.current_duty_cycle = min(100, self.current_duty_cycle + MyDiode.CHANGE_VAL)
        self.diode.ChangeDutyCicle(self.current_duty_cycle)

    def decrease_led(self):
        self.current_duty_cycle = max(0, self.current_duty_cycle - MyDiode.CHANGE_VAL)
        self.diode.ChangeDutyCicle(self.current_duty_cycle)

    def stop(self):
        self.diode.stop()


my_diode = MyDiode()


def leftPinCallback(channel):
    if GPIO.input(encoderRight) == 0:
        # global my_diode
        my_diode.decrease_led()


def rightPinCallback(channel):
    if GPIO.input(encoderLeft) == 0:
        # global my_diode
        my_diode.increase_led()


def setup():
    my_diode.start()
    GPIO.add_event_detect(encoderLeft, GPIO.RISING, callback=leftPinCallback, bouncetime=200)
    GPIO.add_event_detect(encoderRight, GPIO.RISING, callback=rightPinCallback, bouncetime=200)


if __name__ == '__main__':
    setup()
    execute = True
    while execute:
        pass
