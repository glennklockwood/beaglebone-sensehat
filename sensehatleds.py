import itertools
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

DEVICE_ADDRESS = 0x46

DEFAULT_PATTERN = [
    [
        [ 0x1F, 0x1F, 0x1F, 0x1F, 0x14, 0x03, 0x00, 0x00, ],
        [ 0x00, 0x00, 0x03, 0x12, 0x1F, 0x1F, 0x1F, 0x1F, ],
        [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, ],
    ],
    [
        [ 0x1F, 0x1F, 0x1F, 0x12, 0x03, 0x00, 0x00, 0x00, ],
        [ 0x00, 0x04, 0x14, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, ],
        [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x1D, ],
    ],
    [
        [ 0x1F, 0x1F, 0x11, 0x02, 0x00, 0x00, 0x00, 0x00, ],
        [ 0x05, 0x15, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0B, ],
        [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x1F, 0x1F, ],
    ],
    [
        [ 0x1F, 0x0F, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, ],
        [ 0x17, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0A, 0x00, ],
        [ 0x00, 0x00, 0x00, 0x00, 0x0A, 0x1F, 0x1F, 0x1F, ],
    ],
    [
        [ 0x0E, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, ],
        [ 0x1F, 0x1F, 0x1F, 0x1F, 0x1D, 0x08, 0x00, 0x00, ],
        [ 0x00, 0x00, 0x01, 0x0B, 0x1F, 0x1F, 0x1F, 0x1F, ],
    ],
    [
        [ 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x14, ],
        [ 0x1F, 0x1F, 0x1F, 0x1B, 0x07, 0x00, 0x00, 0x00, ],
        [ 0x00, 0x01, 0x0C, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, ],
    ],
    [
        [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x15, 0x1F, ],
        [ 0x1F, 0x1F, 0x19, 0x06, 0x00, 0x00, 0x00, 0x00, ],
        [ 0x02, 0x0E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x12, ],
    ],
    [
        [ 0x00, 0x00, 0x00, 0x00, 0x05, 0x17, 0x1F, 0x1F, ],
        [ 0x1F, 0x17, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, ],
        [ 0x0F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0F, 0x02, ],
    ],
]

class LEDMatrix:
    def __init__(self, i2c_bus, address=DEVICE_ADDRESS):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self._brightness = 1.0
        self.nrow = 8
        self.ncol = 8
        self.clear()

    def __str__(self):
        output_str = ""
        for y in range(self.nrow):
            for rgb in range(3):
                for x in range(self.ncol):
                    output_str += "0x{:02x}, ".format(self.pixels[y][rgb][x])
                output_str += "\n"
            output_str += "\n"
        return output_str

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value % 1.0

    def default_pattern(self):
        self.pixels = DEFAULT_PATTERN

    def clear(self):
        self.pixels = [[[0 for x in range(self.ncol)] for rgb in range(3)] for y in range(self.nrow)]

    def set_pixel(self, x, y, red, green, blue):
        self.pixels[y][0][x] = int(red * 63)
        self.pixels[y][1][x] = int(green * 63)
        self.pixels[y][2][x] = int(blue * 63)

    def shift_l(self):
        for irow, row in enumerate(self.pixels):
            for rgb in row:
                rgb0 = rgb[0]
                for col in range(1, self.ncol):
                    rgb[col - 1] = rgb[col]
                rgb[-1] = rgb0

    def shift_r(self):
        for irow, row in enumerate(self.pixels):
            for rgb in row:
                rgb0 = rgb[-1]
                for col in range(1, self.ncol):
                    rgb[self.ncol - col] = rgb[7 - col]
                rgb[0] = rgb0

    def shift_u(self):
        shift_buf = self.pixels[0]
        for row in range(1, self.nrow):
            self.pixels[row - 1] = self.pixels[row]
        self.pixels[-1] = shift_buf

    def shift_d(self):
        shift_buf = self.pixels[-1]
        for row in range(1, self.nrow):
            self.pixels[self.nrow - row] = self.pixels[7 - row]
        self.pixels[0] = shift_buf

    def update(self):
        with self.i2c_device as display:
            display.write(bytearray([0] + [
                int(x * self.brightness) for x in itertools.chain(
                    *itertools.chain(
                        *self.pixels))]))

def demo():
    import time

    i2c = board.I2C()
    display = LEDMatrix(i2c)

    display.default_pattern()
    display.update()

    while True:
        #display.brightness += 0.1
        display.shift_r()
        display.shift_d()
        display.update()
        time.sleep(0.1)

if __name__ == "__main__":
    demo()
