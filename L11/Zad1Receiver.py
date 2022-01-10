import datetime
from threading import Thread
import tkinter
import paho.mqtt.client as paho
from L11.Zad1 import Receiver

global counter
if __name__ == '__main__':
    rec = Receiver()
    rec.connect_to_broker()

    inp = ""
    while inp != "exit":
        inp = input()
