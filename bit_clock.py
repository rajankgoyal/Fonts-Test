from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf,sys, utime
import one
import number
import imgfile

pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution

i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
i2c_addr = [hex(ii) for ii in i2c_dev.scan()] # get I2C address in hex format
if i2c_addr==[]:
    print('No I2C Display Found') 
    sys.exit() # exit routine if no dev found
else:
    print("I2C Address      : {}".format(i2c_addr[0])) # I2C device address
    print("I2C Configuration: {}".format(i2c_dev)) # print I2C params


oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller

buffer,img_res = number.get_img() # get the image byte array

buffer5,img_res5 = one.get_img() # get the image byte array
buffer10,img_res10 = imgfile.get_img() # get the image byte array


fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
fb5 = framebuf.FrameBuffer(buffer5, img_res5[0], img_res5[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
fb10 = framebuf.FrameBuffer(buffer10, img_res10[0], img_res10[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB


oled.fill(0) # clear the OLED
oled.blit(fb, -5, 16) # show the image at location (x=0,y=0)
oled.blit(fb5, 25, 16) # show the image at location (x=0,y=0)
# oled.blit(fb10, 55, 16) # show the image at location (x=0,y=0)
oled.blit(fb5, 65, 16) # show the image at location (x=0,y=0)
oled.blit(fb5, 95, 16) # show the image at location (x=0,y=0)

oled.text('SUN   FEB 4   38', 0, 0, 1)
oled.show() # show the new text and image
## Showing running time with blinking colon indicating seconds
while True:
    oled.fill_rect(60, 30, 5, 5, 1)
    oled.fill_rect(60, 50, 5, 5, 1)
    oled.show()
    utime.sleep(.5)
    oled.fill_rect(60, 30, 5, 5, 0)
    oled.fill_rect(60, 50, 5, 5, 0)
    oled.show()
    utime.sleep(.5)