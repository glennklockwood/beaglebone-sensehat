import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

DEVICE_ADDRESS = 0x46

DEFAULT_PATTERN = [
    0x1F, 0x1F, 0x1F, 0x1F, 0x14, 0x03, 0x00, 0x00, # 1-8
    0x00, 0x00, 0x03, 0x12, 0x1F, 0x1F, 0x1F, 0x1F, # 9-16
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, # 17-24

    0x1F, 0x1F, 0x1F, 0x12, 0x03, 0x00, 0x00, 0x00, # 25-32
    0x00, 0x04, 0x14, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, # 33-40
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x1D, # 41-48

    0x1F, 0x1F, 0x11, 0x02, 0x00, 0x00, 0x00, 0x00, # 49-56
    0x05, 0x15, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0B, # 57-64
    0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x1F, 0x1F, # 65-72

    0x1F, 0x0F, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, # 73-80
    0x17, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0A, 0x00, # 81-88
    0x00, 0x00, 0x00, 0x00, 0x0A, 0x1F, 0x1F, 0x1F, # 89-96

    0x0E, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, # 97-104
    0x1F, 0x1F, 0x1F, 0x1F, 0x1D, 0x08, 0x00, 0x00, # 105-112
    0x00, 0x00, 0x01, 0x0B, 0x1F, 0x1F, 0x1F, 0x1F, # 113-120

    0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x14, # 121-128
    0x1F, 0x1F, 0x1F, 0x1B, 0x07, 0x00, 0x00, 0x00, # 129-136
    0x00, 0x01, 0x0C, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, # 137-144

    0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x15, 0x1F, # 145-152
    0x1F, 0x1F, 0x19, 0x06, 0x00, 0x00, 0x00, 0x00, # 153-160
    0x02, 0x0E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x12, # 161-168

    0x00, 0x00, 0x00, 0x00, 0x05, 0x17, 0x1F, 0x1F, # 169-176
    0x1F, 0x17, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, # 177-184
    0x0F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0F, 0x02, # 185-192
]

class LEDMatrix:
    def __init__(self, i2c_bus, address=DEVICE_ADDRESS):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self.brightness = 1.0
        self.clear()

    def __str__(self):
        output_str = ""
        for y in range(8):
            for rgb in range(3):
                for x in range(8):
                    output_str += "0x{:02x}, ".format(
                        self.pixels[self.xy2addr(x, y)[rgb]])
                output_str += "\n"
            output_str += "\n"
        return output_str

    def default_pattern(self):
        self.pixels = [0] + DEFAULT_PATTERN

    def clear(self):
        self.pixels = [0] * (8 * 8 * 3 + 1)

    def xy2addr(self, x, y):
        linear_addr = x * 8 + y
        r_addr = (y * 24) + x + 1
        g_addr = r_addr + 8
        b_addr = g_addr + 8
        return r_addr, g_addr, b_addr

    def set_pixel(self, x, y, red, green, blue):
        r_addr, g_addr, b_addr = self.xy2addr(x, y)
        self.pixels[r_addr] = int(red * 63)
        self.pixels[g_addr] = int(green * 63)
        self.pixels[b_addr] = int(blue * 63)

    def shift_l(self):
        shift_buf = self.pixels[1:193:8]
        for col in range(2, 9):
            self.pixels[col-1:193:8] = self.pixels[col:193:8]
        self.pixels[8:193:8] = shift_buf

    def shift_r(self):
        shift_buf = self.pixels[8:193:8]
        for col in range(8, 1, -1):
            self.pixels[col:193:8] = self.pixels[col-1:193:8]
        self.pixels[1:193:8] = shift_buf

    def shift_u(self):
        shift_buf = self.pixels[1:25]
        for row in range(0, 7):
            idx0 = row * 24 + 1
            idxf = idx0 + 24
            self.pixels[idx0:idxf] = self.pixels[idxf:idxf+24]
        self.pixels[169:193] = shift_buf

    def shift_d(self):
        shift_buf = self.pixels[169:193]
        for row in range(6, -1, -1):
            idx0 = row * 24 + 1
            idxf = idx0 + 24
            self.pixels[idxf:idxf+24] = self.pixels[idx0:idxf]
        self.pixels[1:25] = shift_buf

    def update(self):
        with self.i2c_device as display:
            display.write(bytearray([int(x * self.brightness) for x in self.pixels]))

def demo():
    import time

    i2c = board.I2C()
    display = LEDMatrix(i2c)

    display.default_pattern()
    display.update()

    display.brightness = 0.10
    while True:
        display.shift_d()
        display.update()
        time.sleep(0.1)

if __name__ == "__main__":
    demo()
