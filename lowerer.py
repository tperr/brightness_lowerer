
from PIL import ImageGrab
import time
import os
import subprocess

BACKLIGHT_DIR = "/sys/class/backlight/"
backlights = dict() # could be multiple backlights, this does it with both of them
for sub_dir in os.listdir(BACKLIGHT_DIR):
    with open(BACKLIGHT_DIR + sub_dir + "/max_brightness") as mb:
        backlights[sub_dir] = int(mb.read())

command = "echo %d | /usr/bin/tee /sys/class/backlight/%s/brightness > /dev/null"

lower_bound_trigger = 100
upper_bound_trigger = 100
lower_bound_set = 0.1
upper_bound_set = 1

start = time.time()
timesPerSec = 0

while True:

    # if time.time() - start <= 1:
    #     timesPerSec += 1
    # else:
    #     timesPerSec = 0
    #     start = time.time()
    # print(timesPerSec)

    avg = 0
    img = ImageGrab.grab()
    m_height = img.height
    m_width = img.width
    px = img.load()
    for y in range(0, m_height, 100):
        for x in range(0, m_width, 100):
            color = px[x, y]
            R=color[0]
            G=color[1]
            B=color[2]
            avg += (0.2126*R + 0.7152*G + 0.0722*B)

    avg = (avg/(m_width*m_height/10000))
    if avg > upper_bound_trigger: # if its bright make dimmer
        for m in backlights.keys():
            os.system(command % (round(lower_bound_set * backlights[m]), m))
    if avg < lower_bound_trigger: # if its dim make brighter
        for m in backlights.keys():
            os.system(command % (round(upper_bound_set * backlights[m]), m))