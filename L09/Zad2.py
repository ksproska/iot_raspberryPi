from ..raspberry_pi_program_testowy.config import *
import RPi.GPIO as GPIO
import time
import neopixel
import board
import busio
import w1termsensor
import adafruit_bme280.advanced as adafruit_bme280

# pixels = neopixel.NeoPiel(board.D18, 8, brightness=1.0 / 32, auto_write=False)


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
            return self.r, self.g, self.b, self.brightness

        @color.setter
        def color(self, color_tuple: tuple[int, int, int]):
            self.r, self.g, self.b = color_tuple

    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.__pixels = neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write)
        self.__colors = [self.InnerColor.black() for _ in self.__pixels]
        self.update_all()

    def update_all(self):
        for inx in range(self.__pixels):
            self.__pixels[inx] = self.__colors[inx].color
        self.__pixels.show()

    def set_color_all(self, color_tuple: tuple[int, int, int]):
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
        self.update_all()

    def display(self, val: float, start: float, end: float):
        max_one_led = (end - start) / 8
        full_leds = int((val - start) / max_one_led)
        brightness = (val - start - full_leds * max_one_led) / max_one_led
        self.__assign_brightness(full_leds, brightness)

    def __assign_brightness(self, number_of_full: int, value_of_not_full_brightness: float):
        for col in self.__colors:
            col.brightness = 0

        for i in range(number_of_full):
            self.__colors[i].brightness = 1
        self.__colors[number_of_full].brightness = value_of_not_full_brightness
        self.update_all()


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
        self.current_option = 0

        self.handlers: list[ExerciseHandler.OptionHandler] = \
            [
                self.TemperatureHandler(self.led_controller, self.outside_word_handler),
                self.HumidityHandler(self.led_controller, self.outside_word_handler),
                self.AltitudeHandler(self.led_controller, self.outside_word_handler),
                self.PressureHandler(self.led_controller, self.outside_word_handler)
            ]

    @property
    def current_handler(self):
        return self.handlers[self.current_option]

    @property
    def current_activity(self):
        return self.current_handler.activity

    @property
    def current_encoder(self):
        return lambda x: self.current_handler.encoder(x)

    @property
    def current_button(self):
        return self.current_handler.button

    class OptionHandler:
        def __init__(self, led_controller, outside_word_handler):
            self.led_controller = led_controller
            self.outside_word_handler = outside_word_handler

        def __str__(self):
            return f'Current running: {self.__class__.__name__}'

        def activity(self):
            pass

        def encoder(self, is_right: bool):
            print(f'Encoder from: {self.__class__.__name__}')
            pass

        def button(self):
            print(f'Button from: {self.__class__.__name__}')
            pass

    class TemperatureHandler(OptionHandler):
        def __init__(self, led_controller, outside_word_handler):
            super().__init__(led_controller, outside_word_handler)
            self.temp_start = self.outside_word_handler.temperature
            self.temp_min = 10
            self.temp_max = 40

        def activity(self):
            super().activity()
            temp = self.outside_word_handler.temperature
            print(f'Current temperature: {temp}')
            self.led_controller.rainbow()
            self.led_controller.display(temp, self.temp_min, self.temp_max)

        def encoder(self, is_right: bool):
            super().encoder(is_right)
            if is_right:
                self.temp_max += 1
            else:
                self.temp_max -= 1
            print(f'Temperature range is: {self.temp_min} to {self.temp_max} °C')

        def button(self):
            super().button()
            new_min_temp = input(f'Current min temp is {self.temp_min}. Set new one: ')
            self.temp_min = int(new_min_temp)

    class HumidityHandler(OptionHandler):
        def __init__(self, led_controller, outside_word_handler):
            super().__init__(led_controller, outside_word_handler)

        def activity(self):
            super().activity()
            hum = self.outside_word_handler.humidity
            print(f'Current humidity: {hum}')
            self.led_controller.set_color_all(Color.blue)
            self.led_controller.display(hum, 0, 100)

    class AltitudeHandler(OptionHandler):
        def __init__(self, led_controller, outside_word_handler):
            super().__init__(led_controller, outside_word_handler)
            self.altitude_min = 100
            self.altitude_max = 160

        def activity(self):
            super().activity()
            alt = self.outside_word_handler.altitude
            print(f'Current altitude: {alt}')
            self.led_controller.set_color_all(Color.yellow)
            self.led_controller.display(alt, self.altitude_min, self.altitude_max)

    class PressureHandler(OptionHandler):
        def __init__(self, led_controller, outside_word_handler):
            super().__init__(led_controller, outside_word_handler)
            self.pressure_min = 960
            self.pressure_max = 1050

        def activity(self):
            super().activity()
            press = self.outside_word_handler.pressure
            print(f'Current pressure: {press}')
            self.led_controller.set_color_all(Color.orange)
            self.led_controller.display(press, self.pressure_min, self.pressure_max)

    # menus _____________________________________________________________________________________________________
    def set_next(self):
        self.current_option = (self.current_option + 1) % len(self.handlers)
        print(self.current_handler)

    def set_prev(self):
        self.current_option = (self.current_option + len(self.handlers) - 1) % len(self.handlers)

    def encoder_left_callback(self):
        if GPIO.input(encoderRight) == 0:
            self.current_encoder(False)

    def encoder_right_callback(self):
        if GPIO.input(encoderLeft) == 0:
            self.current_encoder(True)

    def green_button_callback(self):
        self.current_button()


exHand = ExerciseHandler()


def setup():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=exHand.set_next, bouncetime=200)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=exHand.green_button_callback, bouncetime=200)
    GPIO.add_event_detect(encoderLeft, GPIO.RISING, callback=exHand.encoder_left_callback, bouncetime=200)
    GPIO.add_event_detect(encoderRight, GPIO.RISING, callback=exHand.encoder_right_callback, bouncetime=200)


if __name__ == '__main__':
    setup()
    while True:
        exHand.current_activity()
