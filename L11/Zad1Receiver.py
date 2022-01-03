from threading import Thread
import tkinter
import paho.mqtt.client as paho
from L11.Zad1 import Receiver


if __name__ == '__main__':
    # rec = Receiver()
    # rec.connect_to_broker()
    #w = tkinter.Tk()
    #w.mainloop()

    client = paho.Client()
    broker = 'localhost'

    def on_message(cl, userdata, message):
        print('It works!')

    client.on_message = on_message
    client.connect(broker, port=1883)
    client.loop_forever()


