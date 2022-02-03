from smbus2 import SMBus
import paho.mqtt.client as mqtt
from mlx90614 import MLX90614
import time
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
print ("Ambient Temperature :"+str(sensor.get_ambient()))
print ("Temperatura del objeto :"+str(sensor.get_object_1()))
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con codigo de resultado {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.1.78", 1883, 60)
while(1):
    print("Temperatura ambiente:"+str(sensor.get_ambient()))
    print("temperatura objeto:"+str(sensor.get_object_1()))
    client.publish('isur/temperatura_salon', payload = sensor.get_ambient(),qos=0,retain=False)
    client.publish('isur/temp',payload = sensor.get_object_1(),qos=0,retain=False)
    time.sleep(5)
bus.close()
