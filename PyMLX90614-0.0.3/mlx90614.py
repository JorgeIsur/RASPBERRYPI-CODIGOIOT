from smbus2 import SMBus
import paho.mqtt.client as mqtt
from mlx90614 import MLX90614
import time
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
print ("Ambient Temperature :"), sensor.get_ambient()
print ("Temperatura del objeto :", sensor.get_object_1())
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con codigo de resultado {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.1.72", 1883, 60)
while(1):
    client.publish('isur/temperatura_salon', payload = sensor.get_ambient(),qos=0,retain=false)
    client.publish('isur/temp',payload = sensor.get_object_1(),qos=0,retain=false)
    time.sleep(5)
    client.loop_forever()
bus.close()