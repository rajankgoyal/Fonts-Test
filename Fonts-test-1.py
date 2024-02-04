from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
from fdrawer import FontDrawer
import utime


i2c = I2C(1,scl=Pin(27),sda=Pin(26),freq=200000)

lcd = SSD1306_I2C(128, 64, i2c)

# # Normal FrameBuffer operation
# lcd.rect( 0, 0, 128, 64, 1 )
# lcd.fill(0)
# lcd.show()

# Use a font drawer to draw font to FrameBuffer
fd = FontDrawer( frame_buffer=lcd, font_name = 'arial60' )
fd.print_str( "8a", 0, 16 )
# lcd.text('2/3 - 69 deg', 0, 8, 1)
# fd.print_char( "#", 100, 2 )
# fd.print_str( fd.font_name, 2, 18 )
# utime.sleep(5)
# Send the FrameBuffer content to the LCD
lcd.show()