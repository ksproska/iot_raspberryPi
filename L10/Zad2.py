import datetime

from ..raspberry_pi_program_testowy.config import *
import RPi.GPIO as GPIO
import time
from datetime import datetime
import neopixel
import board
import busio
import w1thermsensor
import adafruit_bme280.advanced as adafruit_bme280
from mfrc522 import MFRC522


class PrettyDate:
    def __init__(self):
        pass

    @staticmethod
    def to_str(ms):
        return f'{ms.hour}:{ms.minute}:{ms.second},{ms.microsecond}'


class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    lime = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    silver = (192, 192, 192)
    grey = (128, 128, 128)
    maroon = (128, 0, 0)
    olive = (128, 128, 0)
    green = (0, 128, 0)
    purple = (128, 0, 128)
    teal = (0, 128, 128)
    navy = (0, 0, 128)
    orange = (255, 128, 0)



class LedController:
    class InnerColor:
        def __init__(self, r, g, b, brightness):
            self.r = r
            self.g = g
            self.b = b
            self.brightness = brightness

        @classmethod
        def black(cls):
            return cls(*Color.black, 1)

        @property
        def color(self):
            return int(self.r * self.brightness), int(self.g * self.brightness), int(self.b * self.brightness)

        @color.setter
        def color(self, color_tuple):
            self.r, self.g, self.b = color_tuple

    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.__pixels = neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write)
        self.__colors = [self.InnerColor.black() for _ in range(8)]
        self.update_all()

    def update_all(self):
        for inx in range(len(self.__colors)):
            self.__pixels[inx] = self.__colors[inx].color
        self.__pixels.show()

    def set_color_all(self, color_tuple):
        for color in self.__colors:
            color.color = color_tuple
        self.update_all()

    # to jest jako eksperyment. Wiem że to brzydkie kodowanie
    def slow_load(self):
        self.set_rainbow()
        divider = 100
        index = 0
        prev_index = 0
        self.__pixels[index] = self.__colors[index].color
        for i in range(divider * 8 + 2):
            index = int(i / divider)
            if index != prev_index:
                prev_index = index
                self.__pixels[index] = self.__colors[index].color

    def clear(self):
        self.set_color_all(Color.black)
        self.update_all()

    def set_rainbow(self):
        self.__colors[0].color = Color.red
        self.__colors[1].color = Color.orange
        self.__colors[2].color = Color.yellow
        self.__colors[3].color = Color.lime
        self.__colors[4].color = Color.green
        self.__colors[5].color = Color.cyan
        self.__colors[6].color = Color.blue
        self.__colors[7].color = Color.purple

    def rainbow(self):
        self.set_rainbow()
        self.update_all()


class RFIDHandler:
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.start_time = None
        self.is_being_sensed = False

    def read(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                new_time = datetime.datetime.now()
                if not self.is_being_sensed:
                    self.is_being_sensed = True
                    self.start_time = new_time
                    return True
            else:
                self.is_being_sensed = False
        else:
            self.is_being_sensed = False
        return False

    def __str__(self):
        print(f'Is card sensed: {self.is_being_sensed}; Last card read time: {PrettyDate.to_str(self.start_time)}')


class ExerciseHandler:
    def __init__(self):
        self.rfidh = RFIDHandler()
        self.oled = LedController()
        self.signal_time_period = 1

    def buzzer(self, state):
        GPIO.output(buzzerPin, not state)

    def run(self):
        was_read_successful = self.rfidh.read()
        if was_read_successful:
            print(self.rfidh)
            self.buzzer(True)
            self.oled.rainbow()

        if self.rfidh.start_time + self.signal_time_period < datetime.datetime.now():
            self.buzzer(False)

        if not self.rfidh.is_being_sensed:
            self.oled.set_color_all(Color.black)


if __name__ == '__main__':
    exh = ExerciseHandler()
    while True:
        exh.run()
