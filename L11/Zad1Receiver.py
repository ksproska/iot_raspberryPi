import datetime
from threading import Thread
import tkinter
import paho.mqtt.client as paho
from Zad1 import *


class Receiver(Messenger):
    def __init__(self):
        Messenger.__init__(self)

    def connect_to_broker(self):
        super().connect_to_broker()
        self.client.on_message = self.process_message
        self.client.loop_start()
        self.client.subscribe("id/card")

    @staticmethod
    def process_message(client, userdata, message):
        card_id, log_time = str(message.payload.decode('utf-8')).split('#')
        print(f'Card: {card_id}\nTime: {log_time}\n')


if __name__ == '__main__':
    rec = Receiver()
    rec.connect_to_broker()

    inp = ""
    while inp != "exit":
        inp = input()
