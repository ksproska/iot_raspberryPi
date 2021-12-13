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

    img.show()






