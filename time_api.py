# Import modules
import network
import urequests,utime
from machine import Pin, I2C, RTC, ADC
from machine import Pin, I2C, RTC, ADC
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, bookerly_20
from ssd1306 import SSD1306_I2C
import framebuf, sys, utime, imgfile, network, socket

#OLED
pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution
i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("NWRKTEST", "FASTCARS1")
while not wlan.isconnected():
    pass
print('Connected to WLAN')

# Make an API call
try:
    response = urequests.get(url='https://worldtimeapi.org/api/timezone/est')
except Exception as e:
    print('failed')

data = response.json()
# print(response.text)
datetime=data['datetime']
day_of_week= data['day_of_week']
print(datetime)

x = datetime.split('T')
date = x[0].split('-')
timestamp = x[1].split('.')
time = timestamp[0].split(':')
print(date)
print(time)
rtc=machine.RTC()
rtc.datetime((int(date[0]),int(date[1]),int(date[2]),int(day_of_week-1),int(time[0]),int(time[1]),int(time[2]),0))
write20 = Write(oled, ubuntu_mono_20)
while True:
    oled.fill(0)
    timestamp=rtc.datetime()
    print(timestamp)
    oled.text(str(timestamp[0:4]), 0, 0, 1)
    oled.text(str(timestamp[4:7]), 0, 35, 1)
    oled.show()
    utime.sleep(1)

