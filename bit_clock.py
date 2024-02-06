from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
import framebuf,sys, utime
import one
import number
import imgfile

def bit_numbers(number):
    buffer,img_res = imgfile.get_img(number) # get the image byte array
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
    return fb

pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution

i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
rtc=machine.RTC()
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller
# TIME
digit_1,digit_2,digit_3,digit_4 = 0,0,0,0
# bit_numbers(7)
oled.fill(0) # clear the OLED
oled.blit(bit_numbers(digit_1), -5, 19) # show the image at location (x=0,y=0)
oled.blit(bit_numbers(digit_2), 25, 19) # show the image at location (x=0,y=0)
oled.blit(bit_numbers(digit_3), 65, 19) # show the image at location (x=0,y=0)
oled.blit(bit_numbers(digit_4), 95, 19) # show the image at location (x=0,y=0)
## Calender with weather information
oled.text('FEB', 0, 2, 1)
oled.text('14', 29, 2, 1)
oled.text('SUN', 58, 2, 1)
oled.text(' 47', 100, 2, 1)
oled.show() # show the new text and image
## Showing running time with blinking colon indicating seconds
while True:
    timestamp=rtc.datetime()
#     timeString="%02d:%02d:%02d"%(timestamp[4:7])
    digit_1 = int(timestamp[4]/10)
    digit_2 = timestamp[4]%10
    digit_3 = int(timestamp[5]/10)
    digit_4 = timestamp[5]%10
    oled.blit(bit_numbers(digit_1), -5, 19) # show the image at location (x=0,y=0)
    oled.blit(bit_numbers(digit_2), 25, 19) # show the image at location (x=0,y=0)
    oled.blit(bit_numbers(digit_3), 65, 19) # show the image at location (x=0,y=0)
    oled.blit(bit_numbers(digit_4), 95, 19) # show the image at location (x=0,y=0)
    print(digit_4)
    for second in range(2):
        oled.fill_rect(60, 30, 5, 5, second)
        oled.fill_rect(60, 50, 5, 5, second)
        oled.show()
        utime.sleep(1)
        
