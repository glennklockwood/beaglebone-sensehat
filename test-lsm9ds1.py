#!/usr/bin/env python

import board
import adafruit_lsm9ds1

def main():
    i2c = board.I2C()
    sensor = adafruit_lsm9ds1.LSM9DS1_I2C(
        i2c=i2c,
        mag_address=0x1C,
        xg_address=0x6A)

    print("Accelerometer: x={:7.3f}  y={:7.3f}  z={:7.3f} m/s^2".format(
        *sensor.acceleration))
    print("Magnetometer:  x={:7.3f}  y={:7.3f}  z={:7.3f} gauss".format(
        *sensor.magnetic))
    print("Gyroscope:     x={:7.3f}  y={:7.3f}  z={:7.3f} radians/sec".format(
        *sensor.gyro))
    print("Thermometer:   {:.2f} C".format(sensor.temperature))

if __name__ == "__main__":
    main()
