from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
import framebuf, sys, utime, imgfile

def bit_numbers(number):
    buffer,img_res = imgfile.get_img(number) # get the image byte array
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
    return fb

# CONSTANTS
DAYS = ['MON','TUE','WED','THU','FRI','SAT','SUN']
MONTHS = ['ZERO_MONTH','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

# OLED
pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution
i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller

# TIME
rtc=machine.RTC()
digit_1,digit_2,digit_3,digit_4 = 0,0,0,0

## Showing running time with blinking colon indicating seconds
while True:
    timestamp=rtc.datetime()
    # TIME
    digit_1 = int(timestamp[4]/10)
    digit_2 = timestamp[4]%10
    digit_3 = int(timestamp[5]/10)
    digit_4 = timestamp[5]%10
    oled.blit(bit_numbers(digit_1), -5, 19) # show the image at location (x=0,y=0)
    oled.blit(bit_numbers(digit_2), 25, 19) # show the image at location (x=0,y=0)
    oled.blit(bit_numbers(digit_3), 64, 19) # show the image at location (x=0,y=0)
    oled.blit(bit_numbers(digit_4), 94, 19) # show the image at location (x=0,y=0)
    # CALENDER
    oled.text(MONTHS[timestamp[1]], 0, 2, 1)
    oled.text(str(timestamp[2]), 29, 2, 1)
    oled.text(DAYS[timestamp[3]], 58, 2, 1)
    #WEATHER
    oled.text(' 47', 100, 2, 1)
    
    for second in range(2):
        oled.fill_rect(60, 30, 5, 5, second)
        oled.fill_rect(60, 50, 5, 5, second)
        oled.show()
        utime.sleep(1)
        
