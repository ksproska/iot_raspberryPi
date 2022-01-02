import sqlite3
import time
import os
#from mfrc522 import MFRC522
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

    class MIFAREReader:
        PICC_REQIDL = "pic_reqidl"

        def __init__(self):
            pass

    MI_OK = 0
    MI_ERR = 1

    def __init__(self, successful=False):
        self.successful = successful

    def MFRC552_Request(self, arg: MIFAREReader):
        return self.MI_OK if self.successful else self.MI_ERR, "tagType"

    def MFMFRC522_Anticoll(self):
        return self.MI_OK if self.successful else self.MI_ERR, "uid"


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
        self.window = tkinter.Tk()

    def connect_to_broker(self):
        self.client.connect(self.broker)

    def disconnect_from_broker(self):
        self.client.disconnect(self.broker)

    def run(self):
        #self.connect_to_broker()
        self.window.geometry("300x200")


class Sender(Messenger):
    def __init__(self):
        Messenger.__init__(self)

    def publish(self, card_id, log_time):
        self.client.publish('Card used', card_id + '#' + log_time)

    def run(self):
        super().run()
        self.client.connect(self.broker)
        self.window.title("SENDER")
        button_attach = tkinter.Button(self.window, text="ATTACH CARD")
        button_attach.grid(row=0, column=0)
        self.window.mainloop()
        self.disconnect_from_broker()


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


if __name__ == '__main__':
    sender = Sender()
    sender.run()
