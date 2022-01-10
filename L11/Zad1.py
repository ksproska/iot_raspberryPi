import datetime
import random
import sqlite3
import time
import os
#from mfrc522 import MFRC522
from threading import Thread

import paho.mqtt.client as mqtt
import tkinter


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


class MFRC522:
    PICC_REQIDL = "pic_reqidl"
    MI_OK = 0
    MI_ERR = 1

    def __init__(self, successful=False):
        self.successful = successful

    def MFRC522_Request(self, arg):
        if self.successful:
            return self.MI_OK, "exampleTag"
        return self.MI_ERR, "exampleTag"

    def MFRC522_Anticoll(self):
        if self.successful:
            return self.MI_OK, f'{random.randint(1000, 10000)}'
        return self.MI_ERR, "exampleUid"


class RFIDHandler:
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.was_read = False

    def read(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                if not self.was_read:
                    self.was_read = True
                    return uid
                return None
        else:
            self.was_read = False
        return None


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
        #self.window.geometry("300x200")
