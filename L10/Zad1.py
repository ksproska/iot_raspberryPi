from ..raspberry_pi_program_testowy.config import *
import RPi.GPIO as GPIO
import time
import board
import busio
import w1thermsensor
import adafruit_bme280.advanced as adafruit_bme280
import lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont


class Font:
    ARIAL = ImageFont.truetype("fonts/arial.ttf")
    TIMES = ImageFont.truetype("fonts/times.ttf")
    MATORAN = ImageFont.truetype("fonts/Matoran.ttf")


class OledHandler:
    # modes
    RGB = "RGB"
    RGBA = "RGBA"
    CMYK = "CMYK"

    # DO NOT DELETE or else I'll have to check this color all over again and I'm lazy...
    __GRAY = (40, 40, 40)

    def __init__(self, background_color, background_file):
        self.__display = SSD1331.SSD1331()
        self.__display.Init()
        self.__display.clear()
        self.__background = Image.open(background_file)
        self.__printer = ImageDraw.Draw(self.__background)
        self.__background_color = background_color

    def show(self):
        self.__display.ShowImage(self.__background)

    def clear(self):
        self.__display.clear()

    def reset(self):
        self.__display.reset()

    @property
    def width(self):
        return self.__display.width

    @property
    def height(self):
        return self.__display.height

    # PRINTS --------------------------------------------------------
    def base_print(self, xy, text, color=None, font=Font.ARIAL):
        self.__printer.text(xy, text, fill=color, font=font)

    # CLEAR ---------------------------------------------------------
    def base_clear(self, xy):
        self.__printer.rectangle(xy, fill=self.__background_color)


class OutsideWorldHandler:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        self.__init_env()
        self.__thermometer = w1thermsensor.W1ThermSensor()

    def __init_env(self):
        self.__sensor.sea_level_preasure = 1013.25
        self.__sensor.standby_period = adafruit_bme280.STANDBY_TC_500
        self.__sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.__sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.__sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.__sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    def temperature(self):
        return self.__thermometer.get_temperature()

    def altitude(self):
        return self.__sensor.altitude

    def pressure(self):
        return self.__sensor.pressure

    def humidity(self):
        return self.__sensor.humidity


class ExerciseHandler:
    TEMPERATURE_DELTA = 0.1
    HUMIDITY_DELTA = 0.1
    ALTITUDE_DELTA = 0.1
    PRESSURE_DELTA = 1
    PIXEL_RIGHT = 30
    MAX_RIGHT = 96

    def __init__(self):
        self.oled_handler = OledHandler(OledHandler.GRAY, "images/background_dark.png")
        self.outside_world_handler = OutsideWorldHandler()
        self.all_handlers = \
            [
                self.SensorHandler(self.oled_handler, self.outside_world_handler.temperature,
                                   (self.PIXEL_RIGHT, 3),
                                   ((self.PIXEL_RIGHT, 0), (self.MAX_RIGHT, 20)),
                                   self.TEMPERATURE_DELTA, 'Temp:', 'C'),
                self.SensorHandler(self.oled_handler, self.outside_world_handler.humidity,
                                   (self.PIXEL_RIGHT, 19),
                                   ((self.PIXEL_RIGHT, 15), (self.MAX_RIGHT, 35)),
                                   self.HUMIDITY_DELTA, 'Hum:', '%'),
                self.SensorHandler(self.oled_handler, self.outside_world_handler.altitude,
                                   (self.PIXEL_RIGHT, 35),
                                   ((self.PIXEL_RIGHT, 30), (self.MAX_RIGHT, 50)),
                                   self.ALTITUDE_DELTA, 'Alt:', 'm'),
                self.SensorHandler(self.oled_handler, self.outside_world_handler.pressure,
                                   (self.PIXEL_RIGHT, 50),
                                   ((self.PIXEL_RIGHT, 45), (self.MAX_RIGHT, 65)),
                                   self.PRESSURE_DELTA, 'Press:', 'hPa')
            ]

    class SensorHandler:
        def __init__(self, oled_handler, accessor, pixel_tuple, clear_tuple, value_delta, extra_text, si_unit):
            self.oled_handler = oled_handler
            self.current_value = accessor()
            self.value_delta = value_delta
            self.accessor = accessor
            self.print_tuple = pixel_tuple
            self.clear_tuple_of_tuples = clear_tuple
            self.extra_text = extra_text
            self.si_unit = si_unit

        def conditioned_print(self, font=Font.ARIAL, color=None):
            new_value = self.accessor()
            if abs(self.current_value - new_value) > self.value_delta:
                self.current_value = new_value
                self.print(font, color)

        def print(self, font=Font.ARIAL, color=None):
            self.clearer()
            text = f'{self.extra_text} {round(self.current_value, 1)} {self.si_unit}'
            self.oled_handler.base_print(self.print_tuple, text, color=color, font=font)

        def clearer(self):
            self.oled_handler.base_clear(self.clear_tuple_of_tuples)

    def first_print_all(self):
        for handler in self.all_handlers:
            handler.print()
        self.oled_handler.show()

    def print_all(self):
        for handler in self.all_handlers:
            handler.conditioned_print()
        self.oled_handler.show()


if __name__ == '__main__':
    exercise_handler = ExerciseHandler()
    exercise_handler.first_print_all()
    while True:
        exercise_handler.print_all()
