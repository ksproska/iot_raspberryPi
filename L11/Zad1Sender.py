from Zad1 import *

class Sender(Messenger):
    class Window:
        def __init__(self, mfrc: MFRC522):
            self.mfrc = mfrc
            window = tkinter.Tk()
            window.title("SENDER")

            def set_success(succ=True):
                print(succ)
                mfrc.successful = succ

            button_attach = tkinter.Button(window, text="ATTACH CARD"
                                           # , command=lambda event=None: self.card_reader.successful
                                           )
            button_attach.bind('<ButtonPress-1>', lambda event=None, succ=True: set_success(succ))
            button_attach.bind('<ButtonRelease-1>', lambda event=None, succ=False: set_success(succ))
            button_attach.grid(row=0, column=0)
            window.mainloop()

    def __init__(self, card_handler):
        self.card_handler = card_handler
        Messenger.__init__(self)

    def publish(self, card_id, log_time):
        self.client.publish('id/card', card_id + '#' + log_time)

    def run(self):
        super().run()
        self.connect_to_broker()
        # https://stackoverflow.com/questions/51347381/connection-refused-error-in-paho-mqtt-python-package


if __name__ == '__main__':
    card_handler = RFIDHandler()
    sender = Sender(card_handler)
    Thread(target=lambda: Sender.Window(card_handler.MIFAREReader)).start()

    sender.run()
    while True:
        log_time = datetime.datetime.now()
        read = card_handler.read()
        print(f'{datetime.datetime.now()} - {read}')
        if read is not None:
            print('imagine light and sound...')
            sender.publish(read, f'{log_time.hour}:{log_time.minute}:{log_time.second},{log_time.microsecond}')

        time.sleep(0.1)

