import sqlite3
import time
import os
from mfrc522 import MFRC522
import neopixel
import board
import paho.mqtt.client as mqtt


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    LIME = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    SILVER = (192, 192, 192)
    GREY = (128, 128, 128)
    MAROON = (128, 0, 0)
    OLIVE = (128, 128, 0)
    GREEN = (0, 128, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)
    NAVY = (0, 0, 128)
    ORANGE = (255, 128, 0)


class LedController:
    class InnerColor:
        def __init__(self, r, g, b, brightness):
            self.r = r
            self.g = g
            self.b = b
            self.brightness = brightness

        @classmethod
        def black(cls):
            return cls(*Color.BLACK, 1)

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

    def clear(self):
        self.set_color_all(Color.BLACK)
        self.update_all()

    def set_rainbow(self):
        self.__colors[0].color = Color.RED
        self.__colors[1].color = Color.ORANGE
        self.__colors[2].color = Color.YELLOW
        self.__colors[3].color = Color.LIME
        self.__colors[4].color = Color.GREEN
        self.__colors[5].color = Color.CYAN
        self.__colors[6].color = Color.BLUE
        self.__colors[7].color = Color.PURPLE

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
                pass


class Messenger:
    def __init__(self):
        self.broker = 'localhost'
        self.client = mqtt.Client()

    def connect_to_broker(self):
        self.client.connect(self.broker)

    def disconnect_from_broker(self):
        self.client.disconnect(self.broker)

    def run(self):
        self.connect_to_broker()
        while True:
            pass


class Sender(Messenger):
    def __init__(self):
        Messenger.__init__(self)

    def publish(self, card_id, log_time):
        self.client.publish('Card used', card_id + '#' + log_time)


class Receiver(Messenger):
    def __init__(self):
        Messenger.__init__(self)

    def connect_to_broker(self):
        super().connect_to_broker()
        self.client.on_message = self.process_message

    @staticmethod
    def process_message(client, userdata, message):
        card_id, log_time = str(message.payload.decode('utf-8')).split('#')
        print(f'Card: {card_id}\nTime: {log_time}\n')


class ExerciseHandler:
    pass


