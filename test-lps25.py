#!/usr/bin/env python3

import board
import adafruit_lps2x

i2c = board.I2C()
lps = adafruit_lps2x.LPS25(i2c_bus=i2c, address=0x5c)

print("Pressure: {:.2f} hPa".format(lps.pressure))
print("Temperature: {:.2f} C".format(lps.temperature))
