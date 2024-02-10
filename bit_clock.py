from machine import Pin, I2C, RTC, ADC
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, bookerly_20
from ssd1306 import SSD1306_I2C
import framebuf, sys, utime, imgfile, network, socket


def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

def bit_numbers(number):
    buffer,img_res = imgfile.get_img(number) # get the image byte array
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB) # MONO_HLSB, MONO_VLSB, MONO_HMSB
    return fb

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

def get_connection():
    ssid = 'SERVO'
    password = 'picoservo'

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
      pass

    print('Connection successful')
    print(ap.ifconfig())


    # HTTP server with socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)

    # Listen for connections
    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            # print('Content = %s' % str(request))
            request = str(request)
            print(request)
            # Load html and replace with current data 
            response = get_html('clock.html')
            try:
                response = response.replace('slider_value', str(deg))
                
            except Exception as e:
                response = response.replace('slider_value', '0')
            
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.send(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed')



# CONSTANTS
DAYS = ['MON','TUE','WED','THU','FRI','SAT','SUN']
MONTHS = ['ZERO_MONTH','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

# OLED
pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution
i2c_dev = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller
i2c_right = I2C(0,scl=Pin(21),sda=Pin(20),freq=200000)
oled_right = SSD1306_I2C(pix_res_x, pix_res_y, i2c_right)
# TIME
rtc=machine.RTC()
digit_1,digit_2,digit_3,digit_4 = 0,0,0,0

# ADC
adcpin = 4
sensor = machine.ADC(adcpin)
#big fonts
write20 = Write(oled, ubuntu_mono_20)
write20_right = Write(oled_right, ubuntu_mono_20)
#get_connection()
## Showing running time with blinking colon indicating seconds
while True:
    # Clears the OLED
    oled.fill(0)
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
    write20.text(MONTHS[timestamp[1]], 50, 0, 1)
    write20.text(str("%02d"%(timestamp[2])), 105, 0, 1)
    write20.text(DAYS[timestamp[3]], 0, 0, 1)
    #STOCKS
    write20_right.text('PLTR', 0, 0, 1)
    write20_right.text('8847.45', 55, 0, 1)
    # OUTSIDE TEMPERATURE
    oled_right.blit(bit_numbers(int((((ReadTemperature()*(9/5))+32)-32)/10)), -5, 19) # show the image at location (x=0,y=0)
    oled_right.blit(bit_numbers(int((((ReadTemperature()*(9/5))+32)-32)%10)), 25, 19) # show the image at location (x=0,y=0)
    # DIVIDING LINE
    oled_right.vline(63, 25, 35, 2)
    # INSIDE TEMPERATURE
    oled_right.blit(bit_numbers(int((((ReadTemperature()*(9/5))+32)-6)/10)), 64, 19) # show the image at location (x=0,y=0)
    oled_right.blit(bit_numbers(int((((ReadTemperature()*(9/5))+32)-6)%10)), 94, 19) # show the image at location (x=0,y=0)
    for second in range(2):
        oled.fill_rect(60, 30, 5, 5, second)
        oled.fill_rect(60, 50, 5, 5, second)
        oled.show()
        oled_right.show()
        utime.sleep(1)