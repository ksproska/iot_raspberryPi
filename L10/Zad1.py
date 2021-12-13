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

    __WHITE = (255, 255, 255)
    __GRAY = (40, 40, 40)

    def __init__(self, background_file="images/background_dark.png"):
        self.__display = SSD1331.SSD1331()
        self.__display.Init()
        self.__display.clear()
        self.__background = Image.open(background_file)
        self.__printer = ImageDraw.Draw(self.__background)

    @property
    def width(self):
        return self.__display.width

    @property
    def height(self):
        return self.__display.height

    # PRINTS --------------------------------------------------------
    def print_temperature(self, text, font=Font.ARIAL, color=None):
        self.__printer.text((30, 3), "24 C", fill=color, font=font)

    def print_humidity(self, text, font=Font.ARIAL, color=None):
        self.__printer.text((30, 19), "24 C", fill=color, font=font)

    def print_altitude(self, text, font=Font.ARIAL, color=None):
        self.__printer.text((30, 35), "24 C", fill=color, font=font)

    def print_pressure(self, text, font=Font.ARIAL, color=None):
        self.__printer.text((30, 50), "24 C", fill=color, font=font)

    # CLEAR ---------------------------------------------------------
    def clear_temperature(self, background_color=__GRAY):
        self.__printer.rectangle(((30, 0), (96, 20)), fill=background_color)

    def clear_humidity(self, background_color=__GRAY):
        self.__printer.rectangle(((30, 15), (96, 35)), fill=background_color)

    def clear_altitude(self, background_color=__GRAY):
        self.__printer.rectangle(((30, 15), (96, 50)), fill=background_color)

    def clear_pressure(self, background_color=__GRAY):
        self.__printer.rectangle(((30, 15), (96, 65)), fill=background_color)


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