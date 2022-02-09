#declaracion de modulos
from smbus2 import SMBus
import paho.mqtt.client as mqtt
from mlx90614 import MLX90614
import time
import RPi.GPIO as gpio
import random
#instancias de objetos
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
#LEDS Y PINES
LED_ENCENDIDO = 12
LED_MQTT = 16
LED_STANDBY = 18
pin_button = 22
#funcion para conectarnos a mqtt
def on_connect(client, userdata, flags, rc):
    for i in range(2):
        gpio.output(LED_MQTT,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_MQTT,False)
    print(f"Conectado con codigo de resultado {rc}")
def parpadeo(LED_ENCENDIDO,LED_MQTT,LED_STANDBY):
    modo = random.randint(0,3)
    if modo == 0:
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
    if modo ==1:
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_STANDBY,False)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,False)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
    if modo ==2:
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,False)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
    if modo ==3:
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,False)
        gpio.output(LED_MQTT,False)
        gpio.output(LED_STANDBY,True)
        time.sleep(1)
        gpio.output(LED_ENCENDIDO,True)
        gpio.output(LED_MQTT,True)
        gpio.output(LED_STANDBY,False)
        time.sleep(1)
#programa principal
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(pin_button,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.setup(LED_ENCENDIDO,gpio.OUT)
gpio.setup(LED_MQTT,gpio.OUT)
gpio.setup(LED_STANDBY,gpio.OUT)
gpio.output(LED_ENCENDIDO,True)
client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.1.78", 1883, 60)
if(gpio.input(pin_button)==gpio.HIGH):
    print("Iniciando lectura:\n")
while(1):
    if(gpio.input(pin_button)==gpio.HIGH):
        print("Iniciando lectura:\n")
        print("Temperatura ambiente:"+str(sensor.get_ambient()))
        print("temperatura objeto:"+str(sensor.get_object_1()))
        client.publish('isur/temperatura_salon', payload = sensor.get_ambient(),qos=0,retain=False)
        client.publish('isur/temp',payload = sensor.get_object_1(),qos=0,retain=False)
        time.sleep(5)
    else:
        print("MODO STANDBY")
        print("Presione el boton durante 3 segundos para iniciar la lectura.")
        parpadeo(LED_ENCENDIDO,LED_MQTT,LED_STANDBY)
bus.close()
