from ..raspberry_pi_program_testowy.config import *
import RPi.GPIO as GPIO
import time
import neopixel
import board
import busio
import w1termsensor
import adafruit_bme280.advanced as adafruit_bme280

pixels = neopixel.NeoPiel(board.D18, 8, brightness=1.0/32, auto_write=False)


class Color:
    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    lime = (0,255,0)
    blue = (0,0,255)
    yellow = (255,255,0)
    cyan = (0,255,255)
    magenta = (255,0,255)
    silver = (192,192,192)
    grey = (128,128,128)
    maroon = (128,0,0)
    olive = (128,128,0)
    green = (0,128,0)
    purple = (128,0,128)
    teal = (0,128,128)
    navy = (0,0,128)
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
            return self.r, self.g, self.b

        @color.setter
        def color(self, color_tuple):
            if len(color_tuple) == 3:
                self.r, self.g, self.b = color_tuple
                self.brightness = 1
            else:
                self.r, self.g, self.b, self.brightness = color_tuple

    def __init__(self, brightness=1.0/32, auto_write=False):
        self.__pixels = neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write)
        self.__colors = [self.InnerColor.black() for _ in self.__pixels]
        
    def update_all(self):
        for inx in range(self.__pixels):
            self.__pixels[inx] = self.__colors[inx].color
        self.__pixels.show()

    def set_color(self, color_tuple: tuple, *inxs):
        for inx in inxs:
            self.__colors[inx].color = color_tuple
        self.update_all()

    def set_color_all(self, color_tuple: tuple):
        for color in self.__colors:
            color.color = color_tuple
        self.update_all()

    def rainbow(self):
        self.__colors[0].color = Color.red
        self.__colors[1].color = Color.orange
        self.__colors[2].color = Color.yellow
        self.__colors[3].color = Color.lime
        self.__colors[4].color = Color.green
        self.__colors[5].color = Color.cyan
        self.__colors[6].color = Color.blue
        self.__colors[7].color = Color.purple

    def display(self, val: float, start: float, end: float):
        max_one_led = (end - start) / 8
        full_leds = int((val - start) / max_one_led)
        brightness = (val - start - full_leds * max_one_led) / max_one_led
        self.__assign(full_leds, brightness)

    def __assign(self, full: int, brightness):
        for col in self.__colors:
            col.brightness = 0

        for i in range(full):
            self.__colors[i].brightness = 1
        self.__colors[full].brightness = brightness
        self.update_all()

    def __getitem__(self, item):
        return self.__pixels[item]


class OutsideWorldHandler:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        self.__init_env()
        self.__thermometer = w1termsensor.W1ThermSensor()

    def __init_env(self):
        self.__sensor.sea_level_preasure = 1013.25
        self.__sensor.standby_period = adafruit_bme280.STANDBY_TC_500
        self.__sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.__sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.__sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.__sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    @property
    def temperature(self):
        return self.__thermometer.get_temperature()

    @property
    def altitude(self):
        return self.__sensor.altitude

    @property
    def pressure(self):
        return self.__sensor.pressure

    @property
    def humidity(self):
        return self.__sensor.humidity


class ExerciseHandler:
    def __init__(self):
        self.led_controller = LedController()
        self.outside_word_handler = OutsideWorldHandler()
        self.temp_start = self.outside_word_handler.temperature
        self.temp_min = 10
        self.temp_max = 40
        self.altitude_min = 100
        self.altitude_max = 160
        self.pressure_min = 960
        self.pressure_max = 1050

        self.current_option = 0

        self.text_to_display = [f'Displaying temperature',
                                f'Displaying humidity',
                                f'Displaying altitude',
                                f'Displaying pressure'
                                ]

        self.options = [self.option_temperature,
                        self.humidity_act,
                        self.altitude_act,
                        self.pressure_act
                        ]

        self.encoder_options = [
            lambda x: self.encoder_temperature(x),
            lambda x: self.encoder_humidity(x),
            lambda x: self.encoder_altitude(x),
            lambda x: self.encoder_pressure(x)
        ]

        self.button_options = [
            self.button_temperature,
            self.button_humidity,
            self.button_altitude,
            self.button_pressure
        ]

    @property
    def get_current(self):
        return self.options[self.current_option]

    # temperature _______________________________________________________________________________________________
    def option_temperature(self):
        temp = self.outside_word_handler.temperature
        self.led_controller.rainbow()
        self.led_controller.display(temp, self.temp_min, self.temp_max)

    def encoder_temperature(self, is_right):
        if is_right:
            self.temp_max += 1
        else:
            self.temp_max -= 1
        print(f'Temperature range is: {self.temp_min} to {self.temp_max} ^C')

    def button_temperature(self):
        new_min_temp = input(f'Current min temp is {self.temp_min}. Set new one: ')
        self.temp_min = int(new_min_temp)

    # humidity ___________________________________________________________________________________________________
    def humidity_act(self):
        hum = self.outside_word_handler.humidity
        self.led_controller.set_color_all(Color.blue)
        self.led_controller.display(hum, 0, 100)

    def encoder_humidity(self, is_right):
        pass

    def button_humidity(self):
        pass

    # altitude ____________________________________________________________________________________________________
    def altitude_act(self):
        alt = self.outside_word_handler.altitude
        self.led_controller.set_color_all(Color.yellow)
        self.led_controller.display(alt, self.altitude_min, self.altitude_max)

    def encoder_altitude(self, is_right):
        pass

    def button_altitude(self):
        pass

    # pressure ___________________________________________________________________________________________________
    def pressure_act(self):
        press = self.outside_word_handler.pressure
        self.led_controller.set_color_all(Color.orange)
        self.led_controller.display(press, self.pressure_min, self.pressure_max)

    def encoder_pressure(self, is_right):
        pass

    def button_pressure(self):
        pass

    # menus _____________________________________________________________________________________________________
    def menu_forward(self):
        self.current_option = (self.current_option + 1) % len(self.options)
        print(self.text_to_display[self.current_option])

    def menu_backward(self):
        self.current_option = (self.current_option + len(self.options) - 1) % len(self.options)

    def leftPinCallback(self):
        if GPIO.input(encoderRight) == 0:
            self.encoder_options[self.current_option](False)

    def rightPinCallback(self):
        if GPIO.input(encoderLeft) == 0:
            self.encoder_options[self.current_option](True)

    def green_button_menu(self):
        self.button_options[self.current_option]()


exHand = ExerciseHandler()


def setup():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=exHand.menu_forward, bouncetime=200)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=exHand.green_button_menu, bouncetime=200)
    GPIO.add_event_detect(encoderLeft, GPIO.RISING, callback=exHand.leftPinCallback, bouncetime=200)
    GPIO.add_event_detect(encoderRight, GPIO.RISING, callback=exHand.rightPinCallback, bouncetime=200)


if __name__ == '__main__':
    setup()
    while True:
        exHand.get_current()
