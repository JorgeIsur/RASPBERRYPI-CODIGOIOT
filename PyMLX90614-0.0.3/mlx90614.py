from smbus2 import SMBus
from mlx90614 import MLX90614
import time
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
print ("Ambient Temperature :"), sensor.get_ambient()
while(True):
    print("Object Temperature :"), sensor.get_object_1()
    time.sleep(3)
bus.close()