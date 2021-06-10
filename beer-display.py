#!/usr/bin/python
# -*- coding: utf8 -*-
# Based on sample code from https://github.com/YahboomTechnology/Raspberry-Pi-RGB-Cooling-HAT/
import time
import os

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 10
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
# font = ImageFont.load_default()
font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 20)
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Write two lines of text.
    cmd = "tail -n 1 tilt.csv | cut -d, -f2"
    beerTemp = subprocess.check_output(cmd, shell = True ).rstrip()
    cmd = "tail -n 1 tilt.csv | cut -d, -f3"
    gravity = subprocess.check_output(cmd, shell = True )
    beerString = "{}C".format(beerTemp)

    draw.text((x, top), beerString, font=font, fill=255)
    draw.text((x+70, top), str(gravity),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
