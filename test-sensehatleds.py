import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

DEVICE_ADDRESS = 0x46

class LED2472G:
    def __init__(self, i2c_bus, address=DEVICE_ADDRESS):
        self.i2c_device = I2CDevice(i2c, address)
        self.clear()

    def clear(self):
        self.pixels = [0] * (8 * 8 * 3 + 1)

    def set_pixel(self, x, y, red, green, blue):
        linear_addr = x * 8 + y
        r_addr = (y * 24) + x + 1
        g_addr = r_addr + 8
        b_addr = g_addr + 8
        self.pixels[r_addr] = int(red * 64)
        self.pixels[g_addr] = int(green * 64)
        self.pixels[b_addr] = int(blue * 64)

    def update(self):
        with self.i2c_device as display:
            display.write(bytearray(self.pixels))

i2c = board.I2C()
display = LED2472G(i2c)

while True:
    addr = input("Enter register address: ")
    addr = int(addr)
    value = input("Enter value for register: ")
    display.clear()
    print(f"Setting addr={addr} to {value}")
    display.pixels[addr] = int(value, 0)
    display.update()

print("Use ctrl+d to exit the following loop!")
while True:
    display.clear()
    addr = input("Enter x, y (0-7): ")
    x, y = [int(z) for z in addr.replace(",", " ").split()]
    value = input("Enter r, g, b (0.0-1.0): ")
    r, g, b = [float(z) for z in value.replace(",", " ").split()]
    display.set_pixel(x, y, r, g, b)
    display.update()
