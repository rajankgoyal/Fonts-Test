from machine import Pin, I2C, RTC
import utime
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, bookerly_20
import utime
import network
import urequests

WIDTH = 128
HEIGHT = 64
i2c = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)
rtc=machine.RTC()
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
write20 = Write(oled, ubuntu_mono_20)

# Connect to WLAN
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect("NWRKTEST", "FASTCARS1")
# while not wlan.isconnected():
#     pass
# print('Connected to WLAN')

# response = urequests.get('https://official-joke-api.appspot.com/random_joke')
# data = response.json()
# print(data['setup'])
# print(data['punchline'])
# write20.text(data['setup'], 0, 0)
# write20.text(data['punchline'], 0, 40)

# write20.text('RAJAN GOYAL RAJAN GOYAL RAJAN GOYAL RAJAN GOYAL ', 0, 0).
# 
# oled.contrast(255)
# oled.show()
# while True:
#     utime.sleep(1)
# #     oled.fill(0)
#     oled.scroll(-5, 0)
#     oled.show()

while True:
    timestamp=rtc.datetime()
    dateString="%04d-%02d-%02d"%(timestamp[0:3])
    timeString="%02d:%02d:%02d"%(timestamp[4:7])
    write20.text("Cute", 0, 40)
    write20.text(dateString, 0, 20)
    write20.text(timeString, 0, 0)
    oled.show()

#     utime.sleep(0.5)