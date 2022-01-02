from PIL import Image, ImageDraw, ImageFont

if __name__ == '__main__':
    img = Image.open("images/background_dark.png")
    MATORAN = ImageFont.truetype("fonts/arial.ttf")

    GRAY = (40, 40, 40)

    draw = ImageDraw.Draw(img)

    draw.text((30, 3), "24 C", fill=(255, 255, 255), font=MATORAN)
    draw.text((30, 19), "24 C", fill=(255, 255, 255), font=MATORAN)
    draw.text((30, 35), "24 C", fill=(255, 255, 255), font=MATORAN)
    draw.text((30, 50), "24 C", fill=(255, 255, 255), font=MATORAN)

    # draw.rectangle(((30, 0), (96, 20)), fill=GRAY)
    # draw.rectangle(((30, 15), (96, 35)), fill=GRAY)
    # draw.rectangle(((30, 30), (96, 50)), fill=GRAY)
    # draw.rectangle(((30, 45), (96, 65)), fill=GRAY)

    #img.show()

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
        GRAY = (40, 40, 40)

        def __init__(self, background_color, background_file):
            self.__background = Image.open(background_file)
            self.__printer = ImageDraw.Draw(self.__background)
            self.__background_color = background_color

        def show(self):
            self.__background.show()

        # PRINTS --------------------------------------------------------
        def base_print(self, xy, text, color=None, font=Font.ARIAL):
            self.__printer.text(xy, text, fill=color, font=font)

        # CLEAR ---------------------------------------------------------
        def base_clear(self, xy):
            self.__printer.rectangle(xy, fill=self.__background_color)

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
            text = f'{self.extra_text} {self.current_value} {self.si_unit}'
            self.oled_handler.base_print(self.print_tuple, text, color=color, font=font)
            print(text)


    oh = OledHandler(OledHandler.GRAY, "images/background_dark.png")
    a = SensorHandler(oh, lambda: 1, (20, 3), ((30, 0), (96, 20)), 0.1, 'Temp: ', 'C')
    b = SensorHandler(oh, lambda: 1, (20, 19), ((30, 15), (96, 35)), 0.1, 'Hum:  ', '%')
    c = SensorHandler(oh, lambda: 1, (20, 35), ((30, 30), (96, 50)), 0.1, 'Alt:     ', 'm')
    d = SensorHandler(oh, lambda: 1, (20, 50), ((30, 45), (96, 65)), 1, 'Press:', 'hPa')
    a.print()
    b.print()
    c.print()
    d.print()
    oh.show()

