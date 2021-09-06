#!/usr/bin/env python3
import board
import adafruit_hts221

def main():
    i2c = board.I2C()
    hts = adafruit_hts221.HTS221(i2c)

    print("Relative humidity: {:.1f}%".format(hts.relative_humidity))
    print("Temperature:       {:.2f} C".format(hts.temperature))

if __name__ == "__main__":
    main()
